import smtplib
from email.mime.text import MIMEText
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

class Notifier:
    def __init__(self, email_to, sms_to, smtp_user, smtp_pass, twilio_sid, twilio_token, twilio_from, logger):
        self.email_to = email_to
        self.sms_to = sms_to
        self.smtp_user = smtp_user
        self.smtp_pass = smtp_pass
        self.twilio_sid = twilio_sid
        self.twilio_token = twilio_token
        self.twilio_from = twilio_from
        self.logger = logger

    def send_email(self, message):
        """Send an email notification via SMTP (e.g., Gmail)."""
        if not self.email_to or not self.smtp_user or not self.smtp_pass:
            self.logger.warning("Email not configured, skipping")
            return  # Skip if not configured
        try:
            msg = MIMEText(message)
            msg["Subject"] = "Sentinel Alert: UTXO Spent"
            msg["From"] = self.smtp_user
            msg["To"] = self.email_to
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_pass)
                server.send_message(msg)
            self.logger.info("Email sent successfully")
        except Exception as e:
            self.logger.error(f"Failed to send email: {e}")

    def send_sms(self, message):
        """Send an SMS notification via Twilio."""
        if not self.sms_to or not self.twilio_sid or not self.twilio_token or not self.twilio_from:
            self.logger.warning("SMS not configured, skipping")
            return
        try:
            client = Client(self.twilio_sid, self.twilio_token)
            client.messages.create(
                to=self.sms_to,
                from_=self.twilio_from,
                body=message
            )
            self.logger.info("SMS sent successfully")
        except TwilioRestException as e:
            self.logger.error(f"Failed to send SMS: {e}")

    def notify(self, txid, vout):
        """Send notifications when UTXO is spent."""
        message = f"UTXO spent: txid={txid}, vout={vout}"
        self.send_email(message)
        self.send_sms(message)
