from pydantic import BaseModel, HttpUrl

class _ErrorResponseData(BaseModel):
    message: str

class ErrorResponse(BaseModel):
    success: bool
    data: _ErrorResponseData
    