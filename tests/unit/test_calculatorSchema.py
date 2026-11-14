from app.schemas.calculatorSchema import CalculationCreate, CalculationRead
import pytest
from datetime import datetime
from pydantic import ValidationError, model_validator

def test_calculation_create_valid():
    data = {
        "a": 5,
        "b": 10,
        "type": "add"
    }
    calc_create = CalculationCreate(**data)
    assert calc_create.a == 5
    assert calc_create.b == 10
    assert calc_create.type == "add"

def test_calculation_create_invalid():
    data = {
        "a": "invalid",
        "b": 10,
        "type": "add"
    }
    with pytest.raises(ValidationError):
        CalculationCreate(**data)

def test_calculation_read_valid():
    data = {
        "id": 1,
        "a": 5,
        "b": 10,
        "type": "add",
        "result": 15,
        "created_at": datetime.now()
    }
    calc_read = CalculationRead(**data)
    assert calc_read.id == 1
    assert calc_read.a == 5
    assert calc_read.b == 10
    assert calc_read.type == "add"
    assert calc_read.result == 15
    assert isinstance(calc_read.created_at, datetime)

def test_calculation_read_invalid():
    data = {
        "id": "invalid",
        "a": 5,
        "b": 10,
        "type": "add",
        "result": 15,
        "created_at": datetime.now()
    }
    with pytest.raises(ValidationError):
        CalculationRead(**data)
def test_calculation_create_divide_by_zero():
    data = {
        "a": 5,
        "b": 0,
        "type": "divide"
    }
    with pytest.raises(ValueError):
        CalculationCreate(**data)

def test_calculation_read_divide_by_zero():
    data = {
        "id": 1,
        "a": 5,
        "b": 0,
        "type": "divide",
        "result": 0,
        "created_at": datetime.now()
    }
    with pytest.raises(ValueError):
        CalculationRead(**data)