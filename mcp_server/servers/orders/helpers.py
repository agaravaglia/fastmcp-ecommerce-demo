from datetime import date
from pydantic import BaseModel, Field

from backend import db_connector, parse_output


# --- Pydantic Models ---
class NewOrderInfo(BaseModel):
    user_id: str = Field(description="The ID of the user placing the order.")
    product_id: str = Field(description="The ID of the product being ordered.")
    quantity: int = Field(gt=0, description="The number of units to order. Must be positive.")


# --- Internal Database Logic ---
@db_connector
def _fetch_orders(cur):
    """
    Fetches all orders from the database.
    """
    cur.execute("SELECT * FROM orders ORDER BY purchase_date DESC;")
    return parse_output(cur)

@db_connector
def _fetch_order_by_id(cur, order_id: str):
    """
    Fetches a single order by its ID.
    """
    cur.execute("SELECT * FROM orders WHERE order_id = %s;", (order_id,))
    return parse_output(cur, one=True)

@db_connector
def _fetch_user_purchase_history(cur, user_id: str):
    """
    Fetches all orders associated with a specific user.
    """
    cur.execute(
        """
        SELECT o.order_id, o.purchase_date, o.status, p.product_name, o.quantity, p.price
        FROM orders o JOIN products p ON o.product_id = p.product_id
        WHERE o.user_id = %s ORDER BY o.purchase_date DESC;
        """,
        (user_id,)
    )
    return parse_output(cur)

@db_connector
def _create_new_order(cur, order_details: NewOrderInfo):
    """
    Creates a new order in the database and updates stock.
    """
    import uuid
    # Check for sufficient stock
    cur.execute("SELECT stock_quantity FROM products WHERE product_id = %s;", (order_details.product_id,))
    stock = cur.fetchone()
    if not stock or stock[0] < order_details.quantity:
        raise ValueError(f"Insufficient stock for product {order_details.product_id}.")

    # Create the new order
    order_id = f"ord_{str(uuid.uuid4())[:8]}"
    cur.execute(
        """
        INSERT INTO orders (order_id, user_id, product_id, quantity, purchase_date, status)
        VALUES (%s, %s, %s, %s, %s, 'submitted') RETURNING order_id;
        """,
        (order_id, order_details.user_id, order_details.product_id, order_details.quantity, date.today())
    )
    new_order_id = cur.fetchone()[0]

    # Decrement stock
    cur.execute(
        "UPDATE products SET stock_quantity = stock_quantity - %s WHERE product_id = %s;",
        (order_details.quantity, order_details.product_id)
    )
    return {"order_id": new_order_id, "status": "success"}