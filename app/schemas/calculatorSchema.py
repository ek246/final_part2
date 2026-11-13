from typing import Literal
from pydantic import BaseModel, ConfigDict, model_validator

class CalculationCreate(BaseModel):
    # Validate that division by zero does not occur after the model is created
    @model_validator(mode="after")
    def check_divide_by_zero(cls, values):
        a = values.get("a")
        b = values.get("b")
        type = values.get("type")
        if b == 0 and type == "divide":
            raise ValueError("Cannot divide by zero")
        return values
    
    a: float
    b: float
    type: Literal["add", "subtract", "multiply", "divide"]

    

class CalculationRead(BaseModel):
   # Validate that division by zero does not occur after the model is created
   @model_validator(mode="after")
   def check_divide_by_zero(cls, values):
        a = values.get("a")
        b = values.get("b")
        type = values.get("type")
        if b == 0 and type == "divide":
            raise ValueError("Cannot divide by zero")
        return values
   a: float
   b: float
   type: Literal["add", "subtract", "multiply", "divide"]
   result: float