import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Template
from .config import SMTP_SERVER, SMTP_PORT, EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER, FAMILY_PRICING_FACTOR

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; color: #333; margin: 0; padding: 20px; }
        .container { max-width: 600px; margin: auto; background: #fff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        .header { text-align: center; border-bottom: 2px solid #eee; padding-bottom: 20px; }
        .header h1 { color: #2c3e50; margin: 0; }
        .header p { color: #7f8c8d; font-size: 14px; }
        .deal-card { border: 1px solid #eee; border-radius: 8px; padding: 15px; margin-top: 20px; background: #fafafa; }
        .deal-title { font-weight: bold; color: #e67e22; font-size: 18px; }
        .deal-meta { font-size: 13px; color: #95a5a6; margin-bottom: 10px; }
        .family-summary { background: #e8f6f3; padding: 10px; border-radius: 5px; margin-top: 10px; border-left: 4px solid #1abc9c; }
        .details-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 10px; font-size: 14px; }
        .price { font-size: 20px; font-weight: bold; color: #27ae60; }
        .btn { display: inline-block; background: #3498db; color: #fff; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin-top: 15px; }
        .footer { text-align: center; margin-top: 30px; font-size: 12px; color: #bdc3c7; }
        .tag { background: #34495e; color: #fff; padding: 2px 8px; border-radius: 4px; font-size: 10px; text-transform: uppercase; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌍 Nomad Flight Intel</h1>
            <p><strong>International "WOW" Deals</strong> for the Wood Family (6 seats)</p>
        </div>

        {% for deal in deals %}
        <div class="deal-card">
            <div class="deal-title">{{ deal.title }}</div>
            <div class="deal-meta">Origin: {{ deal.origin }} | Date: {{ deal.departure_date }}</div>
            
            <div class="details-grid">
                <div><strong>Airline:</strong> {{ deal.airline }}</div>
                <div><strong>Duration:</strong> {{ deal.duration }}</div>
                <div><strong>Stops:</strong> {{ deal.stops }}</div>
                <div><strong>Type:</strong> <span class="tag">{{ deal.type }}</span></div>
            </div>

            <div class="family-summary">
                <span class="price">${{ "{:,.0f}".format(deal.price_per_person) }}</span> <small>per seat</small><br>
                <strong>Family Total (6 seats): ${{ "{:,.2f}".format(deal.family_total) }}</strong><br>
                <small style="color: #666;">(Estimated total for everyone with their own seat)</small>
            </div>
            
            <a href="{{ deal.link }}" class="btn">View on Google Flights</a>
        </div>
        {% endfor %}

        <div class="footer">
            Sent with ❤️ by your Flight Finder Bot.<br>
            Filtering for International Deals < ${{ Global_Limit }} | CLT, RDU, ILM
        </div>
    </div>
</body>
</html>
"""

def send_daily_summary(deals):
    if not deals:
        return False
    
    if not EMAIL_SENDER or not EMAIL_PASSWORD or not EMAIL_RECEIVER:
        return False

    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"🔥 {len(deals)} International 'WOW' Deals Found!"
    msg['From'] = EMAIL_SENDER
    msg['To'] = ", ".join(RECIPIENTS)

    # Threshold for footer
    from .config import THRESHOLDS, RECIPIENTS
    
    template = Template(HTML_TEMPLATE)
    html_content = template.render(deals=deals, Global_Limit=THRESHOLDS["Global"])
    msg.attach(MIMEText(html_content, 'html'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, [EMAIL_RECEIVER], msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending SMTP email: {e}")
        return False
