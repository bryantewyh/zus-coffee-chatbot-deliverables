"""FastAPI for outlets/products"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import products, outlets, calculator
from dotenv import load_dotenv
import uvicorn
import os
# Load environment variables
load_dotenv()

app = FastAPI(
    title="ZUS Coffee API",
    description="FastAPI backend for ZUS Coffee product KB and outlet queries",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(products.router)
app.include_router(outlets.router)
app.include_router(calculator.router)

@app.get("/")
async def root():
    return {
        "message": "ZUS Coffee API",
        "status": "running",
        "endpoints": {
            "calculator": "/calculator",
            "calculator_health": "/calculator/health",
            "products": "/products?query=<search_query>&top_k=3",
            "products_health": "/products/health",
            "outlets": "/outlets?query=<natural_language_query>",
            "outlets_schema": "/outlets/schema",
            "outlets_health": "/outlets/health",
            "outlets_nearest": "/outlets/nearest",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)