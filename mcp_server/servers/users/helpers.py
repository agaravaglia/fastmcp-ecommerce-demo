import uuid
from pydantic import BaseModel, Field

from backend import db_connector, parse_output


# --- Pydantic Models for Data Validation ---
class NewUserInfo(BaseModel):
    name: str = Field(description="Full name of the user.")
    email: str = Field(description="Unique email address of the user.")
    phone_number: str | None = Field(None, description="Phone number of the user.")
    shipping_address: str | None = Field(None, description="Shipping address for the user.")

class UserUpdateInfo(BaseModel):
    name: str | None = Field(None, description="New full name of the user.")
    email: str | None = Field(None, description="New email address of the user.")
    phone_number: str | None = Field(None, description="New phone number of the user.")
    shipping_address: str | None = Field(None, description="New shipping address for the user.")


# --- Internal Database Logic ---

@db_connector
def _fetch_users(cur, brief: bool = False):
    """
    Fetches user data from the database.
    """
    query = "SELECT user_id, name FROM users;" if brief else "SELECT * FROM users;"
    cur.execute(query)
    return parse_output(cur)

@db_connector
def _fetch_user_by_id(cur, user_id: str):
    """
    Fetches a single user by their ID.
    """
    cur.execute("SELECT * FROM users WHERE user_id = %s;", (user_id,))
    return parse_output(cur, one=True)

@db_connector
def _add_new_user(cur, user_info: NewUserInfo):
    """
    Adds a new user to the database.
    """
    user_id = f"usr_{str(uuid.uuid4())[:8]}"
    cur.execute(
        """
        INSERT INTO users (user_id, name, email, phone_number, shipping_address)
        VALUES (%s, %s, %s, %s, %s) RETURNING user_id;
        """,
        (user_id, user_info.name, user_info.email, user_info.phone_number, user_info.shipping_address)
    )
    return {
        "user_id": cur.fetchone()[0], 
        "status": "success"
    }

@db_connector
def _modify_user(cur, user_id: str, user_data: UserUpdateInfo):
    """
    Updates an existing user's data.
    """
    update_fields = {k: v for k, v in user_data.model_dump().items() if v is not None}
    if not update_fields:
        raise ValueError("No fields provided to update.")

    set_clause = ", ".join([f"{key} = %s" for key in update_fields.keys()])
    values = list(update_fields.values()) + [user_id]
    
    query = f"UPDATE users SET {set_clause} WHERE user_id = %s;"
    cur.execute(query, tuple(values))

    if cur.rowcount == 0:
        return {"status": "failure", "message": f"User with ID '{user_id}' not found."}
    return {
        "user_id": user_id, 
        "status": "success", 
        "updated_fields": list(update_fields.keys())
    }
