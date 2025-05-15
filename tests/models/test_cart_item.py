import uuid
from datetime import datetime, timezone
from decimal import Decimal

import pytest
from app.models import CartItem, Cart, Product, User, Category

def test_cart_item_creation(session):
    now = datetime.now(timezone.utc)
    
    user = User(
        id=uuid.uuid4(),
        email="testuser@example.com",
        hashed_password="hashedpassword123",
        full_name="Test User",
        is_active=True,
        is_superuser=False,
        created_at=now,
        updated_at=now,
    )
    
    cart = Cart(
        id=uuid.uuid4(),
        user=user,
        created_at=now,
        updated_at=now,
        is_active=True,
        is_checked_out=False,
    )
    
    category = Category(
        name="Eletrônicos",
        description="Produtos eletrônicos em geral",
        created_at=now,
    )
    
    product = Product(
        id=uuid.uuid4(),
        category=category,
        name="Test Product",
        description="Test Description",
        price=Decimal("10.00"),
        stock=100,
        created_at=now,
        updated_at=now,
    )
    
    session.add_all([user, cart, category, product])
    session.flush()  # gera IDs, mas não commita
    
    cart_item = CartItem(
        id=uuid.uuid4(),
        cart=cart,
        product=product,
        quantity=2,
        price_snapshot=Decimal("10.00"),
        created_at=now,
        updated_at=now,
    )
    
    session.add(cart_item)
    session.commit()
    
    assert cart_item.id is not None
    assert cart_item.cart_id == cart.id
    assert cart_item.product_id == product.id
    assert cart_item.quantity == 2
    assert cart_item.price_snapshot == Decimal("10.00")
    assert isinstance(cart_item.created_at, datetime)
    assert isinstance(cart_item.updated_at, datetime)
    assert cart_item.cart == cart
    assert cart_item.product == product
