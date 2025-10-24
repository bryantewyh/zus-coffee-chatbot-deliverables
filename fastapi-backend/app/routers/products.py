from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from typing import List
import faiss
import pickle
from sentence_transformers import SentenceTransformer
from pathlib import Path
import threading

router = APIRouter(prefix="/products", tags=["products"])

# Global variables to load once
_model = None
_index = None
_products = None
_init_lock = threading.Lock()
_initialized = False

def _initialize():
    """Initialize the vector store"""
    global _model, _index, _products, _initialized
    if _initialized:
        return

    with _init_lock:
        if _initialized:
            return
        print("Loading product vector store...")

        BASE_DIR = Path(__file__).resolve().parents[2]
        VECTOR_DIR = BASE_DIR / "data" / "vector_store"
        INDEX_PATH = VECTOR_DIR / "products.index"
        PICKLE_PATH = VECTOR_DIR / "products.pkl"

        _model = SentenceTransformer('all-MiniLM-L6-v2')
        _index = faiss.read_index(str(INDEX_PATH))

        with open(PICKLE_PATH, 'rb') as f:
            data = pickle.load(f)
            _products = data.get('products', data) if isinstance(data, dict) else data

        _initialized = True
        print(f"Loaded {_index.ntotal} vectors and {len(_products)} products")


# Response models
class Product(BaseModel):
    name: str
    category: str
    price: str
    description: str = ""
    image_url: str = ""
    url: str = ""

class ProductSearchResponse(BaseModel):
    query: str
    products: List[Product]
    count: int
    top_k: int

@router.get("/", response_model=ProductSearchResponse)
async def search_products(
    query: str = Query(..., description="Search query for products"),
    top_k: int = Query(3, ge=1, le=10, description="Number of results to return")
):
    """
    Search ZUS Coffee drinkware products using semantic vector search.
    Returns raw product data without AI summary.
    
    Example: GET /products?query=thermal+bottle&top_k=3
    """
    try:
        _initialize()
        
        # Encode the query
        query_embedding = _model.encode([query], convert_to_numpy=True)
        
        # Search in FAISS index
        distances, indices = _index.search(
            query_embedding.astype('float32'), 
            top_k
        )
        
        # Collect results
        results = []
        print(f"Search returned indices: {indices[0]}, distances: {distances[0]}")
        print(f"Total products available: {len(_products)}")
        
        for idx, dist in zip(indices[0], distances[0]):
            print(f"Processing index {idx}, distance {dist}")
            if idx < len(_products):
                product = _products[idx]
                print(f"Found product: {product.get('name', 'Unknown')}")
                results.append(Product(
                    name=product.get('name', 'Unknown'),
                    category=product.get('category', 'N/A'),
                    price=product.get('price', 'N/A'),
                    description=product.get('detailed_description', ''),
                    image_url=product.get('image_url', ''),
                    url=product.get('url', '')
                ))
            else:
                print(f"Index {idx} is out of range!")
        
        print(f"Returning {len(results)} results")
        
        return ProductSearchResponse(
            query=query,
            products=results,
            count=len(results),
            top_k=top_k
        )
        
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=500, 
            detail="Product data not found. Please run ingestion script first."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health():
    """Health check endpoint"""
    try:
        _initialize()
        return {
            "status": "healthy",
            "products_loaded": _index.ntotal if _index else 0
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }