import requests
from bs4 import BeautifulSoup
import json
import os
import time

def scrape_zus_drinkware():
    """Scrape drinkware products from ZUS Coffee shop"""
    url = "https://shop.zuscoffee.com/collections/all?filter.p.product_type=Drinkware+Accessories&filter.p.product_type=Mugs&filter.p.product_type=Tumbler"
    
    print(f"Fetching drinkware from filtered URL...")
    
    products = []
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        print(f"Status Code: {response.status_code}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for product cards
        product_cards = soup.find_all('product-card')
        
        if not product_cards:
            product_cards = soup.find_all('div', class_=lambda x: x and 'product-card' in str(x))
        
        print(f"\n=== Found {len(product_cards)} product cards ===\n")
        
        for card in product_cards:
            try:
                # Extract category
                category_elem = card.find('span', class_='product-card__category')
                category = category_elem.get_text(strip=True) if category_elem else "Drinkware"
                
                # Extract product name
                name_elem = card.find('h3', class_='product-card__title')
                if not name_elem:
                    name_elem = card.find('a', class_='product-card__title')
                if not name_elem:
                    name_elem = card.find(class_=lambda x: x and 'title' in str(x).lower())
                name = name_elem.get_text(strip=True) if name_elem else "Unknown"
                
                # Extract price using the custom sale-price element
                price_elem = card.find('sale-price')
                if not price_elem:
                    price_elem = card.find('span', class_='price')
                if not price_elem:
                    price_elem = card.find(class_=lambda x: x and 'price' in str(x).lower())
                
                price = "N/A"
                if price_elem:
                    price_text = price_elem.get_text(strip=True)
                    # Remove sale price prefix if present
                    price_text = price_text.replace('Sale price', '').replace('sale price', '').strip()
                    # Also handle regular price or other prefixes
                    price_text = price_text.replace('Regular price', '').replace('regular price', '').strip()
                    price = price_text if price_text else "N/A"
                
                # Extract product URL
                link_elem = card.find('a', href=True)
                product_url = link_elem.get('href', '') if link_elem else ""
                if product_url and not product_url.startswith('http'):
                    product_url = 'https://shop.zuscoffee.com' + product_url
                
                
                # Extract image URL
                img_elem = card.find('img')
                image_url = img_elem.get('src', '') if img_elem else ""
                if image_url and image_url.startswith('//'):
                    image_url = 'https:' + image_url
                
                product = {
                    'name': name,
                    'category': category,
                    'price': price,
                    'url': product_url,
                    'image_url': image_url
                }
                
                products.append(product)
                print(f"{category}: {name} - {price}")
                
            except Exception as e:
                print(f"Error parsing product card: {e}")
                continue
        
        return products
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {e}")
        return []
    except Exception as e:
        print(f"Error scraping: {e}")
        return []

def scrape_product_details(product_url):
    """Scrape detailed information from individual product page"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(product_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract detailed description
        desc_elem = soup.find('div', class_=lambda x: x and 'description' in str(x).lower())
        description = desc_elem.get_text(strip=True) if desc_elem else ""
        
        # Extract specifications/features
        specs = []
        spec_items = soup.find_all(['li', 'p'], class_=lambda x: x and ('feature' in str(x).lower() or 'spec' in str(x).lower()))
        for item in spec_items:
            specs.append(item.get_text(strip=True))
        
        return {
            'detailed_description': description
        }
        
    except Exception as e:
        print(f"Error scraping product details: {e}")
        return {}

if __name__ == "__main__":
    # Create directory if it doesn't exist
    os.makedirs('data/products', exist_ok=True)
    
    print("Starting ZUS Coffee Drinkware Scraper")
    print("=" * 50)
    
    products = scrape_zus_drinkware()
    
    if products:
        # Optionally scrape detailed info for each product
        print("\n" + "=" * 50)
        print("Fetching detailed product information...")
        print("=" * 50 + "\n")
        
        for i, product in enumerate(products):
            if product.get('url'):
                print(f"Fetching details for: {product['name']}")
                details = scrape_product_details(product['url'])
                product.update(details)

                time.sleep(1)
        
        # Save to JSON
        output_file = 'data/products/drinkware.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(products, f, indent=2, ensure_ascii=False)
        
        print(f"\n Scraped {len(products)} products")
        print(f" Saved to {output_file}")
        
        # Display sample
        if products:
            print("\n" + "=" * 50)
            print("Sample Product:")
            print("=" * 50)
            print(json.dumps(products[0], indent=2, ensure_ascii=False))
    else:
        print("\nNo products scraped yet - need to adjust selectors")