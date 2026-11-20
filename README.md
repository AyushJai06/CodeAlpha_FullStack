# OnStore — Django E-commerce Project

OnStore is a Django-based e-commerce application with product browsing, user accounts, a session-based cart, checkout, Cash on Delivery orders, and stock management.

## Apps
- `accounts/` — registration, login, logout, profile
- `store/` — product catalogue and product details
- `cart/` — shopping cart
- `orders/` — checkout and order records
- `payment/` — payment-related app
- `config/` — Django project configuration

## Setup
1. Create and activate a virtual environment.
2. Install dependencies: `pip install -r requirements.txt`.
3. Set a secure `DJANGO_SECRET_KEY` environment variable before deployment.
4. Run `python manage.py migrate`.
5. Run `python manage.py createsuperuser` if admin access is needed.
6. Start the development server: `python manage.py runserver`.

The local SQLite database is intentionally not included. Product media images are included under `media/products/`.

## Security note
Do not commit `.env` files, production secrets, user databases, or virtual environments. `DEBUG` and `ALLOWED_HOSTS` must be configured appropriately before deployment.