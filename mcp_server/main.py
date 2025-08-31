from fastmcp import FastMCP

from servers.users.server import user_server
from servers.products.server import product_server
from servers.orders.server import order_server

# Initialize the main MCP application
mcp_server = FastMCP("Ecommerce")

# Mount the individual servers with their respective prefixes
mcp_server.mount(user_server, prefix="users")
mcp_server.mount(product_server, prefix="products")
mcp_server.mount(order_server, prefix="orders")


if __name__ == "__main__":
    mcp_server.run(
        transport="http",
        host="0.0.0.0",
        port=8000,
        log_level="debug",
    )