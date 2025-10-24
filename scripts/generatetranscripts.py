import requests
import json
from datetime import datetime
import sys

BASE_URL = "https://zus-coffee-chatbot-api-702670372085.asia-southeast1.run.app"

class TranscriptGenerator:
    def __init__(self):
        self.output = []
        
    def add_header(self, text, level=1):
        """Add markdown header"""
        self.output.append(f"\n{'#' * level} {text}\n")
    
    def add_text(self, text):
        """Add regular text"""
        self.output.append(f"{text}\n")
    
    def test_endpoint(self, endpoint, params, description, expected_status="success"):
        """Test an endpoint and capture the transcript"""
        self.add_header(description, level=3)
        
        # Build request URL
        param_str = "&".join([f"{k}={v}" for k, v in params.items()])
        full_url = f"{BASE_URL}{endpoint}?{param_str}"
        
        self.add_text(f"**Request:**")
        self.add_text(f"```\nGET {endpoint}?{param_str}\n```")
        
        try:
            # Make the actual API call
            response = requests.get(full_url, timeout=10)
            
            # Capture response
            self.add_text(f"\n**Response Status:** {response.status_code}")
            self.add_text(f"\n**Response Body:**")
            self.add_text(f"```json\n{json.dumps(response.json(), indent=2, ensure_ascii=False)}\n```")
            
            # Determine status
            if response.status_code == 200:
                data = response.json()
                if endpoint == "/products":
                    count = data.get('count', 0)
                    status = f"Success - Found {count} product(s)"
                elif endpoint == "/outlets":
                    count = data.get('count', 0)
                    success = data.get('success', False)
                    if success:
                        status = f"Success - Found {count} outlet(s)"
                    else:
                        error = data.get('error', 'Unknown error')
                        status = f"Failed - {error}"
                else:
                    status = "Success"
            else:
                status = f"Failed - HTTP {response.status_code}"
            
            self.add_text(f"\n**Status:** {status}\n")
            self.add_text("---\n")
            
            return response.status_code == 200
            
        except requests.exceptions.ConnectionError:
            self.add_text(f"\n**Error:** Could not connect to {BASE_URL}")
            self.add_text(f"**Status:** Server not running\n")
            self.add_text("---\n")
            return False
        except Exception as e:
            self.add_text(f"\n**Error:** {str(e)}")
            self.add_text("---\n")
            return False
        
    def test_post_endpoint(self, endpoint, body, description):
        """Test a POST endpoint and capture the transcript"""
        self.add_header(description, level=3)
        
        full_url = f"{BASE_URL}{endpoint}"
        
        self.add_text(f"**Request:**")
        self.add_text(f"```\nPOST {endpoint}\n```")
        self.add_text(f"\n**Request Body:**")
        self.add_text(f"```json\n{json.dumps(body, indent=2)}\n```")
        
        try:
            # Make the actual API call
            response = requests.post(full_url, json=body, timeout=10)
            
            # Capture response
            self.add_text(f"\n**Response Status:** {response.status_code}")
            self.add_text(f"\n**Response Body:**")
            self.add_text(f"```json\n{json.dumps(response.json(), indent=2, ensure_ascii=False)}\n```")
            
            # Determine status
            if response.status_code == 200:
                data = response.json()
                
                # Calculator
                if endpoint == "/calculator/":
                    success = data.get('success', False)
                    if success:
                        result = data.get('result')
                        status = f"Success - Result: {result}"
                    else:
                        message = data.get('message', 'Unknown error')
                        status = f"Failed - {message}"
                # Nearest outlets logic
                else:
                    success = data.get('success', False)
                    count = data.get('count', 0)
                    if success:
                        status = f"Success - Found {count} nearest outlet(s)"
                    else:
                        error = data.get('error', 'Unknown error')
                        status = f"Failed - {error}"
            else:
                status = f"Failed - HTTP {response.status_code}"
            
            self.add_text(f"\n**Status:** {status}\n")
            self.add_text("---\n")
            
            return response.status_code == 200
            
        except requests.exceptions.ConnectionError:
            self.add_text(f"\n**Error:** Could not connect to {BASE_URL}")
            self.add_text(f"**Status:** Server not running\n")
            self.add_text("---\n")
            return False
        except Exception as e:
            self.add_text(f"\n**Error:** {str(e)}")
            self.add_text("---\n")
            return False    
        
    def generate(self):
        """Generate all transcripts"""
        
        # Header
        self.add_header("ZUS Coffee API - Real Transcripts", level=1)
        self.add_text(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        self.add_text("These are real API responses captured from the running server.\n")
        
        # Products Endpoint Tests
        self.add_header("Products Endpoint (`/products`)", level=2)
        self.add_header("Success Cases", level=3)
        
        self.test_endpoint(
            "/products",
            {"query": "mug", "top_k": 3},
            "Example 1: Search for Mugs"
        )
        
        self.test_endpoint(
            "/products",
            {"query": "tumbler", "top_k": 5},
            "Example 2: Search for Tumblers"
        )
        
        self.test_endpoint(
            "/products",
            {"query": "reusable straw", "top_k": 3},
            "Example 3: Search for Reusable Straws"
        )
        
        self.test_endpoint(
            "/products",
            {"query": "bottle", "top_k": 2},
            "Example 4: Search for Bottles"
        )
        
        # Products Failure Cases
        self.add_header("Failure Cases", level=3)
        
        self.test_endpoint(
            "/products",
            {"query": "coffee beans", "top_k": 3},
            "Example 1: No Results Found (Product Not in Drinkware)"
        )
        
        self.test_endpoint(
            "/products",
            {"query": "mug", "top_k": 100},
            "Example 2: Invalid top_k Parameter"
        )
        # Calculator Endpoint Tests
        self.add_header("Calculator Endpoint (`/calculator`)", level=2)
        self.add_header("Success Cases", level=3)

        self.test_post_endpoint(
            "/calculator/",
            {"expression": "100 * 0.15"},
            "Example 1: Calculate 15% of 100"
        )

        self.test_post_endpoint(
            "/calculator/",
            {"expression": "250 + 50"},
            "Example 2: Simple Addition"
        )

        self.test_post_endpoint(
            "/calculator/",
            {"expression": "(100 + 50) * 2"},
            "Example 3: Complex Expression"
        )

        self.test_post_endpoint(
            "/calculator/",
            {"expression": "1000 / 4"},
            "Example 4: Division"
        )

        # Calculator Failure Cases
        self.add_header("Failure Cases", level=3)

        self.test_post_endpoint(
            "/calculator/",
            {"expression": "invalid expression"},
            "Example 1: Invalid Expression"
        )

        self.test_post_endpoint(
            "/calculator/",
            {"expression": "10 / 0"},
            "Example 2: Division by Zero"
        )        
        
        # Outlets Endpoint Tests
        self.add_header("Outlets Endpoint (`/outlets`)", level=2)
        self.add_header("Success Cases", level=3)
        
        self.test_endpoint(
            "/outlets",
            {"query": "outlets in Kuala Lumpur"},
            "Example 1: Find Outlets by Location"
        )
        
        self.test_endpoint(
            "/outlets",
            {"query": "which outlets have drive thru"},
            "Example 2: Find Outlets with Drive-Thru"
        )
        
        self.test_endpoint(
            "/outlets",
            {"query": "outlets with wifi in Petaling Jaya"},
            "Example 3: Find Outlets with WiFi in Specific Area"
        )
        
        self.test_endpoint(
            "/outlets",
            {"query": "what time does ZUS Coffee KLCC open"},
            "Example 4: Check Operating Hours"
        )
        
        self.test_endpoint(
            "/outlets",
            {"query": "show me all outlets"},
            "Example 5: List All Outlets"
        )
        
        # Outlets Failure Cases
        self.add_header("Failure Cases", level=3)
        
        self.test_endpoint(
            "/outlets",
            {"query": "delete all outlets"},
            "Example 1: Dangerous SQL Attempt (Should be Blocked)"
        )
        
        self.test_endpoint(
            "/outlets",
            {"query": "asdfghjkl random nonsense"},
            "Example 2: Nonsense Query (Should Return No Results)"
        )

        # Nearest Outlet
        self.add_header("Nearest Outlets Endpoint (`/outlets/nearest`)", level=2)
        self.add_header("Success Cases", level=3)

        self.test_post_endpoint(
            "/outlets/nearest",
            {
                "latitude": 3.1478,
                "longitude": 101.6953,
                "limit": 3
            },
            "Example 1: Find 3 Nearest Outlets (Petaling Jaya Area)"
        )

        self.add_header("Failure Cases", level=3)

        self.test_post_endpoint(
            "/outlets/nearest",
            {
                "latitude": 999,
                "longitude": 999,
                "limit": 3
            },
            "Example 1: Invalid Coordinates"
        )

        self.test_post_endpoint(
            "/outlets/nearest",
            {
                "latitude": 3.1478,
                "longitude": 101.6953
                # Missing limit should use default
            },
            "Example 2: Missing Limit Parameter"
        )        
        # Health Checks
        self.add_header("Health Checks", level=2)
        
        self.test_endpoint(
            "/products/health",
            {},
            "Products Health Check"
        )
        self.test_endpoint(
            "/calculator/health",
            {},
            "Calculator Health Check"
        )
        self.test_endpoint(
            "/outlets/health",
            {},
            "Outlets Health Check"
        )
        
        # Summary
        self.add_header("Summary", level=2)
        self.add_text("All transcripts captured from live API responses.")
        self.add_text(f"Server: {BASE_URL}")
        self.add_text(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return "\n".join(self.output)
    
    def save_to_file(self, filename="examples/transcripts.md"):
        """Save transcripts to file"""
        import os
        
        content = self.generate()
        
        # Create directory if it doesn't exist
        directory = os.path.dirname(filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            print(f" Created directory: {directory}")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f" Real transcripts saved to {filename}")

if __name__ == "__main__":
    print("=" * 60)
    print("Transcript generation for ZUS API")
    print("=" * 60)
    try:
        # Quick server check
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        if response.status_code == 200:
            print(" Server is running")
            print()
            
            generator = TranscriptGenerator()
            generator.save_to_file()
            
            print()
            print("Done! Check examples/transcripts.md")
        else:
            print("Server responded but with unexpected status")
            sys.exit(1)
            
    except requests.exceptions.ConnectionError:
        print("Could not connect to server")
        print()
        sys.exit(1)