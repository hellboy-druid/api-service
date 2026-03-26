import os
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="API Service")

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/items/")
def create_item(item: Item):
    logger.info(f"Creating item: {item.name}")
    return {"item": item}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    if item_id < 0:
        raise HTTPException(status_code=400, detail="Invalid item ID")
    item = {"item_id": item_id, "q": q}
    logger.info(f"Retrieving item: {item_id}")
    return item

@app.on_event("startup")
def startup_event():
    logger.info("API Service is starting up...")

@app.on_event("shutdown")
def shutdown_event():
    logger.info("API Service is shutting down...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))