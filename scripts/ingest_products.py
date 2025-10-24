import json
import os
import numpy as np
from typing import List, Dict
import faiss
from sentence_transformers import SentenceTransformer
import pickle

class ProductVectorStore:
    def __init__(self, model_name='sentence-transformers/all-MiniLM-L6-v2'):
        """Initialize vector store with sentence transformer model"""
        print(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        self.index = None
        self.products = []
        self.product_texts = []
        
    def create_product_text(self, product: Dict) -> str:
        """Create searchable text representation of product"""
        parts = []
        
        # Add name
        if product.get('name'):
            parts.append(f"Product: {product['name']}")
        
        # Add category
        if product.get('category'):
            parts.append(f"Category: {product['category']}")
        
        # Add price
        if product.get('price'):
            parts.append(f"Price: {product['price']}")
        
        # Add detailed description
        if product.get('detailed_description'):
            parts.append(f"Description: {product['detailed_description']}")
        
        return ' | '.join(parts)
    
    def ingest_products(self, products: List[Dict]):
        """Ingest products into vector store"""
        print(f"\nIngesting {len(products)} products...")
        
        self.products = products
        self.product_texts = []
        
        # Create searchable text for each product
        for product in products:
            text = self.create_product_text(product)
            self.product_texts.append(text)
        
        # Generate embeddings
        print("Generating embeddings...")
        embeddings = self.model.encode(
            self.product_texts,
            show_progress_bar=True,
            convert_to_numpy=True
        )
        
        # Create FAISS index
        print("Building FAISS index...")
        self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(embeddings.astype('float32'))
        
        print(f"Vector store created with {self.index.ntotal} products")
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search for products using semantic similarity"""
        if self.index is None:
            raise ValueError("Vector store not initialized. Run ingest_products first.")
        
        # Generate query embedding
        query_embedding = self.model.encode([query], convert_to_numpy=True)
        
        # Search
        distances, indices = self.index.search(
            query_embedding.astype('float32'), 
            top_k
        )
        
        # Return results with scores
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.products):
                result = {
                    **self.products[idx],
                    'score': float(distances[0][i]),
                    'matched_text': self.product_texts[idx]
                }
                results.append(result)
        
        return results
    
    def save(self, index_path: str, data_path: str):
        """Save FAISS index and product data"""
        print(f"\nSaving vector store...")
        
        # Save FAISS index
        faiss.write_index(self.index, index_path)
        
        # Save products and texts
        data = {
            'products': self.products,
            'product_texts': self.product_texts
        }
        with open(data_path, 'wb') as f:
            pickle.dump(data, f)
        
        print(f"Saved index to {index_path}")
        print(f"Saved data to {data_path}")
    
    def load(self, index_path: str, data_path: str):
        """Load FAISS index and product data"""
        print(f"\nLoading vector store...")
        
        # Load FAISS index
        self.index = faiss.read_index(index_path)
        
        # Load products and texts
        with open(data_path, 'rb') as f:
            data = pickle.load(f)
            self.products = data['products']
            self.product_texts = data['product_texts']
        
        print(f"Loaded {self.index.ntotal} products from index")

def main():
    """Main ingestion pipeline"""
    # Paths
    products_file = 'data/products/drinkware.json'
    index_dir = 'data/vector_store'
    index_path = os.path.join(index_dir, 'products.index')
    data_path = os.path.join(index_dir, 'products.pkl')
    
    # Create directory
    os.makedirs(index_dir, exist_ok=True)
    
    # Load products
    print("Loading products from JSON...")
    if not os.path.exists(products_file):
        print(f"Error: {products_file} not found. Run scrape_products.py first.")
        return
    
    with open(products_file, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    print(f"Loaded {len(products)} products")
    
    # Initialize vector store
    vector_store = ProductVectorStore()
    
    # Ingest products
    vector_store.ingest_products(products)
    
    # Save vector store
    vector_store.save(index_path, data_path)
    
    # Test search
    print("\n" + "=" * 50)
    print("Testing search functionality...")
    print("=" * 50 + "\n")
    
    test_queries = [
        "thermal mug for hot drinks",
        "portable water bottle",
        "coffee tumbler"
    ]
    
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        print("-" * 50)
        results = vector_store.search(query, top_k=3)
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['name']} - {result['price']}")
            print(f"   Score: {result['score']:.4f}")
    
    print("\nIngestion complete!")

if __name__ == "__main__":
    main()