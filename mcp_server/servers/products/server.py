from typing import Any
from fastmcp import FastMCP

from backend import handle_errors
from servers.products.helpers import _fetch_products, _fetch_product_by_id


# Define the server for product-related operations
product_server = FastMCP("Products")


# --- MCP Resources (Exposing the Table via GET) ---

@product_server.resource("data://products")
@handle_errors
def get_all_products() -> list[dict[str, Any]]:
    """
    Exposes the entire products table.

    Returns:
        A list of dictionaries representing all products with full details.
    """
    return _fetch_products(brief=False)


@product_server.resource("data://products/product/{product_id}")
@handle_errors
def get_product_by_id(product_id: str) -> dict[str, Any]:
    """
    Exposes a single product record from the products table.

    Args:
        product_id: The ID of the product to retrieve.

    Returns:
        A dictionary representing the product, or a failure message if not found.
    """
    product = _fetch_product_by_id(product_id)
    if not product:
        return {"status": "failure", "message": f"Product with ID '{product_id}' not found."}
    return product


@product_server.tool
@handle_errors
def get_product_data(
    data_detail: str
) -> list[dict[str, Any]] | dict[str, Any]:
    """
    This is a tool that allows to query the databse without calling the specific 
    resource (so far, basic implementation with mcp adapters do not allow to pass an agent resource and prompts).

    data_details is the URL of the data to query. It has to be of the format
    - data://products/product/{product_id}: for a specific product given its id
    - data://products: all the products

    Args:
        data_detail: the data to retrieve

    Returns:
        A list of dictionaries representing the data.
    """
    if data_detail.startswith("data://products/product/"):
        product_id = data_detail.split("/")[-1]
        return _fetch_product_by_id(product_id)
    elif data_detail == "data://products":
        return _fetch_products()
    else:
        return {
            "status": "failure", 
            "message": f"Invalid data detail: {data_detail}. Please use a valid order data URL."
        }
