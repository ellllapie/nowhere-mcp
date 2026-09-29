"""Railway entrypoint: Nowhere MCP (Streamable HTTP at /mcp) + web observer page (/).

One service, one port:
  /mcp        -> MCP endpoint for Kelivo / claude.ai
  /           -> observer page (map, body state, postcards)
  /postcards  -> postcard list (JSON), plus reply endpoint

Tool-driving HTTP endpoints (open_door, walk, ... , DELETE postcard) from
nowhere.web are deliberately NOT exposed here: the URL is public, and only
the AI should move the body.
"""

import os

import uvicorn
from starlette.applications import Starlette
from starlette.routing import Mount, Route

from nowhere.server import mcp
from nowhere import web

# Observer-only routes (read state, leave a message, reply to a postcard).
_OBSERVER_ROUTES = [
    Route("/", web.index),
    Route("/state", web.state),
    Route("/message", web.post_message, methods=["POST"]),
    Route("/messages", web.get_messages),
    Route("/postcards", web.get_postcards),
    Route("/postcard/{card_id:int}/reply", web.reply_postcard, methods=["POST"]),
    Route("/history", web.get_history),
    Route("/marks", web.get_marks),
    Route("/sightings", web.get_sightings),
]

mcp_app = mcp.http_app(path="/mcp")

app = Starlette(
    routes=[
        *_OBSERVER_ROUTES,
        Mount("/static", app=web.StaticFiles(directory=web._STATIC_DIR), name="static"),
        Mount("/", app=mcp_app),
    ],
    lifespan=mcp_app.lifespan,
)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    uvicorn.run(app, host="0.0.0.0", port=port)
