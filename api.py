"""
#Gyan Labs - Enterprise AI Commerce REST API (FastAPI)
======================================================
Production-grade RESTful API endpoints for multi-route chatbot querying,
hardware catalog search, order tracking, and FAQ retrieval.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import uvicorn
from src.pipeline import CommerceChatbotPipeline

app = FastAPI(
    title="#Gyan Labs AI Hardware & Commerce API",
    description="High-performance REST API for enterprise AI hardware search, order tracking, and procurement FAQs.",
    version="1.0.0"
)

pipeline = CommerceChatbotPipeline()


class MessageRequest(BaseModel):
    query: str = Field(..., example="Show me all NVIDIA H100 servers")
    force_route: Optional[str] = Field(None, example="catalog_sql")


class TrackOrderRequest(BaseModel):
    order_id_or_tracking: str = Field(..., example="GL-ORD-8821")


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "#Gyan Labs AI Commerce Platform"}


@app.post("/chat")
def chat_endpoint(req: MessageRequest):
    try:
        res = pipeline.process_message(req.query, force_route=req.force_route)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/catalog")
def get_catalog(category: Optional[str] = None):
    try:
        products = pipeline.get_all_products(category=category)
        return {"count": len(products), "products": products}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/track")
def track_order_endpoint(req: TrackOrderRequest):
    try:
        res = pipeline.order_tracker.track_order(req.order_id_or_tracking)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8001, reload=True)
