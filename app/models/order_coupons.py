from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID

from app.db import mapper_registry

order_coupons = Table(
    "order_coupons",
    mapper_registry.metadata,
    Column("order_id", UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), primary_key=True),
    Column("coupon_id", UUID(as_uuid=True), ForeignKey("coupons.id", ondelete="CASCADE"), primary_key=True),
)
