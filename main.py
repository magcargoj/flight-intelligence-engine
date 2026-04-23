import logging
from nomad_flight_finder.src.deal_engine import fetch_rss_deals
from nomad_flight_finder.src.search_engine import get_inspiration_deals
from nomad_flight_finder.src.notifier import send_daily_summary
from nomad_flight_finder.src.db_manager import init_db, is_deal_sent, mark_deal_as_sent

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_scan():
    logging.info("Starting Daily Nomad Flight Scan...")
    
    # 1. Initialize DB
    init_db()
    
    # 2. Fetch Curated Deals (RSS)
    logging.info("Fetching RSS deals...")
    rss_deals = fetch_rss_deals()
    
    # 3. Fetch Dynamic Deals (SerpApi)
    logging.info("Fetching Google Flights inspiration deals via SerpApi...")
    amadeus_deals = get_inspiration_deals()
    
    all_found = rss_deals + amadeus_deals
    new_deals = []
    
    # 4. Filter for only new deals
    for deal in all_found:
        if not is_deal_sent(deal['id']):
            new_deals.append(deal)
            mark_deal_as_sent(deal['id'])
    
    # 5. Send Summary
    if new_deals:
        logging.info(f"Found {len(new_deals)} NEW deals. Sending summary...")
        success = send_daily_summary(new_deals)
        if success:
            logging.info("Summary sent successfully!")
        else:
            logging.warning("Failed to send summary (or no API key).")
    else:
        logging.info("No new deals found today.")

if __name__ == "__main__":
    run_scan()
