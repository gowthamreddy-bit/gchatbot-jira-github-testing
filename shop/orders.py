from shop.database import get_connection
from shop.inventory import check_stock

def create_order(user_id, items, db_path=None):
    if not items:
        raise ValueError("An order must contain at least one item")
    for item in items:
        if item["quantity"] < 1 or not check_stock(item["product_id"], item["quantity"], db_path):
            raise ValueError(f"Insufficient stock for product {item['product_id']}")
    with get_connection(db_path) as conn:
        total = 0.0
        for item in items:
            product = conn.execute("SELECT price FROM products WHERE id=?", (item["product_id"],)).fetchone()
            total += product["price"] * item["quantity"]
        cur = conn.execute("INSERT INTO orders(user_id,status,total) VALUES(?,?,?)", (user_id, "pending", total))
        order_id = cur.lastrowid
        for item in items:
            product = conn.execute("SELECT price FROM products WHERE id=?", (item["product_id"],)).fetchone()
            conn.execute("INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES(?,?,?,?)", (order_id, item["product_id"], item["quantity"], product["price"]))
            conn.execute("UPDATE products SET stock=stock-? WHERE id=?", (item["quantity"], item["product_id"]))
    return order_id

def cancel_order(order_id, db_path=None):
    with get_connection(db_path) as conn:
        order = conn.execute("SELECT status FROM orders WHERE id=?", (order_id,)).fetchone()
        if order is None or order["status"] != "pending":
            return False
        items = conn.execute("SELECT product_id,quantity FROM order_items WHERE order_id=?", (order_id,)).fetchall()
        for item in items:
            conn.execute("UPDATE products SET stock=stock+? WHERE id=?", (item["quantity"], item["product_id"]))
        conn.execute("UPDATE orders SET status='cancelled' WHERE id=?", (order_id,))
    return True
