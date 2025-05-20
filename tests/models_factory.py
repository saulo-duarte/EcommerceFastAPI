import uuid
from datetime import datetime, timezone
from decimal import Decimal

import factory
from factory.alchemy import SQLAlchemyModelFactory

from app.models import (
    Address,
    Cart,
    CartItem,
    Category,
    Order,
    OrderItem,
    OrderStatus,
    Payment,
    PaymentMethod,
    PaymentStatus,
    Product,
    Review,
    Shipment,
    ShipmentStatus,
    User,
)


def set_factories_session(session):
    UserFactory._meta.sqlalchemy_session = session
    AddressFactory._meta.sqlalchemy_session = session
    CategoryFactory._meta.sqlalchemy_session = session
    ProductFactory._meta.sqlalchemy_session = session
    ReviewFactory._meta.sqlalchemy_session = session
    CartFactory._meta.sqlalchemy_session = session
    CartItemFactory._meta.sqlalchemy_session = session
    OrderFactory._meta.sqlalchemy_session = session
    OrderItemFactory._meta.sqlalchemy_session = session
    PaymentFactory._meta.sqlalchemy_session = session
    ShipmentFactory._meta.sqlalchemy_session = session


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = None

    id = factory.LazyFunction(uuid.uuid4)
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    hashed_password = factory.LazyFunction(lambda: "Aa1!aaaa")
    full_name = "John Doe"
    is_active = True
    is_superuser = False
    created_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    updated_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))


class AddressFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Address
        sqlalchemy_session = None

    id = factory.LazyFunction(uuid.uuid4)
    user = factory.SubFactory(UserFactory)

    street = factory.Faker("street_address")
    city = factory.Faker("city")
    state = factory.Faker("state")
    country = factory.Faker("country")
    postal_code = factory.LazyFunction(lambda: "12345-678")

    is_default_shipping = False
    is_default_billing = False
    created_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    updated_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))


class CategoryFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Category
        sqlalchemy_session = None

    id = factory.LazyFunction(uuid.uuid4)
    name = factory.Sequence(lambda n: f"Category {n}")
    description = factory.Faker("sentence", nb_words=6)
    created_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))


class ProductFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Product
        sqlalchemy_session = None

    id = factory.LazyFunction(uuid.uuid4)
    name = factory.Faker("word")
    description = factory.Faker("paragraph")
    stock = factory.Faker("random_int", min=0, max=100)
    price = factory.Faker(
        "pyfloat", left_digits=2, right_digits=2, positive=True, min_value=1.0
    )
    is_active = True
    created_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    updated_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))

    category = factory.SubFactory(CategoryFactory)


class ReviewFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Review
        sqlalchemy_session = None

    id = factory.LazyFunction(uuid.uuid4)
    user = factory.SubFactory(UserFactory)
    product = factory.SubFactory(ProductFactory)
    rating = factory.Faker(
        "pyfloat",
        left_digits=1,
        right_digits=1,
        positive=True,
        min_value=1.0,
        max_value=5.0,
    )
    comment = factory.Faker("paragraph", nb_sentences=2)
    created_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    updated_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))


class CartFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Cart
        sqlalchemy_session = None

    id = factory.LazyFunction(uuid.uuid4)
    user = factory.SubFactory(UserFactory)
    created_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    updated_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    is_active = True
    is_checked_out = False


class CartItemFactory(SQLAlchemyModelFactory):
    class Meta:
        model = CartItem
        sqlalchemy_session = None

    id = factory.LazyFunction(uuid.uuid4)
    cart = factory.SubFactory(CartFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = factory.Faker("random_int", min=1, max=10)
    price_snapshot = factory.LazyAttribute(lambda o: float(o.product.price))
    created_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    updated_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))


class OrderItemFactory(SQLAlchemyModelFactory):
    class Meta:
        model = OrderItem
        sqlalchemy_session = None

    id = factory.LazyFunction(uuid.uuid4)
    order = factory.SubFactory("tests.models_factory.OrderFactory")
    product = factory.SubFactory(ProductFactory)
    quantity = 1
    price_snapshot = factory.LazyAttribute(lambda o: Decimal(str(o.product.price)))


class OrderFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Order
        sqlalchemy_session = None

    id = factory.LazyFunction(uuid.uuid4)
    user = factory.SubFactory(UserFactory)
    status = OrderStatus.PENDING
    total_price = Decimal("0.00")
    shipping_address = factory.SubFactory(AddressFactory)
    billing_address = factory.SubFactory(AddressFactory)
    created_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    updated_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))


class PaymentFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Payment
        sqlalchemy_session = None

    id = factory.LazyFunction(uuid.uuid4)
    order = factory.SubFactory(OrderFactory)
    amount = factory.LazyFunction(lambda: Decimal("100.00"))
    currency = "brl"
    stripe_payment_intent_id = None
    stripe_status = None
    status = PaymentStatus.PENDING
    method = PaymentMethod.CREDIT_CARD
    created_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    updated_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))


class ShipmentFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Shipment
        sqlalchemy_session = None

    id = factory.LazyFunction(uuid.uuid4)
    order = factory.SubFactory(OrderFactory)
    tracking_number = factory.Faker("uuid4")
    status = ShipmentStatus.PENDING
    shipping_address = factory.SubFactory(AddressFactory)
    billing_address = factory.SubFactory(AddressFactory)
    created_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    updated_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))
