import uuid
from datetime import datetime, timezone

from app.models import Cart, User

def test_cart_creation(session):
   user = User(
      id=uuid.uuid4(),
      email="test@test.com",
      hashed_password="hashed_password",
      full_name="Test User",
      is_active=True,
      is_superuser=False,
      created_at=datetime.now(timezone.utc),
      updated_at=datetime.now(timezone.utc),
   )
   session.add(user)
   session.commit()

   cart = Cart(
      id=uuid.uuid4(),
      user_id=user.id,
      created_at=datetime.now(timezone.utc),
      updated_at=datetime.now(timezone.utc),
      is_active=True,
      is_checked_out=False,
   )
   session.add(cart)
   session.commit()

   assert cart.id is not None
   assert cart.user_id is not None
   assert cart.is_active is True
   assert cart.is_checked_out is False
   assert cart.created_at is not None
   assert cart.updated_at is not None
   assert isinstance(cart.created_at, datetime)
   assert isinstance(cart.updated_at, datetime)
   assert cart.created_at.tzinfo is not None

   db_cart = session.query(Cart).filter_by(user_id=cart.user_id).first()
   assert db_cart is not None