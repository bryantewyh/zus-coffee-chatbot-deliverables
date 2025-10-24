import sqlite3
import json
from tabulate import tabulate

DB_PATH = "data/outlets/zus_outlets.db"

def view_all_outlets():
    """Display all outlets with all columns"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM outlets ORDER BY id")
    
    rows = cursor.fetchall()
    
    # Get column names
    column_names = [description[0] for description in cursor.description]
    
    print("\n" + "=" * 150)
    print("ALL ZUS COFFEE OUTLETS")
    print("=" * 150)
    print(tabulate(rows, headers=column_names, tablefmt="grid"))
    print(f"\nTotal: {len(rows)} outlets")
    
    conn.close()

def view_outlet_details(outlet_id=None):
    """Display detailed information for specific outlet(s)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if outlet_id:
        cursor.execute("SELECT * FROM outlets WHERE id = ?", (outlet_id,))
        outlets = [cursor.fetchone()]
    else:
        cursor.execute("SELECT * FROM outlets LIMIT 5")
        outlets = cursor.fetchall()
    
    # Get column names
    column_names = [description[0] for description in cursor.description]
    
    for outlet in outlets:
        if outlet:
            print("\n" + "=" * 80)
            print(f"OUTLET DETAILS (ID: {outlet[0]})")
            print("=" * 80)
            
            for col_name, value in zip(column_names, outlet):
                print(f"{col_name:25s}: {value}")
            print("=" * 80)
    
    conn.close()

def view_summary():
    """Show database summary statistics"""
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
        LIMIT 10
    """)
    top_cities = cursor.fetchall()
    
    # Top states
    cursor.execute("""
        SELECT state, COUNT(*) as count 
        FROM outlets 
        WHERE state IS NOT NULL 
        GROUP BY state 
        ORDER BY count DESC
    """)
    top_states = cursor.fetchall()
    
    conn.close()
    
    print("\n" + "=" * 70)
    print("  ZUS COFFEE OUTLETS DATABASE SUMMARY")
    print("=" * 70)
    print(f"Total Outlets: {total}")
    print(f"Operational: {operational}")
    print(f"Unique Cities: {cities}")
    print(f"Unique States: {states}")
    
    print("\n" + "-" * 70)
    print("TOP CITIES:")
    print("-" * 70)
    print(tabulate(top_cities, headers=["City", "Count"], tablefmt="simple"))
    
    print("\n" + "-" * 70)
    print("OUTLETS BY STATE:")
    print("-" * 70)
    print(tabulate(top_states, headers=["State", "Count"], tablefmt="simple"))
    print("=" * 70)

def search_outlets(query):
    """Search outlets by name or address"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM outlets
        WHERE name LIKE ? OR address LIKE ? OR city LIKE ?
        ORDER BY name
    """, (f'%{query}%', f'%{query}%', f'%{query}%'))
    
    rows = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    
    print("\n" + "=" * 150)
    print(f"SEARCH RESULTS FOR: '{query}'")
    print("=" * 150)
    
    if rows:
        print(tabulate(rows, headers=column_names, tablefmt="grid"))
        print(f"\nFound {len(rows)} outlets")
    else:
        print("No results found")
    
    conn.close()

def export_to_json(output_file="outlets_export.json"):
    """Export database to JSON"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM outlets")
    rows = cursor.fetchall()
    
    outlets = []
    for row in rows:
        outlets.append(dict(row))
    
    with open(output_file, 'w', encoding='utf8') as f:
        json.dump(outlets, f, ensure_ascii=False, indent=2)
    
    print(f"\nExported {len(outlets)} outlets to {output_file}")
    
    conn.close()

def main():
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "all":
            view_all_outlets()
        elif command == "details":
            outlet_id = int(sys.argv[2]) if len(sys.argv) > 2 else None
            view_outlet_details(outlet_id)
        elif command == "summary":
            view_summary()
        elif command == "search":
            if len(sys.argv) > 2:
                search_outlets(sys.argv[2])
            else:
                print("Usage: python view_database.py search <query>")
        elif command == "export":
            output = sys.argv[2] if len(sys.argv) > 2 else "outlets_export.json"
            export_to_json(output)
        else:
            print("Unknown command")
    else:
        # Show summary and sample details
        print("\n" + "=" * 80)
        print("ZUS COFFEE OUTLETS DATABASE VIEWER")
        print("=" * 80)
        print("\nUsage:")
        print("  python view_database.py all              - View all outlets (table)")
        print("  python view_database.py details [id]     - View detailed info (first 5 or specific ID)")
        print("  python view_database.py summary          - Show summary statistics")
        print("  python view_database.py search <query>   - Search outlets")
        print("  python view_database.py export [file]    - Export to JSON")
        print("\nExamples:")
        print("  python view_database.py details 1")
        print("  python view_database.py search Cheras")
        print("  python view_database.py export my_outlets.json")
        print("=" * 80)
        
        # Show quick preview
        view_summary()
        print("\nShowing first 5 outlets:")
        view_outlet_details()

if __name__ == "__main__":
    main()