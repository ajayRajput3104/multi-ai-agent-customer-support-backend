from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    """Customer query request model"""
    query: str = Field(..., min_length=1, description="Customer query text")

class SupportResponse(BaseModel):
    """Support response model"""
    category: str
    sentiment: str
    response: str

class APIResponse(BaseModel):
    """Standard API response wrapper"""
    success: bool
    data: SupportResponse
    message: str = "Query processed successfully"