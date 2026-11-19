import pytest
from shop.database import get_connection, init_db

@pytest.fixture
def db_path(tmp_path):
    path = str(tmp_path / "shop_test.db")
    init_db(path)
    with get_connection(path) as conn:
        conn.execute("INSERT INTO users(email,password,name) VALUES(?,?,?)", ("sam@example.test","test-pass","Sam"))
        conn.execute("INSERT INTO products(name,description,price,stock) VALUES(?,?,?,?)", ("Keyboard","Mechanical computer keyboard",50.0,5))
    return path
