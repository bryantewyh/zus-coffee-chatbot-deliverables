import sqlite3
import json
import os
import re
from pathlib import Path

# Configuration
INPUT_JSON = "zus_places_full.json"
DB_PATH = "data/outlets/zus_outlets.db"

def parse_operating_hours(hours_str):
    """
    Parse operating hours string to extract open/close times
    Returns: (open_time, close_time, is_24_hours)
    """
    if not hours_str:
        return None, None, False
    
    # Check for 24 hours
    if "24" in hours_str.lower() or "24/7" in hours_str.lower():
        return "00:00:00", "23:59:59", True
    
    # Try to extract first day's hours 
    # Format: "Monday: 8:00 AM – 9:40 PM; Tuesday: ..."
    match = re.search(r'(\d{1,2}):(\d{2})\s*(AM|PM|am|pm)\s*[-–]\s*(\d{1,2}):(\d{2})\s*(AM|PM|am|pm)', hours_str)
    
    if match:
        open_hour = int(match.group(1))
        open_min = match.group(2)
        open_period = match.group(3).upper()
        close_hour = int(match.group(4))
        close_min = match.group(5)
        close_period = match.group(6).upper()
        
        # Convert to 24-hour format
        if open_period == "PM" and open_hour != 12:
            open_hour += 12
        elif open_period == "AM" and open_hour == 12:
            open_hour = 0
            
        if close_period == "PM" and close_hour != 12:
            close_hour += 12
        elif close_period == "AM" and close_hour == 12:
            close_hour = 0
        
        open_time = f"{open_hour:02d}:{open_min}:00"
        close_time = f"{close_hour:02d}:{close_min}:00"
        
        return open_time, close_time, False
    
    return None, None, False

def extract_city_state(address_google):
    """
    Extract city and state from Google's formatted address
    Format: "address, postcode City, State, Country"
    """
    if not address_google:
        return None, None, None
    
    # Try to extract postcode
    postcode_match = re.search(r'\b(\d{5})\b', address_google)
    postcode = postcode_match.group(1) if postcode_match else None
    
    states = [
        'Selangor', 'Kuala Lumpur', 'Wilayah Persekutuan Kuala Lumpur',
        'Federal Territory of Kuala Lumpur', 'Putrajaya', 
        'Wilayah Persekutuan Putrajaya', 'Johor', 'Penang', 'Perak',
        'Kedah', 'Kelantan', 'Terengganu', 'Pahang', 'Negeri Sembilan',
        'Melaka', 'Sabah', 'Sarawak', 'Perlis', 'Labuan'
    ]
    
    state = None
    for s in states:
        if s in address_google:
            state = s
            # Normalize state names
            if 'Wilayah Persekutuan Kuala Lumpur' in state or 'Federal Territory of Kuala Lumpur' in state:
                state = 'Kuala Lumpur'
            elif 'Wilayah Persekutuan Putrajaya' in state:
                state = 'Putrajaya'
            break
    
    # Extract city after postcode and before state
    city = None
    if postcode and state:
        pattern = rf'{postcode}\s+([^,]+),\s*{re.escape(state)}'
        city_match = re.search(pattern, address_google)
        if city_match:
            city = city_match.group(1).strip()
    
    if not city:
        cities = [
            'Shah Alam', 'Petaling Jaya', 'Kuala Lumpur', 'Subang Jaya',
            'Ampang', 'Cheras', 'Puchong', 'Klang', 'Putrajaya', 'Cyberjaya',
            'Kajang', 'Sepang', 'Bangi', 'Seri Kembangan', 'Rawang',
            'Selayang', 'Gombak', 'Sentul', 'Wangsa Maju', 'Setapak'
        ]
        for c in cities:
            if c in address_google:
                city = c
                break
    
    return city, state, postcode

