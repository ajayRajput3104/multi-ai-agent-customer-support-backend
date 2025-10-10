# backend/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from backend.multi_ai_support import run_customer_support

app = FastAPI(title="AI Customer Support API", version="1.0")

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def process_query(request: QueryRequest):
    """
    Takes a customer query and returns:
    - category (Technical/Billing/General)
    - sentiment (Positive/Neutral/Negative)
    - response (Generated answer)
    """
    result = run_customer_support(request.query)
    return {"success": True, "data": result}

@app.get("/")
def home():
    return {"message": "Welcome to AI Multi-Agent Customer Support API"}
