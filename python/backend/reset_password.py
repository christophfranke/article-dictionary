from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from flask import current_app
from mail import mail


def create_password_link(email):
    # Create a URLSafeTimedSerializer instance
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

    # Generate a token for the email
    token = s.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])

    # Generate a password reset link using the token
    frontend_base_url = f"{current_app.config['EXTERNAL_PROTOCOL']}://{current_app.config['EXTERNAL_HOSTNAME']}"
    reset_link = f"{frontend_base_url}/reset-password?token={token}"

    return reset_link


def send_reset_mail(email, reset_link):
    # Create a message object for the email
    msg = Message('Password Reset Request',
                  sender=current_app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[email])

    # Set the email body
    msg.body = f'Please use the following link to reset your password: {reset_link}\n' \
               f'This link will expire in 30 minutes.'

    # Send the email using Flask-Mail
    # Try to send the email and log success or failure
    try:
        mail.send(msg)
        print(f"Password reset email sent to {email}.")
        return True
    except SMTPException as e:
        print(f"Failed to send password reset email to {email}. Error: {e}")
    except Exception as e:
        print(f"Unexpected error occurred while sending password reset email to {email}. Error: {e}")

    return False
