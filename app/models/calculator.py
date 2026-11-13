from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.operations import add, subtract, multiply, divide


class Calculator(Base):
    __tablename__ = "calculator"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id", on_delete="CASCADE"), nullable=False , index=True)
    a = Column(Float, nullable=False, index=True)
    b = Column(Float, nullable=False, index=True)
    type = Column(String(50), nullable=False, index=True)
    result = Column(Float, nullable=False, index=True)

    user = relationship("User", back_populates="calculator")

    def __repr__(self):
        return f"<Calculator(id={self.id}, user_id={self.user_id}, a={self.a}, b={self.b}, type={self.type}, result={self.result})>"

class CalculatorFactory():
    @staticmethod
    def create(user_id, type, a, b):
        if type == "add":
            result = add(a, b)
        elif type == "subtract":
            result = subtract(a, b)
        elif type == "multiply":
            result = multiply(a, b)
        elif type == "divide":
            try:
                result = divide(a, b)
            except ZeroDivisionError:
                raise ValueError("Cannot divide by zero")
        else:
            raise ValueError(f"Unsupported type: {type}")
        return Calculator(user_id=user_id, a=a, b=b, type=type, result=result)

        