from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker
from openai import OpenAI
import os
import math
import threading
from pathlib import Path

router = APIRouter(prefix="/outlets", tags=["outlets"])

# Global variables
_engine = None
_session = None
_openai_client = None
_schema = None
_init_lock = threading.Lock()
_initialized = False

def _initialize():
    """Initialize database and OpenAI client    """
    global _engine, _session, _openai_client, _schema, _initialized
    if _initialized:
        return

    with _init_lock:
        if _initialized:
            return
        print("Loading Outlets SQL Service...")

        BASE_DIR = Path(__file__).resolve().parents[2]
        DB_PATH = BASE_DIR / "data" / "outlets" / "zus_outlets.db"
        _engine = create_engine(f"sqlite:///{DB_PATH}")
        Session = sessionmaker(bind=_engine)
        _session = Session()

        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")

        _openai_client = OpenAI(api_key=api_key)
        _schema = _get_schema()
        _initialized = True

        print("Connected to outlets database")

def _get_schema() -> str:
    """Get database schema as a string"""
    inspector = inspect(_engine)
    
    schema_parts = ["Database Schema for ZUS Coffee Outlets:\n"]
    
    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        
        schema_parts.append(f"\nTable: {table_name}")
        schema_parts.append("Columns:")
        
        for col in columns:
            col_type = str(col['type'])
            nullable = "NULL" if col['nullable'] else "NOT NULL"
            desc = ""
            
            # Add helpful descriptions for each field
            if col['name'] == 'id':
                desc = " (Primary key)"
            elif col['name'] == 'name':
                desc = " (Outlet name, e.g., 'ZUS Coffee - KLCC')"
            elif col['name'] == 'address':
                desc = " (Full address)"
            elif col['name'] == 'city':
                desc = " (City name, e.g., 'Kuala Lumpur', 'Petaling Jaya')"
            elif col['name'] == 'state':
                desc = " (State name, e.g., 'Selangor', 'Kuala Lumpur')"
            elif col['name'] == 'postcode':
                desc = " (5-digit postcode)"
            elif col['name'] == 'latitude':
                desc = " (GPS latitude)"
            elif col['name'] == 'longitude':
                desc = " (GPS longitude)"
            elif col['name'] == 'phone':
                desc = " (Local phone format)"
            elif col['name'] == 'phone_international':
                desc = " (International phone format)"
            elif col['name'] == 'operating_hours':
                desc = " (Full weekly schedule text)"
            elif col['name'] == 'open_time':
                desc = " (Opening time in HH:MM:SS format)"
            elif col['name'] == 'close_time':
                desc = " (Closing time in HH:MM:SS format)"
            elif col['name'] == 'business_status':
                desc = " (e.g., 'OPERATIONAL')"
            
            schema_parts.append(f"  - {col['name']} ({col_type}, {nullable}){desc}")
    
    return "\n".join(schema_parts)

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate distance between two coordinates using Haversine formula
    Returns distance in kilometers
    """
    R = 6371  
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = (math.sin(delta_lat/2)**2 + 
         math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    distance = R * c
    return round(distance, 2)

def _text_to_sql(query: str) -> str:
    """Convert natural language to SQL using OpenAI"""
    _initialize()
    
    # Check if the user is trying something malicious
    dangerous_keywords = ['delete', 'drop', 'update', 'insert', 'alter', 'truncate']
    query_lower = query.lower()
    
    # If query contains dangerous keywords directly, reject it
    if any(keyword in query_lower for keyword in dangerous_keywords):
        # Return invalid SQL that will be caught by validator
        return f"-- BLOCKED: Dangerous operation detected: {query}"
    
    prompt = f"""
            You are a SQL expert. Convert the following natural language query into a SQL query for a SQLite database.

            {_schema}

            Important Rules:
            1. ONLY generate SELECT queries
            2. If the user asks to DELETE, UPDATE, INSERT, DROP, or ALTER, respond with: "SELECT 'Operation not allowed' as error"
            3. Use proper SQLite syntax
            4. Use LIKE with '%' for partial text matching
            5. Use LOWER() for case-insensitive text searches

            CRITICAL - Location Search Strategy:
            When users search for a location (like "KLCC", "SS 15", "Sunway Pyramid", "Cheras", "Petaling Jaya"), they might be referring to:
            - The outlet NAME (e.g., "ZUS Coffee - KLCC")
            - The ADDRESS (e.g., "Suria KLCC, Kuala Lumpur")
            - The CITY (e.g., "Kuala Lumpur", "Petaling Jaya")
            - The STATE (e.g., "Selangor", "Kuala Lumpur")

            ALWAYS search across name, address, city, AND state columns using OR conditions.
            Examples:
            WRONG: "outlets in Sungai Long" → WHERE LOWER(name) LIKE '%zus coffee%' OR LOWER(address) LIKE '%sungai long%'
            CORRECT: "outlets in Sungai Long" → WHERE LOWER(name) LIKE '%sungai long%' OR LOWER(address) LIKE '%sungai long%' OR LOWER(city) LIKE '%sungai long%' OR LOWER(state) LIKE '%sungai long%'

            WRONG: "find ZUS Coffee in KLCC" → WHERE LOWER(name) LIKE '%zus%' AND (LOWER(name) LIKE '%klcc%' OR ...)
            CORRECT: "find ZUS Coffee in KLCC" → WHERE LOWER(name) LIKE '%klcc%' OR LOWER(address) LIKE '%klcc%' OR LOWER(city) LIKE '%klcc%' OR LOWER(state) LIKE '%klcc%'
            
            Time-based Queries:
            - open_time and close_time are in 24-hour format (HH:MM:SS)
            - To find outlets open at a specific time, compare: open_time <= 'HH:MM:SS' AND close_time >= 'HH:MM:SS'
            - operating_hours contains the full schedule text

            Phone Number Queries:
            - phone contains local format (e.g., "012-816 1340")
            - phone_international contains international format (e.g., "+60 12-816 1340")

            Common Query Patterns:
            - "outlets in [location]" → Search name, address, city, state
            - "outlets near [landmark]" → Search name and address
            - "outlets open at [time]" → Compare with open_time and close_time
            - "outlets in [city]" → Search city column (exact or LIKE match)
            - "outlets with [phone]" → Search phone or phone_international

            Always return actual outlet data, not counts, unless specifically asked for counts.
            Limit results to 3 by default unless user asks for more or all.

            Natural Language Query: {query}

            Return ONLY the SQL query, nothing else.
            SQL Query:
            """

    try:
        response = _openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a SQL expert. Generate ONLY SELECT queries. Never generate DELETE, UPDATE, INSERT, DROP, or ALTER queries. Always search across multiple relevant columns for location queries."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0
        )
        
        sql_query = response.choices[0].message.content.strip()
        
        # Clean up the SQL 
        sql_query = sql_query.replace('```sql', '').replace('```', '').strip()
        
        return sql_query
        
    except Exception as e:
        raise Exception(f"Error generating SQL: {str(e)}")

def _validate_sql(sql_query: str) -> bool:
    """Validate that SQL query is safe (only SELECT)"""
    sql_lower = sql_query.lower().strip()
    
    # Check for dangerous operations
    dangerous_keywords = [
        'drop', 'delete', 'update', 'insert', 'alter',
        'create', 'truncate', 'replace', 'exec', 'execute'
    ]
    
    for keyword in dangerous_keywords:
        if keyword in sql_lower:
            return False
    
    # Must start with SELECT
    if not sql_lower.startswith('select'):
        return False
    
    return True

def _execute_sql(sql_query: str) -> Dict[str, Any]:
    """Execute SQL query safely"""
    _initialize()
    
    try:
        # Validate query
        if not _validate_sql(sql_query):
            return {
                'success': False,
                'sql': sql_query,
                'error': 'Invalid query: Only SELECT queries are allowed',
                'results': [],
                'count': 0
            }
        
        # Execute query
        result = _session.execute(text(sql_query))
        rows = result.fetchall()
        columns = result.keys()
        
        # Convert to list of dictionaries
        results = []
        for row in rows:
            row_dict = {}
            for col, value in zip(columns, row):
                row_dict[col] = value
            results.append(row_dict)
        
        return {
            'success': True,
            'sql': sql_query,
            'results': results,
            'count': len(results),
            'columns': list(columns)
        }
        
    except Exception as e:
        return {
            'success': False,
            'sql': sql_query,
            'error': str(e),
            'results': [],
            'count': 0
        }

# Response models
class OutletQueryResponse(BaseModel):
    query: str
    sql: str
    success: bool
    results: List[Dict[str, Any]]
    count: int
    error: Optional[str] = None

class NearestOutletsRequest(BaseModel):
    latitude: float
    longitude: float
    limit: Optional[int] = 3

class NearestOutletsResponse(BaseModel):
    success: bool
    user_location: Dict[str, float]
    results: List[Dict[str, Any]]
    count: int
    error: Optional[str] = None
    
@router.get("/", response_model=OutletQueryResponse)
async def query_outlets(
    query: str = Query(..., description="Natural language query about outlets")
):
    """
    Query ZUS Coffee outlets using natural language.
    The query is automatically converted to SQL and executed.
    
    Examples:
    - "Find all outlets in Kuala Lumpur"
    - "Show me outlets in Cheras"
    - "What outlets are in Petaling Jaya?"
    - "Find outlets near KLCC"
    - "Show me outlets in Selangor"
    - "Which outlets are open at 8 AM?"
    - "Find outlets in Shah Alam"
    - "Show me all outlets with their phone numbers"
    """
    try:
        # Convert natural language to SQL
        sql_query = _text_to_sql(query)
        
        # Execute the SQL
        result = _execute_sql(sql_query)
        
        return OutletQueryResponse(
            query=query,
            sql=result['sql'],
            success=result['success'],
            results=result['results'],
            count=result['count'],
            error=result.get('error')
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/nearest", response_model=NearestOutletsResponse)
async def get_nearest_outlets(request: NearestOutletsRequest):
    """
    Find the nearest ZUS Coffee outlets based on user's GPS coordinates.
    
    You are provided the following request body
    {
        "latitude": 3.1478,
        "longitude": 101.6953,
        "limit": 3 
    }
    """
    try:
        _initialize()
        
        # Get all outlets with coordinates
        query = "SELECT * FROM outlets WHERE latitude IS NOT NULL AND longitude IS NOT NULL"
        result = _session.execute(text(query))
        rows = result.fetchall()
        columns = result.keys()
        
        # Convert to list of dicts and calculate distances
        outlets_with_distance = []
        for row in rows:
            outlet = {}
            for col, value in zip(columns, row):
                outlet[col] = value
            
            # Calculate distance
            distance = calculate_distance(
                request.latitude,
                request.longitude,
                outlet['latitude'],
                outlet['longitude']
            )
            outlet['distance_km'] = distance
            outlets_with_distance.append(outlet)
        
        # Sort by distance and limit results
        sorted_outlets = sorted(outlets_with_distance, key=lambda x: x['distance_km'])
        nearest_outlets = sorted_outlets[:request.limit]
        
        return NearestOutletsResponse(
            success=True,
            user_location={
                "latitude": request.latitude,
                "longitude": request.longitude
            },
            results=nearest_outlets,
            count=len(nearest_outlets)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/schema")
async def get_schema():
    """Get the database schema"""
    try:
        _initialize()
        return {
            "schema": _schema
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health():
    """Health check endpoint"""
    try:
        _initialize()
        # Test query to check database connection
        result = _session.execute(text("SELECT COUNT(*) FROM outlets"))
        count = result.scalar()
        return {
            "status": "healthy",
            "outlets_count": count
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }