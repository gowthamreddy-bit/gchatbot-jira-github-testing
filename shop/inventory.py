from shop.database import get_connection

def check_stock(product_id, quantity, db_path=None):
    with get_connection(db_path) as conn:
        row = conn.execute("SELECT stock FROM products WHERE id=?", (product_id,)).fetchone()
    return row is not None and quantity > 0 and row["stock"] >= quantity

def update_stock(product_id, change, db_path=None):
    with get_connection(db_path) as conn:
        result = conn.execute("UPDATE products SET stock=stock+? WHERE id=? AND stock+?>=0", (change, product_id, change))
    return result.rowcount == 1
