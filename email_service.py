import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from config import *

def send_monthly_pack_email():
    """Send email notification with monthly pack summary"""
    
    if not EMAIL_ENABLED:
        print("📧 Email notifications disabled")
        return
    
    try:
        # Load current recommendations
        with open('recommendations.json', 'r') as f:
            pack = json.load(f)
        
        # Create email content
        subject = f"🎁 Your Monthly Pack for {pack['month_year']}"
        
        # Create HTML email body
        html_body = f"""
        <html>
        <body style="font-family: Georgia, serif; background-color: #f5f7fa; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 15px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
                <h1 style="color: #2c3e50; text-align: center; margin-bottom: 30px;">🎁 Your Monthly Pack</h1>
                <p style="color: #7f8c8d; text-align: center; font-size: 1.1em;">Personalized recommendations for {pack['month_year']}</p>
                
                <div style="margin: 30px 0;">
                    <h3 style="color: #667eea;">📺 Entertainment</h3>
                    <p><strong>{pack['recommendations']['entertainment']['title']}</strong></p>
                    <p style="color: #7f8c8d;">{pack['recommendations']['entertainment']['description'][:100]}...</p>
                </div>
                
                <div style="margin: 30px 0;">
                    <h3 style="color: #667eea;">📚 Book</h3>
                    <p><strong>{pack['recommendations']['book']['title']}</strong> by {pack['recommendations']['book']['author']}</p>
                    <p style="color: #7f8c8d;">{pack['recommendations']['book']['description'][:100]}...</p>
                </div>
                
                <div style="margin: 30px 0;">
                    <h3 style="color: #667eea;">🎧 Podcast</h3>
                    <p><strong>{pack['recommendations']['podcast']['title']}</strong></p>
                    <p style="color: #7f8c8d;">by {pack['recommendations']['podcast']['creator']}</p>
                </div>
                
                <div style="margin: 30px 0;">
                    <h3 style="color: #667eea;">🍷 Wine</h3>
                    <p><strong>{pack['recommendations']['wine']['name']}</strong></p>
                    <p style="color: #7f8c8d;">{pack['recommendations']['wine']['description'][:100]}...</p>
                </div>
                
                <div style="margin: 30px 0;">
                    <h3 style="color: #667eea;">🥾 Hiking</h3>
                    <p><strong>{pack['recommendations']['hiking']['name']}</strong></p>
                    <p style="color: #7f8c8d;">{pack['recommendations']['hiking']['location']} • {pack['recommendations']['hiking']['distance']}</p>
                </div>
                
                <div style="margin: 30px 0;">
                    <h3 style="color: #667eea;">🌸 Perfume</h3>
                    <p><strong>{pack['recommendations']['perfume']['name']}</strong></p>
                    <p style="color: #7f8c8d;">{pack['recommendations']['perfume']['brand']} • {pack['recommendations']['perfume']['price_range']}</p>
                </div>
                
                <div style="text-align: center; margin-top: 40px; padding: 20px; background: #ecf0f1; border-radius: 10px;">
                    <p style="color: #2c3e50; margin: 0;">💝 Open your local monthly_pack.html file for the full beautiful display!</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Create plain text version
        text_body = f"""
Your Monthly Pack for {pack['month_year']}

📺 Entertainment: {pack['recommendations']['entertainment']['title']}
📚 Book: {pack['recommendations']['book']['title']} by {pack['recommendations']['book']['author']}
🎧 Podcast: {pack['recommendations']['podcast']['title']}
🍷 Wine: {pack['recommendations']['wine']['name']}
🥾 Hiking: {pack['recommendations']['hiking']['name']}
🌸 Perfume: {pack['recommendations']['perfume']['name']}

Open your monthly_pack.html file for the full experience!
        """
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = RECIPIENT_EMAIL
        
        # Attach both versions
        msg.attach(MIMEText(text_body, 'plain'))
        msg.attach(MIMEText(html_body, 'html'))
        
        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        
        print(f"📧 Monthly pack emailed to {RECIPIENT_EMAIL}")
        
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        print("💡 Email feature is optional - your monthly pack HTML is still ready!")

if __name__ == "__main__":
    send_monthly_pack_email()