import feedparser
import requests
from .config import ORIGINS, RESIDENT_CITY

FEEDS = [
    "https://www.theflightdeal.com/feed",
    "https://www.fly4free.com/feed/"
]

def fetch_rss_deals():
    found_deals = []
    keywords = ORIGINS + [RESIDENT_CITY, "Charlotte", "Raleigh", "Wilmington"]
    
    for url in FEEDS:
        try:
            # Use requests with a timeout to avoid hanging
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=10)
            feed = feedparser.parse(response.content)
            
            for entry in feed.entries:
                title = entry.title.upper()
                summary = entry.get('summary', '').upper()
                
                # Check if any keyword is in title or summary
                if any(keyword.upper() in title or keyword.upper() in summary for keyword in keywords):
                    found_deals.append({
                        "id": entry.link,
                        "title": entry.title,
                        "link": entry.link,
                        "source": "RSS Feed",
                        "type": "Curated Deal"
                    })
        except Exception as e:
            print(f"Error fetching {url}: {e}")
    
    return found_deals

if __name__ == "__main__":
    deals = fetch_rss_deals()
    for d in deals:
        print(f"[{d['source']}] {d['title']} - {d['link']}")
