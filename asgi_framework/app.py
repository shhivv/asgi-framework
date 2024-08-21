from typing import Any
from .responses import Response, TextResponse


class App:
    def __init__(self) -> None:
        self.routes = {}

    async def __call__(self, scope, receive, send) -> Any:
        assert scope["type"] == "http"
        if self.routes.get(scope["path"]):
            response = await self.routes[scope["path"]]()
            await response(scope, receive, send)

    def get(self, path: str):
        def inner(func):
            self.routes[path] = func

        return inner


app = App()


@app.get("/")
async def index():
    return TextResponse("Hello World")
