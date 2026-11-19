from shop.database import get_connection

def get_product(product_id, db_path=None):
    with get_connection(db_path) as conn:
        row = conn.execute("SELECT id,name,description,price,stock FROM products WHERE id=?", (product_id,)).fetchone()
    return dict(row) if row else None

def search_products(keyword, db_path=None):
    term = f"%{keyword}%"
    with get_connection(db_path) as conn:
        rows = conn.execute("SELECT id,name,description,price,stock FROM products WHERE name LIKE ? OR description LIKE ? ORDER BY name", (term, term)).fetchall()
    return [dict(row) for row in rows]
