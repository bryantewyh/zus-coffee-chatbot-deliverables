import requests, time, json, csv, re
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

INPUT_FILE = "zus_maps_links.json"
OUT_JSON = "zus_places_full.json"
OUT_CSV = "zus_places_full.csv"

FIND_PLACE_URL = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json"
API_KEY = os.getenv("GOOGLE_API_KEY")

HEADERS = {"User-Agent":"MyScript/1.0"}

def extract_place_id_from_url(maps_url):
    """
    Extract place_id or CID from Google Maps URL by parsing the URL string.
    NOTE: This does NOT fetch/scrape the URL - it only parses the text string.
    """
    # Pattern 1: Look for !1s followed by place_id (ChIJ format)
    match = re.search(r'!1s(ChIJ[A-Za-z0-9_-]+)', maps_url)
    if match:
        return match.group(1)
    
    # Pattern 2: Look for CID format (0x...:0x...)
    match = re.search(r'!1s(0x[a-f0-9]+:0x[a-f0-9]+)', maps_url)
    if match:
        cid = match.group(1)
        return cid
    
    # Pattern 3: Look for place name in URL path and use coordinates
    match = re.search(r'/place/([^/]+)/@(-?\d+\.\d+),(-?\d+\.\d+)', maps_url)
    if match:
        lat, lng = match.group(2), match.group(3)
        return f"coords:{lat},{lng}"
    
    return None

def find_place_by_coords(lat, lng, name_hint=""):
    """
    Find place using coordinates via Google Places API (official API, not scraping).
    Uses the Find Place from Text endpoint with location bias.
    """
    query = f"{name_hint}" if name_hint else "ZUS Coffee"
    params = {
        "input": query,
        "inputtype": "textquery",
        "fields": "place_id,formatted_address,name,geometry",
        "locationbias": f"circle:50@{lat},{lng}",
        "key": API_KEY,
    }
    print(f"    API Query: {query}")
    print(f"    Location: {lat}, {lng}")
    r = requests.get(FIND_PLACE_URL, params=params, headers=HEADERS, timeout=20)
    r.raise_for_status()
    data = r.json()
    
    print(f"    API Status: {data.get('status')}")
    if data.get("status") == "OK" and data.get("candidates"):
        print(f"    Found {len(data.get('candidates'))} candidates")
        return data["candidates"][0].get("place_id")
    elif data.get("status") == "ZERO_RESULTS":
        print(f"    No results found for this query")
    else:
        print(f"    API Error: {data.get('error_message', 'Unknown error')}")
    
    return None

def get_place_details(place_id):
    """
    Fetch detailed place information using Google Places API (official API, not scraping).
    Uses the Place Details endpoint.
    """
    params = {
        "place_id": place_id,
        "fields": "place_id,name,formatted_address,formatted_phone_number,international_phone_number,opening_hours,geometry,website,rating,user_ratings_total,business_status",
        "key": API_KEY
    }
    r = requests.get(DETAILS_URL, params=params, headers=HEADERS, timeout=20)
    r.raise_for_status()
    data = r.json()
    
    if data.get("status") == "OK":
        return data["result"]
    else:
        print(f"    API returned status: {data.get('status')}")
    
    return None

