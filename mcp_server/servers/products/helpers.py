from backend import db_connector, parse_output


# --- Internal Database Logic ---

@db_connector
def _fetch_products(cur, brief: bool = False):
    """
    Fetches product data from the database.
    """
    query = "SELECT product_id, product_name FROM products;" if brief else "SELECT * FROM products;"
    cur.execute(query)
    return parse_output(cur)

@db_connector
def _fetch_product_by_id(cur, product_id: str):
    """
    Fetches a single product by its ID.
    """
    cur.execute("SELECT * FROM products WHERE product_id = %s;", (product_id,))
    return parse_output(cur, one=True)
