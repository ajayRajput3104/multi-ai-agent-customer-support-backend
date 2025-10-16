from fastapi import APIRouter, HTTPException, status
from app.models.schemas import QueryRequest, APIResponse, SupportResponse
from app.core.multi_ai_support import run_customer_support
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/query", response_model=APIResponse, status_code=status.HTTP_200_OK)
async def process_query(request: QueryRequest):
    """
    Process customer query and return categorized response
    
    - **query**: Customer query text
    
    Returns:
    - **category**: Technical/Billing/General
    - **sentiment**: Positive/Neutral/Negative
    - **response**: Generated support response
    """
    try:
        result = run_customer_support(request.query)
        
        support_response = SupportResponse(
            category=result["category"],
            sentiment=result["sentiment"],
            response=result["response"]
        )
        
        return APIResponse(success=True, data=support_response,message="Query processed successfully")
    
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing query: {str(e)}"
        )

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "AI Customer Support API"}