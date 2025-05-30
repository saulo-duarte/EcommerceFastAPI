import uuid
from datetime import datetime, timezone

import pytest

from app.models import Review
from tests.models_factory import ReviewFactory, set_factories_session

MAX_RATING = 5.0
MIN_RATING = 1.0


def test_review_creation(session):
    set_factories_session(session)

    review = ReviewFactory()

    session.add(review)
    session.commit()

    assert review.id is not None
    assert MIN_RATING <= review.rating <= MAX_RATING
    assert review.product is not None
    assert review.user is not None


@pytest.mark.parametrize("invalid_rating", [0.5, 5.5, -1, 10])
def test_invalid_rating_raises_error(invalid_rating):
    with pytest.raises(ValueError, match="Rating must be between"):
        Review(
            rating=invalid_rating,
            comment="Muito bom",
            product_id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )


def test_comment_too_long():
    long_comment = "A" * 2000
    with pytest.raises(ValueError, match="Comment must be at most"):
        Review(
            rating=4.0,
            comment=long_comment,
            product_id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
