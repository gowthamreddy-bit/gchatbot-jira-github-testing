from shop.database import get_connection

def get_user(user_id, db_path=None):
    with get_connection(db_path) as conn:
        row = conn.execute("SELECT id,email,name FROM users WHERE id=?", (user_id,)).fetchone()
    return dict(row) if row else None

def update_profile(user_id, name, db_path=None):
    with get_connection(db_path) as conn:
        result = conn.execute("UPDATE users SET name=? WHERE id=?", (name, user_id))
    return result.rowcount == 1
