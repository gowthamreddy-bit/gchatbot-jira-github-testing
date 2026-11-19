import pytest
from shop.auth import login_user, verify_token
from shop.cart import add_to_cart, get_cart
from shop.inventory import check_stock
from shop.orders import cancel_order, create_order
from shop.payments import process_payment, refund_payment
from shop.products import get_product, search_products
from shop.users import get_user, update_profile

def test_login_accepts_valid_credentials(db_path):
    assert login_user("sam@example.test","test-pass",db_path)["name"] == "Sam"

def test_login_rejects_wrong_password(db_path):
    assert login_user("sam@example.test","wrong",db_path) is None

def test_token_verification():
    assert verify_token("user:1") == 1
    assert verify_token("invalid") is None

def test_profile_update(db_path):
    assert update_profile(1,"Samuel",db_path)
    assert get_user(1,db_path)["name"] == "Samuel"

def test_product_search_and_lookup(db_path):
    assert search_products("keyboard",db_path)[0]["name"] == "Keyboard"
    assert get_product(1,db_path)["stock"] == 5

def test_cart_add(db_path):
    add_to_cart(1,1,2,db_path)
    assert get_cart(1,db_path)[0]["quantity"] == 2

def test_stock_check(db_path):
    assert check_stock(1,5,db_path)
    assert not check_stock(1,6,db_path)

def test_order_reduces_stock(db_path):
    order_id = create_order(1,[{"product_id":1,"quantity":2}],db_path)
    assert get_product(1,db_path)["stock"] == 3
    assert order_id == 1

def test_order_rejects_insufficient_stock(db_path):
    with pytest.raises(ValueError):
        create_order(1,[{"product_id":1,"quantity":10}],db_path)

def test_cancel_order_restores_stock(db_path):
    order_id = create_order(1,[{"product_id":1,"quantity":2}],db_path)
    assert cancel_order(order_id,db_path)
    assert get_product(1,db_path)["stock"] == 5

def test_payment_and_refund(db_path):
    order_id = create_order(1,[{"product_id":1,"quantity":1}],db_path)
    assert process_payment(order_id,50.0,db_path)
    assert refund_payment(order_id,db_path)
