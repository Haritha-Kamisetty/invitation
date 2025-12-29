"""
Email Service for sending professional invitation emails
Supports Gmail SMTP and other email providers
"""
from flask import render_template, current_app
from flask_mail import Mail, Message
import os

mail = Mail()

def init_mail(app):
    """Initialize Flask-Mail with app"""
    mail.init_app(app)

def send_invitation_email(event, guest, invitation_url):
    """
    Send invitation email to a guest
    
    Args:
        event: Event object
        guest: Guest object
        invitation_url: Full URL to the invitation
    
    Returns:
        bool: True if sent successfully, False otherwise
    """
    try:
        msg = Message(
            subject=f"You're Invited: {event.title}",
            recipients=[guest.email] if guest.email else [],
            sender=current_app.config['MAIL_DEFAULT_SENDER']
        )
        
        # Render HTML email template
        msg.html = render_template(
            'emails/invitation_email.html',
            event=event,
            guest=guest,
            invitation_url=invitation_url
        )
        
        # Plain text fallback
        msg.body = f"""
You're Invited to {event.title}!

Dear {guest.name},

You are cordially invited to {event.title}.

When: {event.event_date} at {event.event_time}
Where: {event.venue}

Please RSVP at: {invitation_url}

We hope to see you there!

Best regards,
{event.host_name}
        """
        
        if guest.email:
            mail.send(msg)
            return True
        return False
        
    except Exception as e:
        print(f"Error sending email to {guest.email}: {str(e)}")
        return False

def send_rsvp_confirmation_email(event, guest):
    """
    Send RSVP confirmation email to a guest
    
    Args:
        event: Event object
        guest: Guest object
    
    Returns:
        bool: True if sent successfully, False otherwise
    """
    try:
        if not guest.email:
            return False
            
        msg = Message(
            subject=f"RSVP Confirmed: {event.title}",
            recipients=[guest.email],
            sender=current_app.config['MAIL_DEFAULT_SENDER']
        )
        
        msg.html = render_template(
            'emails/rsvp_confirmation_email.html',
            event=event,
            guest=guest
        )
        
        msg.body = f"""
RSVP Confirmation

Dear {guest.name},

Thank you for your RSVP to {event.title}!

Your Response: {guest.rsvp_status}
Event Date: {event.event_date} at {event.event_time}
Venue: {event.venue}

We look forward to seeing you!

Best regards,
{event.host_name}
        """
        
        mail.send(msg)
        return True
        
    except Exception as e:
        print(f"Error sending confirmation email to {guest.email}: {str(e)}")
        return False

def send_bulk_invitations(event, guests, base_url):
    """
    Send invitation emails to multiple guests
    
    Args:
        event: Event object
        guests: List of Guest objects
        base_url: Base URL of the application
    
    Returns:
        dict: Statistics about sent emails
    """
    stats = {
        'total': len(guests),
        'sent': 0,
        'failed': 0,
        'skipped': 0
    }
    
    for guest in guests:
        if not guest.email:
            stats['skipped'] += 1
            continue
            
        invitation_url = f"{base_url}/event/{event.id}?guest={guest.unique_token}"
        
        if send_invitation_email(event, guest, invitation_url):
            stats['sent'] += 1
        else:
            stats['failed'] += 1
    
    return stats
