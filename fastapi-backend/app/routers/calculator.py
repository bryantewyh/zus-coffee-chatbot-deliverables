from fastapi import APIRouter
from pydantic import BaseModel
from typing import Any

router = APIRouter(prefix="/calculator", tags=["calculator"])

class CalculatorRequest(BaseModel):
    expression: str

class CalculatorResponse(BaseModel):
    success: bool
    result: Any
    message: str

@router.post("/", response_model=CalculatorResponse)
async def calculate(request: CalculatorRequest):
    """Perform mathematical calculations"""
    try:
        result = eval(request.expression, {"__builtins__": {}}, {})
        return CalculatorResponse(
            success=True,
            result=result,
            message=f"Calculation result: {result}"
        )
    except Exception as e:
        return CalculatorResponse(
            success=False,
            result=None,
            message="I was unable to help with that request right now. Would you like to explore our products or outlets instead?"
        )

@router.get("/health")
async def health():
    """Health check for calculator"""
    return {"status": "healthy"}