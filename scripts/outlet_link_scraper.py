"""Scrape zus map links"""
import requests, time, json, csv
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE = "https://zuscoffee.com"
LISTING_BASE = "https://zuscoffee.com/category/store/kuala-lumpur-selangor/"
TOTAL_PAGES = 22
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) MyScraper/1.0 (+https://example.com/contact)"

HEADERS = {"User-Agent": USER_AGENT}
# Dont overload
SLEEP_BETWEEN_REQUESTS = 0.8  

def fetch(url, allow_redirects=True, timeout=20):
    resp = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=allow_redirects)
    resp.raise_for_status()
    return resp

def get_listing_page_html(page_num):
    if page_num <= 1:
        url = LISTING_BASE
    else:
        url = urljoin(BASE, f"/category/store/kuala-lumpur-selangor/page/{page_num}/")
    r = fetch(url)
    return r.text, r.url

def extract_items_from_html(html, page_url):
    soup = BeautifulSoup(html, "html.parser")
    items = []

    # For each 'Direction' anchor on the page we saw "Direction maps.app.goo.gl"
    # Find <a> elements that contain 'maps.app.goo.gl' OR 'google.com/maps' in href
    anchors = soup.select("a[href*='maps.app.goo.gl'], a[href*='google.com/maps'], a[href*='maps.google.com']")
    seen = set()
    for a in anchors:
        href = a.get("href")
        if not href:
            continue
        # Find nearby title / address text: search up to two parent levels
        title = None
        address = None
        # Try to find the name that you gave: <p class="elementor-heading-title elementor-size-default">
        # Find the closest such element
        t = a.find_previous("p", class_="elementor-heading-title")
        if not t:
            # if not then find previous h2/h3
            t = a.find_previous(["h2","h3","p"])
        if t:
            title = t.get_text(strip=True)

        # Address inside div.elementor-widget-container > p
        addr = a.find_previous("div", class_="elementor-widget-container")
        if addr:
            p = addr.find("p")
            if p:
                address = p.get_text(strip=True)
        # Of not then nearest preceding <p> that looks like an address (contains numbers / postcode)
        if not address:
            p2 = a.find_previous("p")
            if p2:
                address = p2.get_text(strip=True)

        key = (title, href, address)
        if key in seen:
            continue
        seen.add(key)
        items.append({"name": title, "address_snippet": address, "maps_href": href, "list_page": page_url})
    return items

def resolve_maps_url(href):
    # Some links are already full google.com links, others are short maps.app.goo.gl — we resolve redirects
    try:
        # allow redirects so we get final Location. Use HEAD first then GET if needed.
        r = fetch(href, allow_redirects=True, timeout=20)
        return r.url
    except Exception:
        # return original href
        return href

def main():
    all_items = []
    for p in range(1, TOTAL_PAGES + 1):
        try:
            html, page_url = get_listing_page_html(p)
        except Exception as e:
            print(f"[ERROR] fetching page {p}: {e}")
            continue

        print(f"[PAGE {p}] parsing {page_url}")
        items = extract_items_from_html(html, page_url)
        print(f"  found {len(items)} direction links on page {p}")
        for it in items:
            # Resolve maps url
            maps_href = it["maps_href"]
            final_maps = None
            try:
                final_maps = resolve_maps_url(maps_href)
            except Exception as e:
                print("  failed to resolve maps href:", maps_href, e)
                final_maps = maps_href
            it["maps_url_resolved"] = final_maps
            all_items.append(it)
            time.sleep(0.12)  # tiny pause per item

        time.sleep(SLEEP_BETWEEN_REQUESTS)

    # Remove dupes by resolved maps url
    deduped = []
    seen_urls = set()
    for r in all_items:
        url = r.get("maps_url_resolved") or r.get("maps_href")
        if url in seen_urls:
            continue
        seen_urls.add(url)
        deduped.append(r)

    # Save JSON
    with open("zus_maps_links.json", "w", encoding="utf8") as f:
        json.dump(deduped, f, ensure_ascii=False, indent=2)
    # Save CSV
    with open("zus_maps_links.csv", "w", newline="", encoding="utf8") as f:
        writer = csv.DictWriter(f, fieldnames=["name","address_snippet","maps_href","maps_url_resolved","list_page"])
        writer.writeheader()
        for r in deduped:
            writer.writerow(r)

    print("Saved", len(deduped), "unique map links to zus_maps_links.json / .csv")

if __name__ == "__main__":
    main()
