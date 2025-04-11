import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()
sender_email = "meeturiajaykumar.23@gmail.com"
sender_password = os.getenv("GOOGLE_APP_PASSWORD")

def send_email_result(candidate_name, candidate_email, is_selected):
    if is_selected:
        subject = "🎉 You're Selected - Congratulations!"
        body = f"""
Hi {candidate_name},

We are pleased to inform you that you have been selected for the next steps in our hiring process!

Congratulations on making it this far. Our team was really impressed with your profile.

We will be sending more details shortly.

Best Regards,\nThe Team
        """
    else:
        subject = "Update on Your Job Application"
        body = f"""
Hi {candidate_name},

Thank you for taking the time to apply and participate in our screening process.

After careful consideration, we regret to inform you that we won't be moving forward with your application at this time.

We appreciate your interest and encourage you to apply for future opportunities with us.

Best Wishes,\nThe Team
        """

    try:
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = candidate_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, candidate_email, message.as_string())
        server.quit()

        return f"✅ Email sent to {candidate_email}."
    except Exception as e:
        return f"❌ Failed to send email: {e}"
