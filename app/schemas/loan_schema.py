from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.schemas.user_schema import UserResponse
from app.schemas.device_schema import DeviceResponse


class LoanCreate(BaseModel):
    user_id: int = Field(..., example=1)
    device_id: int = Field(..., example=1)


class LoanUpdate(BaseModel):
    return_date: Optional[datetime] = Field(None)
    status: Optional[str] = Field(None, example="returned")


class LoanResponse(BaseModel):
    id: int
    user_id: int
    device_id: int
    loan_date: datetime
    return_date: Optional[datetime] = None
    status: str

    class Config:
        from_attributes = True


class LoanDetailResponse(BaseModel):
    id: int
    status: str
    loan_date: datetime
    return_date: Optional[datetime] = None
    user: UserResponse
    device: DeviceResponse

    class Config:
        from_attributes = True