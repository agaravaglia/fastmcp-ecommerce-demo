from typing import Any
from datetime import date
from fastmcp import FastMCP

from backend import handle_errors
from servers.orders.helpers import (
    NewOrderInfo,
    _fetch_orders, 
    _fetch_order_by_id, 
    _create_new_order,
    _fetch_user_purchase_history
)

# Define the server for order-related operations
order_server = FastMCP("Orders")


# --- MCP Resources (Exposing the Table via GET) ---
@order_server.resource("data://orders",)
@handle_errors
def get_all_orders() -> list[dict[str, Any]]:
    """
    Exposes the entire orders table.

    Returns:
        A list of dictionaries representing the orders.
    """
    return _fetch_orders()

@order_server.resource("data://orders/order/{order_id}")
@handle_errors
def get_order_by_id(order_id: str) -> dict[str, Any]:
    """
    Exposes a single order record from the orders table. 

    Args:
        order_id: The ID of the order to retrieve.
    
    Returns: 
        A dictionary representing the order.
    """
    order = _fetch_order_by_id(order_id)
    if not order:
        return {"status": "failure", "message": f"Order with ID '{order_id}' not found."}
    return order

@order_server.resource("data://orders/user/{user_id}")
@handle_errors
def get_user_orders(user_id: str) -> list[dict[str, Any]]:
    """
    Exposes the history of purschases for a single user.

    Args:
        user_id: The ID of the user to retrieve orders for.

    Returns:
        A list of dictionaries representing the user's orders.
    """
    history = _fetch_user_purchase_history(user_id)
    if not history:
        return [{"message": f"No orders found for user ID '{user_id}'."}]
    return history

# --- MCP Tools (Functions for the Agent to Use) ---
@order_server.tool
@handle_errors
def create_order(order_info: NewOrderInfo) -> dict[str, Any]:
    """
    Places a new order, validates stock, and decrements stock quantity.

    Args:
        order_info: A model containing user_id, product_id, and quantity.
    
    Returns:
        A dictionary with the new order's ID and a success status.
    """
    return _create_new_order(order_info)


@order_server.tool
@handle_errors
async def get_order_data(
    data_detail: str
) -> list[dict[str, Any]] | dict[str, Any]:
    """
    This is a tool that allows to query the databse without calling the specific 
    resource (so far, basic implementation with mcp adapters do not allow to pass an agent resource and prompts).

    data_details is the URL of the data to query. It has to be of the format 
    - data://orders/order/{order_id}: for a specific order given its id
    - data://orders/user/{user_id}: all the orders for the given user
    - data://orders: all the users

    Args:
        data_detail: the data to retrieve

    Returns:
        A list of dictionaries representing the data.
    """
    if data_detail.startswith("data://orders/order/"):
        order_id = data_detail.split("/")[-1]
        return _fetch_order_by_id(order_id)
    elif data_detail.startswith("data://orders/user/"):
        user_id = data_detail.split("/")[-1]
        return _fetch_user_purchase_history(user_id)
    elif data_detail == "data://orders":
        return _fetch_orders()
    else:
        return {
            "status": "failure", 
            "message": f"Invalid data detail: {data_detail}. Please use a valid order data URL."
        }
