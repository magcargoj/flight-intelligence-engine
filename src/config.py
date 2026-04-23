import os
from dotenv import load_dotenv

load_dotenv()

# Family Configuration (Ages: 33, 33, 11, 9, 5, 18mo)
# Pricing Factor: 6.0 (All 6 family members will have their own full seats for car seats)
FAMILY_PRICING_FACTOR = 6.0 
FAMILY_SIZE = 6 # Total humans

ORIGINS = ["CLT", "RDU", "ILM"]
RESIDENT_CITY = "North Carolina"

# SMTP Configuration
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# Recipients
RECIPIENTS = [EMAIL_RECEIVER, "abwood032993@gmail.com"] 

# API Keys
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

# WOW Thresholds (Price per Adult Roundtrip)
# These are "Can't pass up" deals for NC origins
THRESHOLDS = {
    "Europe": 450,
    "Asia": 650,
    "South America": 450,
    "Central America": 300,
    "Mexico": 250,
    "Domestic": 9999,
    "Global": 400 
}