def init_database():
    """Create fresh database with schema"""
    os.makedirs('data/outlets', exist_ok=True)
    
    # Remove existing database if it exists
    if os.path.exists(DB_PATH):
        print(f"Removing existing database: {DB_PATH}")
        os.remove(DB_PATH)
    
    print(f"Creating new database: {DB_PATH}")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS outlets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            city TEXT,
            state TEXT,
            postcode TEXT,
            latitude REAL,
            longitude REAL,
            phone TEXT,
            phone_international TEXT,
            operating_hours TEXT,
            open_time TIME,
            close_time TIME,
            business_status TEXT
        )
    """)
    
    print("Created outlets table")
    
    # Create indexes
    cursor.execute("CREATE INDEX idx_city ON outlets(city)")
    cursor.execute("CREATE INDEX idx_state ON outlets(state)")
    cursor.execute("CREATE INDEX idx_business_status ON outlets(business_status)")
    
    print("Created indexes")
    
    conn.commit()
    conn.close()

def ingest_data():
    """Read JSON and insert into database"""
    
    # Check if input file exists
    if not os.path.exists(INPUT_JSON):
        print(f"ERROR: Input file not found: {INPUT_JSON}")
        return
    
    # Read JSON data
    print(f"\nReading data from: {INPUT_JSON}")
    with open(INPUT_JSON, 'r', encoding='utf8') as f:
        data = json.load(f)
    
    print(f"Found {len(data)} outlets in JSON")
    
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    inserted = 0
    skipped = 0
    
    for idx, outlet in enumerate(data, 1):
        # Skip if no place_id (means API failed)
        if not outlet.get('place_id'):
            print(f"[{idx}/{len(data)}] Skipping: {outlet.get('name_list')} - No place_id")
            skipped += 1
            continue
        
        # Extract data
        name = outlet.get('name_google') or outlet.get('name_list')
        address = outlet.get('address_google') or outlet.get('address_list')
        phone_local = outlet.get('phone_local')
        phone_intl = outlet.get('phone_international')
        lat = outlet.get('lat')
        lng = outlet.get('lng')
        hours = outlet.get('opening_hours')
        business_status = outlet.get('business_status')
        place_id = outlet.get('place_id')
        
        # Parse operating hours
        open_time, close_time, is_24_hours = parse_operating_hours(hours)
        
        # Extract city, state, postcode
        city, state, postcode = extract_city_state(address)
        
        try:
            cursor.execute("""
                INSERT INTO outlets (
                    name, address, city, state, postcode, latitude, longitude,
                    phone, phone_international, operating_hours, open_time, close_time,
                    business_status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                name, address, city, state, postcode, lat, lng,
                phone_local, phone_intl, hours, open_time, close_time,
                business_status
            ))
            
            print(f"[{idx}/{len(data)}] Inserted: {name}")
            inserted += 1
            
        except sqlite3.IntegrityError as e:
            print(f"[{idx}/{len(data)}] Error: {name} - {e}")
            skipped += 1
        except Exception as e:
            print(f"[{idx}/{len(data)}] Error inserting {name}: {e}")
            skipped += 1
    
    conn.commit()
    conn.close()
    
    return inserted, skipped

def show_summary():
    """Display database summary"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM outlets")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT city) FROM outlets WHERE city IS NOT NULL")
    cities = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT state) FROM outlets WHERE state IS NOT NULL")
    states = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM outlets WHERE business_status = 'OPERATIONAL'")
    operational = cursor.fetchone()[0]
    
    # Top cities
    cursor.execute("""
        SELECT city, COUNT(*) as count 
        FROM outlets 
        WHERE city IS NOT NULL 
        GROUP BY city 
        ORDER BY count DESC 
        LIMIT 5
    """)
    top_cities = cursor.fetchall()
    
    conn.close()
    
    print("\n" + "=" * 70)
    print("  ZUS COFFEE OUTLETS DATABASE SUMMARY")
    print("=" * 70)
    print(f"Total Outlets: {total}")
    print(f"Operational: {operational}")
    print(f"Cities: {cities}")
    print(f"States: {states}")
    print("\nTop Cities:")
    for city, count in top_cities:
        print(f"  - {city}: {count} outlets")
    print("=" * 70)

def main():
    print("ZUS Coffee Outlets Database Ingestion")
    print("=" * 70)
    
    # Step 1: Initialize database
    init_database()
    
    # Step 2: Ingest data
    inserted, skipped = ingest_data()
    
    # Step 3: Show summary
    print("\n" + "=" * 70)
    print("  INGESTION COMPLETE")
    print("=" * 70)
    print(f"Inserted: {inserted}")
    print(f"Skipped: {skipped}")
    print("=" * 70)
    
    show_summary()
    
    print(f"\nDatabase ready at: {DB_PATH}")

if __name__ == "__main__":
    main()