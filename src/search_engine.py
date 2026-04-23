import requests
from .config import SERPAPI_KEY, ORIGINS, FAMILY_PRICING_FACTOR, THRESHOLDS
import logging

def get_inspiration_deals():
    if not SERPAPI_KEY:
        logging.warning("SERPAPI_KEY missing. Skipping Google Flights search.")
        return []

    all_deals = []
    
    for origin in ORIGINS:
        try:
            # params for Explore Anywhere
            params = {
                "engine": "google_travel_explore",
                "departure_id": origin,
                "category": "1", # 1 for Flights
                "currency": "USD",
                "api_key": SERPAPI_KEY
            }
            
            response = requests.get("https://serpapi.com/search", params=params)
            data = response.json()
            
            if "destinations" not in data:
                continue

            for deal in data["destinations"]:
                country = deal.get('country', 'Unknown')
                
                # Filter for International Only
                if country == "United States":
                    continue

                price_val = deal.get('flight_price', 0)
                if not price_val:
                    continue

                # Determine Threshold
                limit = THRESHOLDS["Global"]
                if country in ["Mexico", "Guatemala", "Costa Rica", "Panama"]:
                    limit = THRESHOLDS["Central America"] if country != "Mexico" else THRESHOLDS["Mexico"]
                
                if price_val > limit:
                    continue

                family_total = price_val * FAMILY_PRICING_FACTOR
                destination = deal.get('name', 'Unknown')
                airline = deal.get('airline', 'Various')
                duration_mins = deal.get('flight_duration', 0)
                duration_str = f"{duration_mins // 60}h {duration_mins % 60}m" if duration_mins else "Unknown"
                
                # Improved Link Generation
                # We use the specific dates and airport codes to build a direct search link
                dest_code = deal.get('destination_airport', {}).get('code', deal.get('destination_id', ''))
                start_date = deal.get('start_date', '')
                end_date = deal.get('end_date', '')
                
                # This format forces Google Flights to show the specific dates and route
                direct_link = f"https://www.google.com/travel/flights?q=Flights%20to%20{dest_code}%20from%20{origin}%20on%20{start_date}%20returning%20{end_date}"
                
                all_deals.append({
                    "id": f"serpapi_{origin}_{destination}_{start_date}_{price_val}",
                    "title": f"WOW: {destination}, {country} from {origin}",
                    "destination": f"{destination}, {country}",
                    "origin": origin,
                    "departure_date": start_date,
                    "return_date": end_date,
                    "price_per_person": price_val,
                    "family_total": family_total,
                    "airline": airline,
                    "duration": duration_str,
                    "stops": deal.get('number_of_stops', 'N/A'),
                    "link": direct_link, # Updated link
                    "source": "Google Flights",
                    "type": "Anywhere Search"
                })
        except Exception as e:
            logging.error(f"SerpApi Error for {origin}: {e}")
            
    return all_deals
