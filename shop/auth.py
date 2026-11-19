from shop.database import get_connection

def login_user(email, password, db_path=None):
    with get_connection(db_path) as conn:
        row = conn.execute("SELECT id,email,name,password FROM users WHERE email=?", (email,)).fetchone()
    if row is None or row["password"] != password:
        return None
    return {"id": row["id"], "email": row["email"], "name": row["name"]}

def verify_token(token):
    if not token or not token.startswith("user:"):
        return None
    value = token.removeprefix("user:")
    return int(value) if value.isdigit() else None
