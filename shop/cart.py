from shop.database import get_connection

def add_to_cart(user_id, product_id, quantity=1, db_path=None):
    if quantity < 1:
        raise ValueError("Quantity must be positive")
    with get_connection(db_path) as conn:
        found = conn.execute("SELECT id FROM products WHERE id=?", (product_id,)).fetchone()
        if found is None:
            raise ValueError("Product not found")
        conn.execute("INSERT INTO cart_items(user_id,product_id,quantity) VALUES(?,?,?)", (user_id, product_id, quantity))

def remove_from_cart(user_id, product_id, db_path=None):
    with get_connection(db_path) as conn:
        result = conn.execute("DELETE FROM cart_items WHERE user_id=? AND product_id=?", (user_id, product_id))
    return result.rowcount > 0

def get_cart(user_id, db_path=None):
    with get_connection(db_path) as conn:
        rows = conn.execute("SELECT p.id product_id,p.name,p.price,c.quantity FROM cart_items c JOIN products p ON p.id=c.product_id WHERE c.user_id=? ORDER BY p.name", (user_id,)).fetchall()
    return [dict(row) for row in rows]