def main():
    if not API_KEY:
        print("ERROR: GOOGLE_API_KEY not found in environment variables")
        return
    
    data_path = Path(INPUT_FILE)
    if not data_path.exists():
        print(f"Input file not found: {INPUT_FILE}")
        return

    entries = json.loads(data_path.read_text(encoding="utf8"))
    
    results = []
    success_count = 0

    for idx, e in enumerate(entries, 1):
        name = e.get("name") or ""
        address = e.get("address_snippet") or ""
        maps_url = e.get("maps_url_resolved") or e.get("maps_href") or ""
        
        print(f"\n[{idx}/{len(entries)}] Processing: {name}")
        
        place_id = None
        details = None
        
        # Extract place_id from the Google Maps URL
        if maps_url:
            print(f"  → Extracting identifier from URL...")
            extracted_id = extract_place_id_from_url(maps_url)
            
            if extracted_id:
                print(f"Extracted identifier: {extracted_id[:50]}...")
                
                # If we got coordinates, use them to find place_id
                if extracted_id.startswith("coords:"):
                    coords = extracted_id.replace("coords:", "").split(",")
                    lat, lng = coords[0], coords[1]
                    print(f"  → Using coordinates to find place_id...")
                    try:
                        place_id = find_place_by_coords(lat, lng, name)
                        if place_id:
                            print(f"Found place_id via coords: {place_id}")
                    except Exception as ex:
                        print(f"Coordinate lookup error: {ex}")
                        place_id = None
                
                # If it's a CID, we need to convert or search
                elif extracted_id.startswith("0x"):
                    print(f"  → CID format detected, searching by name and location...")
                    coord_match = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)', maps_url)
                    if coord_match:
                        lat, lng = coord_match.group(1), coord_match.group(2)
                        try:
                            place_id = find_place_by_coords(lat, lng, name)
                            if place_id:
                                print(f"Found place_id: {place_id}")
                        except Exception as ex:
                            print(f"Lookup error: {ex}")
                            place_id = None
                    else:
                        print(f"Could not extract coordinates from URL")
                        place_id = None
                
                else:
                    # It's already a proper place_id
                    place_id = extracted_id
                    print(f"Using extracted place_id: {place_id}")
            
            else:
                print(f"Could not extract identifier from URL")
            
            # Use the place_id to get details from Google Places API
            if place_id:
                try:
                    print(f"  → Fetching details from Places API...")
                    details = get_place_details(place_id)
                    
                    if details:
                        print(f"Retrieved details successfully")
                        print(f"    - Name: {details.get('name')}")
                        print(f"    - Phone: {details.get('formatted_phone_number', 'N/A')}")
                        print(f"    - Rating: {details.get('rating', 'N/A')}")
                        success_count += 1
                    else:
                        print(f"Failed to get details from API")
                
                except Exception as ex:
                    print(f"API error: {ex}")
            else:
                print(f"No valid place_id found")
        
        else:
            print(f"No maps URL available")
        
        # Compile result
        geom = details.get("geometry", {}).get("location", {}) if details else {}
        opening_hours = details.get("opening_hours", {}) if details else {}
        opening = "; ".join(opening_hours.get("weekday_text", [])) if opening_hours else ""
        
        combined = {
            "name_list": name,
            "address_list": address,
            "maps_url": maps_url,
            "place_id": place_id,
            "name_google": details.get("name") if details else None,
            "address_google": details.get("formatted_address") if details else None,
            "phone_local": details.get("formatted_phone_number") if details else None,
            "phone_international": details.get("international_phone_number") if details else None,
            "lat": geom.get("lat"),
            "lng": geom.get("lng"),
            "opening_hours": opening,
            "rating": details.get("rating") if details else None,
            "total_ratings": details.get("user_ratings_total") if details else None,
            "website": details.get("website") if details else None,
            "business_status": details.get("business_status") if details else None,
        }
        results.append(combined)
        
        # Polite pause to avoid rate limits
        time.sleep(0.5)

    # Save outputs
    print(f"\n{'='*60}")
    print(f"Processing complete: {success_count}/{len(entries)} places found")
    print(f"{'='*60}\n")
    
    with open(OUT_JSON, "w", encoding="utf8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # CSV flatten
    with open(OUT_CSV, "w", newline="", encoding="utf8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "name_list", "address_list", "maps_url", "place_id", 
            "name_google", "address_google", "phone_local", 
            "phone_international", "lat", "lng", "opening_hours",
            "rating", "total_ratings", "website", "business_status"
        ])
        
        for r in results:
            writer.writerow([
                r.get("name_list"),
                r.get("address_list"),
                r.get("maps_url"),
                r.get("place_id"),
                r.get("name_google"),
                r.get("address_google"),
                r.get("phone_local"),
                r.get("phone_international"),
                r.get("lat"),
                r.get("lng"),
                r.get("opening_hours"),
                r.get("rating"),
                r.get("total_ratings"),
                r.get("website"),
                r.get("business_status")
            ])
    
    print(f"Saved details to {OUT_JSON} and {OUT_CSV}")

if __name__ == "__main__":
    main()