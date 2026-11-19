from shop.database import get_connection

def process_payment(order_id, amount, db_path=None):
    if amount <= 0:
        raise ValueError("Payment amount must be positive")
    with get_connection(db_path) as conn:
        order = conn.execute("SELECT total,status FROM orders WHERE id=?", (order_id,)).fetchone()
        if order is None or order["status"] != "pending" or round(order["total"],2) != round(amount,2):
            return False
        conn.execute("INSERT INTO payments(order_id,amount,status) VALUES(?,?,?)", (order_id, amount, "succeeded"))
        conn.execute("UPDATE orders SET status='paid' WHERE id=?", (order_id,))
    return True

def refund_payment(order_id, db_path=None):
    with get_connection(db_path) as conn:
        payment = conn.execute("SELECT id FROM payments WHERE order_id=? AND status='succeeded' ORDER BY id DESC LIMIT 1", (order_id,)).fetchone()
        if payment is None:
            return False
        conn.execute("UPDATE payments SET status='refunded' WHERE id=?", (payment["id"],))
        conn.execute("UPDATE orders SET status='refunded' WHERE id=?", (order_id,))
    return True
