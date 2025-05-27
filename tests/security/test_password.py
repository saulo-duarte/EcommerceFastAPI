import pytest

from app.models.value_objects import Password

VALID_PASSWORD = "Str0ng!Pass"

def test_should_hash_and_verify_password_successfully():
    pw = Password(raw=VALID_PASSWORD)
    hashed = pw.hash()

    assert pw.verify(hashed)


@pytest.mark.parametrize("weak_password", [
    "short",
    "noupper1!",
    "NOLOWER1!",
    "NoSpecial1",
    "NoDigit!!"
])
def test_should_raise_error_on_weak_password(weak_password):
    with pytest.raises(ValueError, match="Password must be at least 8 characters"):
        Password(raw=weak_password)
