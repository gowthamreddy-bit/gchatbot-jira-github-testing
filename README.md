# ShopLite — E-commerce Test Application

A small Python e-commerce backend for testing Gchatbot's GitHub code search, Graphify relationships, and future Jira-to-code / Jira-to-PR workflows. It uses plain Python and SQLite, not FastAPI or Flask.

## Modules
- `shop/auth.py` — login and token verification
- `shop/users.py` — user lookup and profile updates
- `shop/products.py` — product lookup and search
- `shop/cart.py` — cart item management
- `shop/inventory.py` — stock checks and updates
- `shop/orders.py` — order creation and cancellation
- `shop/payments.py` — simulated payment and refund operations
- `shop/database.py` — SQLite connection and schema setup

## Setup
Python 3.10+ is recommended.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
```

Tests use temporary SQLite databases. No real payment provider, credentials, or external service is used.

## Planned Jira investigation scenarios
1. Login rejects a valid user when the supplied password is incorrect.
2. Product search omits a matching product because of a search-filter defect.
3. Adding the same product twice creates duplicate cart rows.
4. Order creation must reject quantities greater than available stock.
5. A successful simulated payment leaves an order pending.
6. Cancelling an order fails to restore inventory.

These are test scenarios to introduce deliberately only when a matching Jira test needs them. The initial application remains small and understandable.
