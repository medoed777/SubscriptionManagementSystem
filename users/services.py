import stripe

from config.settings import API_KEY_PUBLISHER_STRIPE

stripe.api_key = API_KEY_PUBLISHER_STRIPE


def create_stripe_product(name_product: str) -> dict:
    product = stripe.Product.create(
        name=name_product,
        description=f"Продукт: {name_product}",
    )
    return product


def create_stripe_price_amount(name_product: str, amount: int) -> dict:
    product = create_stripe_product(name_product)
    price = stripe.Price.create(
        currency="rub",
        unit_amount=amount * 100,
        recurring={"interval": "month"},
        product=product.id,
    )
    return price


def create_stripe_session(price: dict) -> tuple:
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/success",
        cancel_url="http://127.0.0.1:8000/cancel",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
