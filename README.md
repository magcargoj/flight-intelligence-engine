# ✈️ Flight Intelligence Engine

**An automated daily-scanning engine designed to identify high-value travel opportunities for a nomadic family of six.**

## 🎯 Project Overview
This Python-based intelligence tool orchestrates data from the **SerpApi Google Flights Engine** to identify "WOW" deals—defined as high-value travel opportunities that meet specific cost-per-passenger and duration thresholds.

## 🏗️ Technical Architecture
- **Data Orchestration:** Python backend fetching, filtering, and deduplicating flight deals.
- **Intelligence Layer:** Custom logic to calculate total family costs for long-term nomadic stays.
- **Automation:** Scheduled task execution with daily personalized email summaries via Gmail SMTP.
- **Persistence:** SQLite database for tracking deal history and avoiding notification fatigue.

## 🛠️ Key Features
- **Dynamic "Anywhere" Search:** Leveraging Google Travel Explore to find the best value from target airports.
- **Cost Analysis:** Granular breakdown of total family cost (6 passengers) vs. market averages.
- **Automated Alerts:** Real-time email notifications for deals that cross the "Sentinel" value threshold.

---
**Maintained by [Jeremy Wood](https://jeremywood.digital)**  
*Technical Sentinel | Python Automation*
