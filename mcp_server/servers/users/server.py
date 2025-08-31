from typing import Any
from fastmcp import FastMCP

from backend import handle_errors
from servers.users.helpers import (
    NewUserInfo, 
    UserUpdateInfo,
    _fetch_users, 
    _fetch_user_by_id, 
    _add_new_user,
    _modify_user
)


# Define the server for user-related operations
user_server = FastMCP("Users")


# --- MCP Resources (Exposing the Table via GET) ---

@user_server.resource("data://users")
@handle_errors
def get_all_users() -> list[dict[str, Any]]:
    """
    Exposes the entire users table.

    Returns:
        A list of dictionaries representing all users with full details.
    """
    return _fetch_users(brief=False)

@user_server.resource("data://users/user/{user_id}")
@handle_errors
def get_user_by_id(user_id: str) -> dict[str, Any]:
    """
    Exposes a single user record from the users table.

    Args:
        user_id: The ID of the user to retrieve.

    Returns:
        A dictionary representing the user, or a failure message if not found.
    """
    user = _fetch_user_by_id(user_id)
    if not user:
        return {"status": "failure", "message": f"User with ID '{user_id}' not found."}
    return user

# --- MCP Tools (to be used by an agent) ---

@user_server.tool
@handle_errors
def add_new_user(user_info: NewUserInfo) -> dict[str, Any]:
    """
    Adds a new user with the provided information.

    Args:
        user_info: A model containing the new user's name, email, and optional details.

    Returns:
        A dictionary with the new user's ID and a success status.
    """
    return _add_new_user(user_info)

@user_server.tool
@handle_errors
def modify_user_info(user_id: str, updates: UserUpdateInfo) -> dict[str, Any]:
    """
    Updates one or more details for an existing user.

    Args:
        user_id: The ID of the user to modify.
        updates: A model with the fields to update. Only non-null fields will be changed.

    Returns:
        A dictionary confirming the update.
    """
    return _modify_user(user_id, updates)


@user_server.tool
@handle_errors
def get_user_data(
    data_detail: str
) -> list[dict[str, Any]] | dict[str, Any]:
    """
    This is a tool that allows to query the databse without calling the specific 
    resource (so far, basic implementation with mcp adapters do not allow to pass an agent resource and prompts).

    data_detail is the URL of the data to query. It has to be of the format
    - data://users/user/{user_id}: for a specific user given its id
    - data://users: all the users

    Args:
        data_detail: the data to retrieve

    Returns:
        A list of dictionaries representing the data.
    """
    if data_detail.startswith("data://users/user/"):
        user_id = data_detail.split("/")[-1]
        return _fetch_user_by_id(user_id)
    elif data_detail == "data://users":
        return _fetch_users()
    else:
        return {
            "status": "failure", 
            "message": f"Invalid data detail: {data_detail}. Please use a valid user data URL."
        }