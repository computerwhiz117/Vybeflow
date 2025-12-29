"""
Notification utilities for sending emails and SMS messages
"""
from flask_mail import Message, Mail
from twilio.rest import Client
import os

# Initialize mail (will be configured from app)
mail = Mail()

def send_welcome_email(recipient_email, username):
    """Send a welcome email to new users"""
    try:
        msg = Message(
            subject='Welcome to VybeFlow!',
            sender=os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@vybeflow.com'),
            recipients=[recipient_email]
        )
        
        msg.body = f"""
Hello {username},

Welcome to VybeFlow! 🎉

Your account has been successfully created. You can now log in and start exploring.

Username: {username}
Email: {recipient_email}

Thank you for joining our community!

Best regards,
The VybeFlow Team
"""
        
        msg.html = f"""
<html>
<body style="font-family: Arial, sans-serif; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #6dd5ed;">Welcome to VybeFlow! 🎉</h2>
        <p>Hello <strong>{username}</strong>,</p>
        <p>Your account has been successfully created. You can now log in and start exploring.</p>
        <div style="background: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <p><strong>Username:</strong> {username}</p>
            <p><strong>Email:</strong> {recipient_email}</p>
        </div>
        <p>Thank you for joining our community!</p>
        <p style="color: #666; margin-top: 30px;">
            Best regards,<br>
            The VybeFlow Team
        </p>
    </div>
</body>
</html>
"""
        
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def send_welcome_sms(phone_number, username):
    """Send a welcome SMS to new users"""
    try:
        # Get Twilio credentials from environment variables
        account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        twilio_phone = os.environ.get('TWILIO_PHONE_NUMBER')
        
        # Skip if Twilio is not configured
        if not all([account_sid, auth_token, twilio_phone]):
            print("Twilio credentials not configured, skipping SMS")
            return False
        
        # Initialize Twilio client
        client = Client(account_sid, auth_token)
        
        # Format phone number (add +1 if not present for US numbers)
        if not phone_number.startswith('+'):
            phone_number = f'+1{phone_number}'
        
        # Send SMS
        message = client.messages.create(
            body=f"Welcome to VybeFlow, {username}! Your account has been successfully created. Log in now to get started!",
            from_=twilio_phone,
            to=phone_number
        )
        
        print(f"SMS sent successfully: {message.sid}")
        return True
    except Exception as e:
        print(f"Error sending SMS: {e}")
        return False


def send_signup_notifications(email, phone, username):
    """Send both email and SMS notifications for new signup"""
    results = {
        'email': False,
        'sms': False
    }
    
    # Send email
    if email:
        results['email'] = send_welcome_email(email, username)
    
    # Send SMS if phone number is provided
    if phone:
        results['sms'] = send_welcome_sms(phone, username)
    
    return results
