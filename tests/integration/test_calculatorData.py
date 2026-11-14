import pytest

from app.models.users import Users
from app.models.calculator import Calculator, CalculatorFactory
from app.schemas.calculatorSchema import CalculationCreate
from pydantic import ValidationError
from sqlalchemy import func, select


@pytest.fixture
def saved_user(db_session):
    user = Users(
        username="calc_test_user",
        email="calc_test@example.com",
        password_hash=Users.hash_password("TestPassword123")
    )
    db_session.add(user)
    db_session.flush()
    return user

@pytest.mark.parametrize(
    "operation,a,b,expected",
    [
        ("add", 5, 10, 15),
        ("subtract", 10, 5, 5),
        ("multiply", 5, 10, 50),
        ("divide", 10, 4, 2.5),
    ]
)
def test_save_calculation(
    db_session, saved_user, operation, a, b, expected
):
    user_id = saved_user.id
    calculation = CalculatorFactory.create(
        user_id=saved_user.id,
        type=operation,
        a=a,
        b=b
    )

    db_session.add(calculation)
    db_session.commit()
    calculation_id = calculation.id

    # Clear cached objects so the next lookup reads from PostgreSQL.
    db_session.expunge_all()

    stored = db_session.get(Calculator, calculation_id)
    assert stored is not None
    assert stored.user_id == user_id
    assert stored.a == a
    assert stored.b == b
    assert stored.type == operation
    assert stored.result == pytest.approx(expected)

@pytest.mark.parametrize(
    "data",
    [
        {"a": 5, "b": 10, "type": "invalid"},
        {"a": 5, "b": 0, "type": "divide"},
    ]
)
def test_invalid_calculation_is_not_saved(db_session, saved_user, data):
    count_query = select(func.count()).select_from(Calculator)
    count_before = db_session.scalar(count_query)

    with pytest.raises(ValidationError):
        validated = CalculationCreate(**data)

        calculation = CalculatorFactory.create(
            user_id=saved_user.id,
            type=validated.type,
            a=validated.a,
            b=validated.b
        )
        db_session.add(calculation)
        db_session.commit()

    assert db_session.scalar(count_query) == count_before