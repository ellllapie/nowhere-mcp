"""Railway entrypoint: run Nowhere MCP over Streamable HTTP for Kelivo."""

import os

from nowhere.server import mcp

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    mcp.run(transport="streamable-http", host="0.0.0.0", port=port)
