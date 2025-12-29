from app import db
from datetime import datetime
import uuid
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

def generate_uuid():
    return str(uuid.uuid4())

class User(UserMixin, db.Model):
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=True)  # Contact phone number
    events = db.relationship('Event', backref='owner', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Event(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    # owner_id is now a foreign key to User.id. Allowing nullable for legacy/guest events if needed, 
    # but ideally linked to user.
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=True) 
    # Keeping owner_id column for now if it was used differently, but user_id is the standard relation.
    # Actually, let's replace owner_id with user_id behavior or map it.
    # The previous code had owner_id = db.Column(db.String(36), nullable=True)
    # I will replace it with the Foreign Key to maintain existing pattern but Enforce relation.
    # If existing rows have owner_id, this might be tricky without migration.
    # Since it's dev/local, I'll add user_id and leave owner_id as legacy or just use user_id.
    # Let's simple swap owner_id definition.
    # owner_id = db.Column(db.String(36), nullable=True) -> replaced by relationship in User
    # But we need the column on specific naming.
    # Let's use user_id as the column name for the relationship.
    
    title = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False) # Birthday, Wedding, etc.
    template_id = db.Column(db.String(50), nullable=False)
    
    # Content Fields (User customized)
    host_name = db.Column(db.String(100))
    partner_name = db.Column(db.String(100))
    event_date = db.Column(db.String(50))
    event_time = db.Column(db.String(50))
    venue = db.Column(db.String(200))
    dress_code = db.Column(db.String(100))
    message = db.Column(db.Text)
    background_image_url = db.Column(db.Text)
    # New field for full-page background/frame
    background_style = db.Column(db.Text, nullable=True)
    
    # Contact Information (optional, overrides user's default contact)
    contact_email = db.Column(db.String(120), nullable=True)
    contact_phone = db.Column(db.String(20), nullable=True)

    # Precise Geographic Coordinates
    venue_latitude = db.Column(db.Float, nullable=True)
    venue_longitude = db.Column(db.Float, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    guests = db.relationship('Guest', backref='event', lazy=True, cascade="all, delete-orphan")
    comments = db.relationship('Comment', backref='event', lazy=True, cascade="all, delete-orphan")
    shares = db.relationship('Share', backref='event', lazy=True, cascade="all, delete-orphan")
    views = db.relationship('View', backref='event', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'type': self.type,
            'template_id': self.template_id,
            'host_name': self.host_name,
            'partner_name': self.partner_name,
            'event_date': self.event_date,
            'event_time': self.event_time,
            'venue': self.venue,
            'dress_code': self.dress_code,
            'message': self.message,
            'background_image_url': self.background_image_url,
            'background_style': self.background_style,
            'venue_latitude': self.venue_latitude,
            'venue_longitude': self.venue_longitude,
            'created_at': self.created_at.isoformat()
        }

class Guest(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    event_id = db.Column(db.String(36), db.ForeignKey('event.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    rsvp_status = db.Column(db.String(20), default='Pending') # Yes, No, Maybe, Pending
    rsvp_time = db.Column(db.DateTime, nullable=True)
    plus_one_count = db.Column(db.Integer, default=0)
    notes = db.Column(db.Text)
    
    # Professional Features
    dietary_restrictions = db.Column(db.String(200), nullable=True)
    invitation_sent_at = db.Column(db.DateTime, nullable=True)
    invitation_opened_at = db.Column(db.DateTime, nullable=True)
    
    # Personalization
    unique_token = db.Column(db.String(36), default=generate_uuid, unique=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'rsvp_status': self.rsvp_status,
            'plus_one_count': self.plus_one_count,
            'dietary_restrictions': self.dietary_restrictions,
            'notes': self.notes,
            'unique_token': self.unique_token,
            'invitation_sent': self.invitation_sent_at.isoformat() if self.invitation_sent_at else None,
            'rsvp_time': self.rsvp_time.isoformat() if self.rsvp_time else None
        }

class Comment(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    event_id = db.Column(db.String(36), db.ForeignKey('event.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False) # Guest name or User name
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'content': self.content,
            'created_at': self.created_at.isoformat()
        }

class Share(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.String(36), db.ForeignKey('event.id'), nullable=False)
    channel = db.Column(db.String(50)) # whatsapp, linkedin, copy, etc.
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class View(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.String(36), db.ForeignKey('event.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Venue(db.Model):
    """Store detailed venue information"""
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    event_id = db.Column(db.String(36), db.ForeignKey('event.id'), nullable=False, unique=True)
    
    # Location details
    place_id = db.Column(db.String(100), nullable=True)  # OpenStreetMap place ID
    name = db.Column(db.String(200), nullable=True)
    address = db.Column(db.String(500), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    
    # Additional details
    venue_type = db.Column(db.String(50), nullable=True)  # restaurant, hall, home, park, etc.
    parking_info = db.Column(db.Text, nullable=True)
    accessibility_notes = db.Column(db.Text, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'place_id': self.place_id,
            'name': self.name,
            'address': self.address,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'venue_type': self.venue_type,
            'parking_info': self.parking_info,
            'accessibility_notes': self.accessibility_notes
        }

class EmailLog(db.Model):
    """Track sent emails for analytics"""
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    event_id = db.Column(db.String(36), db.ForeignKey('event.id'), nullable=False)
    guest_id = db.Column(db.String(36), db.ForeignKey('guest.id'), nullable=True)
    
    email_type = db.Column(db.String(50), nullable=False)  # invitation, confirmation, reminder
    recipient_email = db.Column(db.String(120), nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    opened_at = db.Column(db.DateTime, nullable=True)
    clicked_at = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default='sent')  # sent, delivered, opened, failed
    
    def to_dict(self):
        return {
            'id': self.id,
            'email_type': self.email_type,
            'recipient_email': self.recipient_email,
            'sent_at': self.sent_at.isoformat(),
            'opened_at': self.opened_at.isoformat() if self.opened_at else None,
            'status': self.status
        }


class CustomDesign(db.Model):
    """Store custom designs created in Design Studio"""
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    
    title = db.Column(db.String(200), nullable=False, default='Untitled Design')
    canvas_data = db.Column(db.Text, nullable=False)  # JSON string of Fabric.js canvas
    thumbnail_url = db.Column(db.Text, nullable=True)  # Base64 or URL to thumbnail image
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref=db.backref('custom_designs', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'canvas_data': self.canvas_data,
            'thumbnail_url': self.thumbnail_url,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

