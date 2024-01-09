from asphalt.core import Component, Context, inject, resource
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse


async def root() -> str:
    return "Hello, world!"


class WebRootComponent(Component):
    @inject
    async def start(self, ctx: Context, app: FastAPI = resource()) -> None:
        app.add_api_route("/", root, response_class=PlainTextResponse)
