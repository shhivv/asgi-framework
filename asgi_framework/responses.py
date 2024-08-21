class Response:
    def __init__(self, body, **kwargs) -> None:
        self.status = kwargs.get("status", 200)
        self.headers = kwargs.get("headers", [])
        self.body = body

    def _set_mimetype(self, mimetype):
        self.mimetype = mimetype
        self.headers.append([b"content-type", bytes(mimetype, "utf-8")])

    def _start(self):
        return {
            "type": "http.response.start",
            "status": self.status,
            "headers": self.headers,
        }

    def _body(self):
        return {
            "type": "http.response.body",
            "body": bytes(self.body, "utf-8"),
        }

    async def __call__(self, _scope, _receive, send):
        await send(self._start())
        await send(self._body())


class JSONResponse(Response):
    def __init__(self, body, **kwargs) -> None:
        super().__init__(body, **kwargs)
        self.body = kwargs.get("body", {})
        self._set_mimetype("application/json")


class HTMLResponse(Response):
    def __init__(self, body, **kwargs) -> None:
        super().__init__(body, **kwargs)
        self._set_mimetype("text/html")


class TextResponse(Response):
    def __init__(self, body, **kwargs) -> None:
        super().__init__(body, **kwargs)
        self._set_mimetype("text/plain")


class FileResponse(Response):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._set_mimetype("application/octet-stream")
