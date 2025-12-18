from src.utils import validate_amount, validate_date, validate_category


def test_validate_amount():
    success, value = validate_amount("100")
    assert success is True
    assert value == 100.0

    success, value = validate_amount("-50")
    assert success is False

    success, value = validate_amount("abc")
    assert success is False


def test_validate_date():
    success, value = validate_date("2024-12-01")
    assert success is True
    assert value == "2024-12-01"

    success, value = validate_date("2024-13-01")
    assert success is False

    success, value = validate_date("invalid")
    assert success is False


def test_validate_category():
    success, value = validate_category("Food")
    assert success is True
    assert value == "Food"

    success, value = validate_category("Random")
    assert success is True
    assert value == "Random"

    success, value = validate_category("")
    assert success is False
