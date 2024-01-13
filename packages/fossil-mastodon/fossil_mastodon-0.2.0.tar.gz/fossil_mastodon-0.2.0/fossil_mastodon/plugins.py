import abc
import functools
import inspect
import re
import traceback
from typing import Callable, Type

from fastapi import FastAPI, Request, responses, templating
import pkg_resources
import pydantic

from fossil_mastodon import algorithm, ui, core


def title_case_to_spaced(string):
    # The regex pattern looks for any lowercase letter followed by an uppercase letter
    # and inserts a space between them
    return re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', string)


TootDisplayFn = Callable[[core.Toot, "RenderContext"], responses.Response]
class TootDisplayPlugin(pydantic.BaseModel):
    fn: TootDisplayFn
    fn_name: str

    def render_str(self, toot: core.Toot, context: "RenderContext") -> str:
        obj = self.fn(toot, context)
        content = obj.body.decode("utf-8")
        return content


class RenderContext(pydantic.BaseModel):
    """
    A context object for rendering a template.
    """
    class Config:
        arbitrary_types_allowed = True
    templates: templating.Jinja2Templates
    request: Request
    link_style: ui.LinkStyle
    session: core.Session

    def template_args(self) -> dict:
        return {
            "request": self.request,
            "link_style": self.link_style,
            "ctx": self,
        }

    def render_toot_display_plugins(self, toot: core.Toot) -> str:
        return "".join(
            plugin.render_str(toot, self)
            for plugin in get_toot_display_plugins()
        )


_app: FastAPI | None = None


class Plugin(pydantic.BaseModel):
    """
    Plugin registration API
    
    Example:

        plugin = Plugin(name="My Plugin", description="Add button to toot that triggers an API POST operation")

        @plugin.api_operation.post("/my_plugin")
        def my_plugin(request: Request):
            return responses.HTMLResponse("<div>💯</div>")

        @plugin.toot_display_button
        def my_toot_display(toot: core.Toot, context: RenderContext):
            return responses.HTMLResponse("<div>💯</div>")

    """
    name: str
    display_name: str | None = None
    description: str | None = None
    author: str | None = None
    author_url: str | None = None
    enabled_by_default: bool = True
    _toot_display_buttons: list[TootDisplayPlugin] = pydantic.PrivateAttr(default_factory=list)
    _algorithms: list[Type[algorithm.BaseAlgorithm]] = pydantic.PrivateAttr(default_factory=list)

    @pydantic.validator("display_name", always=True)
    def _set_display_name(cls, v, values):
        return v or values["name"]

    @property
    def api_operation(self) -> FastAPI:
        assert _app is not None
        return _app

    def toot_display_button(self, impl: TootDisplayFn) -> TootDisplayFn:
        """
        Decorator for adding a button to the toot display UI. This function should return a
        fastapi.responses.Response object. The result will be extracted and inserted into the
        toot display UI.
        """
        name = impl.__name__

        @functools.wraps(impl)
        def wrapper(toot: core.Toot, context: RenderContext):
            try:
                return impl(toot, context)
            except TypeError as e:
                raise BadPluginFunction(self, impl, "example_function(toot: fossil_mastodon.core.Toot, context: fossil_mastodon.plugins.RenderContext)") from e
            except Exception as e:
                import inspect
                print(inspect.signature(impl))
                raise RuntimeError(f"Error in toot display plugin '{self.name}', function '{name}'") from e

        self._toot_display_buttons.append(TootDisplayPlugin(fn=wrapper, fn_name=name))
        return wrapper

    def algorithm(self, algo: Type[algorithm.BaseAlgorithm]) -> Type[algorithm.BaseAlgorithm]:
        """
        Decorator for adding an algorithm class.
        """
        if not issubclass(algo, algorithm.BaseAlgorithm):
            raise ValueError(f"Algorithm {algo} is not a subclass of algorithm.BaseAlgorithm")
        self._algorithms.append(algo)
        algo.plugin = self
        return algo


def init_plugins(app: FastAPI):
    global _app
    _app = app
    get_plugins()


@functools.lru_cache
def get_plugins() -> list[Plugin]:
    if _app is None:
        raise RuntimeError("Plugins not initialized")

    plugins = []
    for entry_point in pkg_resources.iter_entry_points("fossil_mastodon.plugins"):
        print("Loading plugin", entry_point.name)
        try:
            plugin = entry_point.load()
            if isinstance(plugin, Plugin):
                plugins.append(plugin)
            else:
                print(f"Error loading toot display plugin '{entry_point.name}': not a subclass of Plugin")
        except:
            print(f"Error loading toot display plugin {entry_point.name}")
            traceback.print_exc()
    return plugins


def get_toot_display_plugins() -> list[TootDisplayPlugin]:
    return [
        b 
        for p in get_plugins() 
        for b in p._toot_display_buttons
    ]


def get_algorithms() -> list[Type[algorithm.BaseAlgorithm]]:
    return [
        algo
        for p in get_plugins()
        for algo in p._algorithms
    ]


class BadPluginFunction(Exception):
    def __init__(self, plugin: Plugin, function: callable, expected_signature: str):
        super().__init__(f"Bad function call: {plugin.name}.{function.__name__} should have signature {expected_signature}")
        self.plugin = plugin
        self.function = function
        self.signature = inspect.signature(function)
        self.expected_signature = expected_signature
        self.function_name = function.__name__
