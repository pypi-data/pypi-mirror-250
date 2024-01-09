async def application(scope, receive, send):
    """Trivial example of a raw ASGI 3.0 application without a framework."""
    if scope["type"] == "http":
        await receive()
        await send(
            {
                "type": "http.response.start",
                "status": 200,
                "headers": [
                    [b"content-type", b"text/plain"],
                ],
            }
        )
        await send(
            {
                "type": "http.response.body",
                "body": b"Hello, world!",
                "more_body": False,
            }
        )
