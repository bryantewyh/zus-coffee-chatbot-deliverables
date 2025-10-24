"""Tools that the agent can use to perform actions."""

import re
from typing import Dict, Any, List
import requests

class Tool:
    """Base class for tools."""
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the tool and return result."""
        raise NotImplementedError


class CalculatorTool(Tool):
    """Tool for performing calculations."""
    
    def __init__(self):
        super().__init__(
            name="calculator",
            description='Performs mathematical calculations. Use this when user asks for math operations like percentages, sums, differences, etc. Parameter: "expression" (the math expression to evaluate, e.g., "100 * 0.15" for 15% of 100)'
        )
    
    def execute(self, expression: str) -> Dict[str, Any]:
        """Call the calculator API endpoint"""
        try:
            response = requests.post(
                "https://zus-coffee-chatbot-api-702670372085.asia-southeast1.run.app/calculator/",
                json={"expression": expression},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "result": None,
                "message": "The request timed out. Please try again later."
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "result": None,
                "message": "Could not connect to the calculator service."
            }
        except Exception as e:
            return {
                "success": False,
                "result": None,
                "message": "I was unable to help with that request right now. Would you like to explore our products or outlets instead?"
            }


class AskUserTool(Tool):
    """Tool for asking the user for more information."""
    
    def __init__(self):
        super().__init__(
            name="ask_user",
            description="Ask the user for missing information when you don't have enough details to complete the task."
        )
    
    def execute(self, question: str) -> Dict[str, Any]:
        """
        Prepare a question to ask the user.
        
        Args:
            question: The question to ask the user
        
        Returns:
            Dict with the question to be displayed
        """
        return {
            "success": True,
            "result": question,
            "message": "Need user input",
            "requires_input": True
        }

class ProductSearchTool(Tool):
    """Tool for searching ZUS Coffee products."""
    
    def __init__(self):
        super().__init__(
            name="product_search",
            description="Search for ZUS Coffee drinkware products (mugs, tumblers, accessories). Use this when users ask about products, prices, or what's available in the shop."
        )
    
    def execute(self, query: str = None, product_type: str = None, category: str = None, top_k: int = 3, **kwargs) -> Dict[str, Any]:
        """
        Search for products via the FastAPI endpoint.
        """
        import requests
        
        try:
            # Combine query and product_type if both provided
            search_query = query or product_type or category or "drinkware"
            if query and (product_type or category):
                search_query = f"{query} {product_type or category}"
            
            response = requests.get(
                "https://zus-coffee-chatbot-api-702670372085.asia-southeast1.run.app/products",
                params={"query": search_query, "top_k": top_k},
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            
            return {
                "success": True,
                "result": data,
                "message": f"Found {data['count']} products for '{search_query}'"
            }
            
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "result": None,
                "message": "The request timed out. Please try again later."
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "result": None,
                "message": "Could not connect to the product service. It may be temporarily unavailable."
            }
        except requests.exceptions.HTTPError as e:
            return {
                "success": False,
                "result": None,
                "message": "I couldn't process your request right now, please try again later."
            }
        except Exception as e:
            return {
                "success": False,
                "result": None,
                "message": f"Product search failed: {str(e)}"
            }


class OutletQueryTool(Tool):
    """Tool for querying ZUS Coffee outlet information using natural language."""
    
    def __init__(self):
        super().__init__(
            name="outlet_query",
            description=(
                "Query ZUS Coffee outlets using natural language. Use this when users ask about:\n"
                "- Outlet locations (by city, state, area, or landmark)\n"
                "- Opening/closing hours or operating schedules\n"
                "- Contact information (phone numbers)\n"
                "- Addresses and directions\n"
                "- Finding outlets in specific areas (e.g., 'KLCC', 'Cheras', 'Petaling Jaya')\n"
                "- NEAREST or CLOSEST outlets to the user (use the longitude and latitude provided)\n" 
                "Examples: 'outlets in KL', 'find outlets near Sunway', 'outlets open at 8am', 'nearest outlets', 'what's near me'"  
            )
        )

    def _normalize_location_shortforms(self, text: str) -> str:
        """Replace common Malaysian city abbreviations with full names."""
        mappings = {
            r"\bkl\b": "Kuala Lumpur",
            r"\bpj\b": "Petaling Jaya",
            r"\bjb\b": "Johor Bahru",
            r"\bkk\b": "Kota Kinabalu",
            r"\bpg\b": "Penang",
            r"\bkt\b": "Kuala Terengganu",
            r"\bip\b": "Ipoh",
        }
        text = text.lower()
        for short, full in mappings.items():
            text = re.sub(short, full.lower(), text, flags=re.IGNORECASE)
        return text

    def execute(self, query: str = None, location: str = None, latitude: float = None, longitude: float = None, **kwargs) -> Dict[str, Any]:
        """
        Query outlets via the FastAPI endpoints.
        
        Args:
            query: Natural language query about outlets
            location: Optional specific location to search
            latitude: User's GPS latitude (for nearest outlets)
            longitude: User's GPS longitude (for nearest outlets)
            **kwargs: Additional parameters (ignored)
        
        Returns:
            Dict with success status, results, and message
        """
        
        try:
            # Check if this is a "nearest" query with coordinates
            is_nearest_query = False
            if query:
                query_lower = query.lower()
                nearest_keywords = ['nearest', 'closest', 'near me', 'nearby', 'close to me', 'around me']
                is_nearest_query = any(keyword in query_lower for keyword in nearest_keywords)

            if latitude is not None and longitude is not None and not query and not location:
                is_nearest_query = True

            if is_nearest_query and latitude is not None and longitude is not None:
                # Use the nearest outlets endpoint
                response = requests.post(
                    "https://zus-coffee-chatbot-api-702670372085.asia-southeast1.run.app/outlets/nearest",
                    json={
                        "latitude": latitude,
                        "longitude": longitude,
                        "limit": 3
                    },
                    timeout=10
                )
                response.raise_for_status()
                data = response.json()
                
                if not data['success']:
                    return {
                        "success": False,
                        "result": None,
                        "message": "Could not find nearest outlets."
                    }
                
                if data['count'] == 0:
                    return {
                        "success": True,
                        "result": data,
                        "message": "No outlets found nearby."
                    }
                
                return {
                    "success": True,
                    "result": data,
                    "message": f"Found {data['count']} nearest outlet(s)",
                    "is_nearest": True 
                }
            
            # Otherwise, use the regular text-to-SQL query
            search_query = query or ""
            if location:
                search_query = f"{search_query} in {location}".strip() if search_query else f"outlets in {location}"
            
            if not search_query:
                search_query = "show all outlets"
            
            # Clean up and normalize
            search_query = search_query.strip()
            search_query = self._normalize_location_shortforms(search_query)

            response = requests.get(
                "https://zus-coffee-chatbot-api-702670372085.asia-southeast1.run.app/outlets/",
                params={"query": search_query},
                timeout=15
            )
            response.raise_for_status()
            
            data = response.json()
            
            if not data['success']:
                error_msg = data.get('error', 'Unknown error')
                return {
                    "success": False,
                    "result": None,
                    "message": f"{error_msg}",
                    "sql": data.get('sql', '')
                }
            
            if data['count'] == 0:
                return {
                    "success": True,
                    "result": data,
                    "message": "No outlets were found matching your description.",
                    "sql": None  
                }
            
            return {
                "success": True,
                "result": data,
                "message": f"Found {data['count']} outlet(s)",
                "sql": None,
                "is_nearest": False
            }
            
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "result": None,
                "message": "The request timed out. Please try again later."
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "result": None,
                "message": "Could not connect to the outlet service. Try again later. "
            }
        
        except requests.exceptions.HTTPError as e:
            return {
                "success": False,
                "result": None,
                "message": "I couldn't process your request right now, please try again later."
            }
                
        except Exception as e:
            return {
                "success": False,
                "result": None,
                "message": f"Unexpected error occured while searching for your request, please try again later."
            }


# Tool registry
AVAILABLE_TOOLS = {
    "calculator": CalculatorTool(),
    "ask_user": AskUserTool(),
    "product_search": ProductSearchTool(),
    "outlet_query": OutletQueryTool()
}


def get_tool(tool_name: str) -> Tool:
    """Get a tool by name."""
    return AVAILABLE_TOOLS.get(tool_name)


def list_tools() -> List[str]:
    """List all available tools."""
    return list(AVAILABLE_TOOLS.keys())