from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, send_file, current_app
import flask
from app import db, login_manager
from app.models import Event, Guest, Comment, Share, View, User, Venue, EmailLog
from datetime import datetime
from flask_login import login_user, logout_user, login_required, current_user
from app import email_service, export_service, venue_service
from werkzeug.utils import secure_filename
import os
import io
import uuid


# Reload check 1
main = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# --- View Routes ---
@main.route('/')
def index():
    return render_template('index.html')

@main.route('/templates')
def templates_page():
    return render_template('templates.html')

@main.route('/create')
@main.route('/create/<template_id>')
@login_required
def create_event_page(template_id=None):
    return render_template('editor.html', template_id=template_id)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.user_dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if not user:
            return render_template('login.html', error='No account found with this email address')
        
        if not user.check_password(password):
            return render_template('login.html', error='Incorrect password')
        
        login_user(user, remember=True)
        return redirect(url_for('main.user_dashboard'))
            
    return render_template('login.html')

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.user_dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        phone = request.form.get('phone')  # Get phone number
        
        if User.query.filter_by(email=email).first():
            return render_template('signup.html', error='Email already registered')
            
        new_user = User(email=email, name=name, phone=phone)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        return redirect(url_for('main.user_dashboard'))
        
    return render_template('signup.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@main.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    
    # Check if email is already taken by another user
    if email != current_user.email:
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already in use by another account')
            return redirect(url_for('main.profile'))
    
@main.route('/api/download', methods=['POST'])
def download_file():
    try:
        data = request.json
        image_data = data.get('image')
        format_type = data.get('format')
        title = data.get('title', 'invitation')
        
        # Sanitize title
        safe_title = "".join([c for c in title if c.isalnum() or c in (' ', '-', '_')]).strip()
        safe_title = safe_title.replace(' ', '_') or 'invitation'
        
        # Decode base64 image
        if ',' in image_data:
            header, encoded = image_data.split(',', 1)
        else:
            encoded = image_data
            
        import base64
        file_bytes = base64.b64decode(encoded)
        
        if format_type == 'png':
            return send_file(
                io.BytesIO(file_bytes),
                mimetype='image/png',
                as_attachment=True,
                download_name=f"{safe_title}.png"
            )
            
        elif format_type == 'pdf':
            # Basic Image-to-PDF using FPDF logic (simulated with standard headers implies PDF reader)
            # Since we can't easily install FPDF, we will send the PNG but wrapped? 
            # No, user wants PDF. 
            # Client-side PDF generation is usually better if backend lacks libs.
            # But we can try to return the bytes with application/pdf if we trust the client to generate it?
            # NO. The client ALREADY generated the image.
            # We will stick to Client-Side for PDF generation logic, 
            # OR we simply cannot make a PDF without a lib.
            # Wait, we can use the "img2pdf" trick if installed?
            # Let's check imports.
            # If no lib, we might have to revert to client-side-download for PDF,
            # BUT relay it through the server to get the filename right.
            # Actually, standard PDF requires a generator.
            # Let's handle PNG and DOC (Word) here specially.
            
            # For this specific "Fix", we will assume the Client generates the PDF blob and sends it?
            # No, sending large blobs is heavy.
            pass

        elif format_type == 'word':
            # Embed Image in Word-compatible HTML
            # This logic is extremely robust for "Opening" in Word.
            img_b64 = base64.b64encode(file_bytes).decode('utf-8')
            
            doc_content = f"""
            <html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-com:office:word' xmlns='http://www.w3.org/TR/REC-html40'>
            <head>
                <meta charset="utf-8">
                <title>{safe_title}</title>
            </head>
            <body>
                <div style="text-align: center; width: 100%;">
                    <!-- Standard Word-compatible Image Embed -->
                    <img src="data:image/png;base64,{img_b64}" style="width:100%; max-width:650px; height:auto;">
                </div>
            </body>
            </html>
            """
            
            return send_file(
                io.BytesIO(doc_content.encode('utf-8')),
                mimetype='application/msword',
                as_attachment=True,
                download_name=f"{safe_title}.doc"
            )
            
    except Exception as e:
        print(f"Download Error: {e}")
        return jsonify({'error': str(e)}), 500
        
    return jsonify({'error': 'Invalid format'}), 400
    current_user.name = name
    current_user.email = email
    current_user.phone = phone if phone else None
    
    db.session.commit()
    flash('Profile updated successfully!')
    return redirect(url_for('main.profile'))

@main.route('/dashboard')
@login_required
def user_dashboard():
    # Fetch all events for current user, most recent first
    # Linking via relationship in User model: current_user.events
    # Or query explicitly if needed for ordering
    events = Event.query.filter_by(user_id=current_user.id).order_by(Event.created_at.desc()).all()
    return render_template('user_dashboard.html', events=events)

@main.route('/event/<event_id>')
def view_event(event_id):
    # Record view
    event = Event.query.get_or_404(event_id)
    new_view = View(event_id=event_id)
    db.session.add(new_view)
    db.session.commit()
    return render_template('invite.html', event=event)

@main.route('/dashboard/<event_id>')
@login_required
def event_dashboard(event_id):
    event = Event.query.get_or_404(event_id)
    # Ensure user can only access their own events
    if event.user_id != current_user.id:
        return redirect(url_for('main.user_dashboard'))
    return render_template('dashboard.html', event=event)

@main.route('/event/<event_id>/delete', methods=['POST'])
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    # Ensure user can only delete their own events
    if event.user_id != current_user.id:
        return flask.redirect(flask.url_for('main.user_dashboard'))
    db.session.delete(event)
    db.session.commit()
    return flask.redirect(flask.url_for('main.user_dashboard'))

# --- API Routes ---

@main.route('/api/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        filename = secure_filename(file.filename)
        # Unique filename to avoid collisions
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        
        upload_folder = current_app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
            
        file.save(os.path.join(upload_folder, unique_filename))
        
        # Return URL
        url = url_for('static', filename=f'uploads/{unique_filename}')
        return jsonify({'url': url}), 200
    
    return jsonify({'error': 'Upload failed'}), 500

@main.route('/api/events', methods=['POST'])
@login_required
def create_event():
    data = request.json
    new_event = Event(
        user_id=current_user.id,  # Link event to logged-in user
        title=data.get('title', 'My Event'),
        type=data.get('type'),
        template_id=data.get('template_id'),
        host_name=data.get('host_name'),
        partner_name=data.get('partner_name'),
        event_date=data.get('event_date'),
        event_time=data.get('event_time'),
        venue=data.get('venue'),
        dress_code=data.get('dress_code'),
        message=data.get('message'),
        background_image_url=data.get('background_image_url'),
        background_style=data.get('background_style'),
        contact_email=data.get('contact_email'),  # Custom contact email
        contact_phone=data.get('contact_phone'),   # Custom contact phone
        venue_latitude=data.get('venue_latitude'),
        venue_longitude=data.get('venue_longitude')
    )
    db.session.add(new_event)
    db.session.commit()
    return jsonify(new_event.to_dict()), 201

@main.route('/api/events/<event_id>', methods=['GET'])
def get_event(event_id):
    event = Event.query.get_or_404(event_id)
    return jsonify(event.to_dict())

@main.route('/api/events/<event_id>/guests', methods=['GET', 'POST'])
def handle_guests(event_id):
    if request.method == 'POST':
        data = request.json
        # Bulk or single add
        guests_data = data.get('guests', [])
        if not guests_data:
            # Fallback to single guest
            guests_data = [data]
        
        created_guests = []
        for g_data in guests_data:
            new_guest = Guest(
                event_id=event_id,
                name=g_data.get('name'),
                email=g_data.get('email'),
                phone=g_data.get('phone')
            )
            db.session.add(new_guest)
            created_guests.append(new_guest)
        
        db.session.commit()
        return jsonify([g.to_dict() for g in created_guests]), 201
    else:
        # GET all guests for event
        guests = Guest.query.filter_by(event_id=event_id).all()
        return jsonify([g.to_dict() for g in guests])

@main.route('/api/events/<event_id>/rsvp', methods=['POST'])
def rsvp(event_id):
    data = request.json
    guest_id = data.get('guest_id') # Optional if using token
    token = data.get('token')
    
    guest = None
    if token:
        guest = Guest.query.filter_by(unique_token=token).first()
    elif guest_id:
        guest = Guest.query.get(guest_id)
        
    if not guest:
        # Allow anonymous RSVP or create new guest functionality could go here
        # For now, require valid guest
        return jsonify({'error': 'Invalid guest'}), 400
    
    # Get event for email
    event = Event.query.get_or_404(event_id)
    
    # Update guest information
    guest.rsvp_status = data.get('status') # Yes, No, Maybe
    guest.plus_one_count = data.get('plus_one_count', 0)
    guest.notes = data.get('notes', '')
    guest.dietary_restrictions = data.get('dietary_restrictions', '')
    guest.rsvp_time = datetime.utcnow()
    
    db.session.commit()
    
    # Send confirmation email if guest has email
    if guest.email:
        try:
            email_service.send_rsvp_confirmation_email(event, guest)
        except Exception as e:
            print(f"Failed to send confirmation email: {str(e)}")
    
    return jsonify({'message': 'RSVP updated', 'guest': guest.to_dict()})

@main.route('/api/events/<event_id>/comments', methods=['GET', 'POST'])
def handle_comments(event_id):
    if request.method == 'POST':
        data = request.json
        new_comment = Comment(
            event_id=event_id,
            name=data.get('name', 'Anonymous'),
            content=data.get('content')
        )
        db.session.add(new_comment)
        db.session.commit()
        return jsonify(new_comment.to_dict()), 201
    else:
        comments = Comment.query.filter_by(event_id=event_id).order_by(Comment.created_at.desc()).all()
        return jsonify([c.to_dict() for c in comments])

@main.route('/api/events/<event_id>/dashboard_stats', methods=['GET'])
def get_dashboard_stats(event_id):
    event = Event.query.get_or_404(event_id)
    total_guests = Guest.query.filter_by(event_id=event_id).count()
    yes_count = Guest.query.filter_by(event_id=event_id, rsvp_status='Yes').count()
    maybe_count = Guest.query.filter_by(event_id=event_id, rsvp_status='Maybe').count()
    no_count = Guest.query.filter_by(event_id=event_id, rsvp_status='No').count()
    views_count = View.query.filter_by(event_id=event_id).count()
    comments_count = Comment.query.filter_by(event_id=event_id).count()
    
    return jsonify({
        'total_guests': total_guests,
        'rsvp_yes': yes_count,
        'rsvp_maybe': maybe_count,
        'rsvp_no': no_count,
        'views': views_count,
        'comments': comments_count
    })

# --- Professional Features API Endpoints ---

@main.route('/api/venues/autocomplete', methods=['GET'])
def venue_autocomplete():
    """Autocomplete venue search using OpenStreetMap"""
    query = request.args.get('q', '')
    country = request.args.get('country', 'in')
    
    if not query or len(query) < 3:
        return jsonify([])
    
    venues = venue_service.autocomplete_venue(query, country_code=country, limit=5)
    return jsonify(venues)

@main.route('/api/venues/geocode', methods=['POST'])
def geocode_venue():
    """Geocode an address to get coordinates"""
    data = request.json
    address = data.get('address')
    
    if not address:
        return jsonify({'error': 'Address is required'}), 400
    
    location = venue_service.geocode_address(address)
    if location:
        return jsonify(location)
    else:
        return jsonify({'error': 'Location not found'}), 404

@main.route('/api/events/<event_id>/guests/import', methods=['POST'])
@login_required
def import_guests(event_id):
    """Import guests from CSV file"""
    event = Event.query.get_or_404(event_id)
    
    # Verify ownership
    if event.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'Only CSV files are supported'}), 400
    
    try:
        # Import guests from CSV
        guests_data = export_service.import_guests_from_csv(file)
        
        # Create guest records
        created_guests = []
        for guest_data in guests_data:
            new_guest = Guest(
                event_id=event_id,
                name=guest_data['name'],
                email=guest_data.get('email'),
                phone=guest_data.get('phone'),
                dietary_restrictions=guest_data.get('dietary_restrictions'),
                notes=guest_data.get('notes')
            )
            db.session.add(new_guest)
            created_guests.append(new_guest)
        
        db.session.commit()
        
        return jsonify({
            'message': f'Successfully imported {len(created_guests)} guests',
            'count': len(created_guests),
            'guests': [g.to_dict() for g in created_guests]
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@main.route('/api/events/<event_id>/guests/export', methods=['GET'])
@login_required
def export_guests(event_id):
    """Export guest list to Excel or CSV"""
    event = Event.query.get_or_404(event_id)
    
    # Verify ownership
    if event.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    format_type = request.args.get('format', 'excel')
    guests = Guest.query.filter_by(event_id=event_id).all()
    
    if format_type == 'excel':
        output = export_service.export_guests_to_excel(event, guests)
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'{event.title}_guests.xlsx'
        )
    elif format_type == 'csv':
        csv_content = export_service.export_guests_to_csv(guests)
        output = io.BytesIO(csv_content.encode('utf-8'))
        output.seek(0)
        return send_file(
            output,
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'{event.title}_guests.csv'
        )
    else:
        return jsonify({'error': 'Invalid format. Use excel or csv'}), 400

@main.route('/api/events/<event_id>/qrcode', methods=['GET'])
@login_required
def generate_qrcode(event_id):
    """Generate QR code for event invitation"""
    event = Event.query.get_or_404(event_id)
    
    # Verify ownership
    if event.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Generate invitation URL
    base_url = request.url_root.rstrip('/')
    invitation_url = f"{base_url}/event/{event_id}"
    
    # Generate QR code
    qr_folder = current_app.config['QR_CODE_FOLDER']
    qr_path = export_service.generate_qr_code(invitation_url, event_id, qr_folder)
    
    if qr_path:
        # Return relative path for frontend
        qr_filename = os.path.basename(qr_path)
        return jsonify({
            'qr_code_url': f'/static/qrcodes/{qr_filename}',
            'invitation_url': invitation_url
        })
    else:
        return jsonify({'error': 'Failed to generate QR code'}), 500

@main.route('/api/events/<event_id>/send-invitations', methods=['POST'])
@login_required
def send_invitations(event_id):
    """Send invitation emails to all guests with email addresses"""
    event = Event.query.get_or_404(event_id)
    
    # Verify ownership
    if event.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json or {}
    guest_ids = data.get('guest_ids', [])
    
    # Get guests to send invitations to
    if guest_ids:
        guests = Guest.query.filter(Guest.id.in_(guest_ids), Guest.event_id == event_id).all()
    else:
        # Send to all guests with email addresses who haven't been sent invitations
        guests = Guest.query.filter_by(event_id=event_id).filter(
            Guest.email.isnot(None),
            Guest.invitation_sent_at.is_(None)
        ).all()
    
    if not guests:
        return jsonify({'message': 'No guests to send invitations to'}), 200
    
    # Send emails
    base_url = request.url_root.rstrip('/')
    stats = email_service.send_bulk_invitations(event, guests, base_url)
    
    # Update invitation_sent_at for successfully sent emails
    for guest in guests:
        if guest.email:
            guest.invitation_sent_at = datetime.utcnow()
            
            # Log email
            email_log = EmailLog(
                event_id=event_id,
                guest_id=guest.id,
                email_type='invitation',
                recipient_email=guest.email,
                status='sent'
            )
            db.session.add(email_log)
    
    db.session.commit()
    
    return jsonify({
        'message': 'Invitations sent',
        'stats': stats
    })

@main.route('/api/events/<event_id>/statistics', methods=['GET'])
@login_required
def get_event_statistics(event_id):
    """Get comprehensive event statistics"""
    event = Event.query.get_or_404(event_id)
    
    # Verify ownership
    if event.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    guests = Guest.query.filter_by(event_id=event_id).all()
    stats = export_service.get_event_statistics(event, guests)
    
    # Add email statistics
    email_logs = EmailLog.query.filter_by(event_id=event_id).all()
    stats['emails_sent'] = len(email_logs)
    stats['emails_opened'] = sum(1 for log in email_logs if log.opened_at)
    
    return jsonify(stats)

@main.route('/api/rsvp/<guest_id>/dietary', methods=['PUT'])
def update_dietary_restrictions(guest_id):
    """Update guest dietary restrictions"""
    guest = Guest.query.get_or_404(guest_id)
    data = request.json
    
    guest.dietary_restrictions = data.get('dietary_restrictions')
    db.session.commit()
    
    return jsonify({'message': 'Dietary restrictions updated', 'guest': guest.to_dict()})


# --- Design Editor Routes ---

@main.route('/design-editor')
@login_required
def design_editor():
    """Design Studio - Create custom designs from scratch"""
    return render_template('design_editor.html')

@main.route('/api/save-design', methods=['POST'])
@login_required
def save_design():
    """Save custom design to database"""
    try:
        data = request.json
        from app.models import CustomDesign
        
        # Check if updating existing design
        design_id = data.get('id')
        if design_id:
            design = CustomDesign.query.get(design_id)
            if design and design.user_id == current_user.id:
                design.title = data.get('title', design.title)
                design.canvas_data = data.get('canvas_data')
                design.thumbnail_url = data.get('thumbnail')
                design.updated_at = datetime.utcnow()
            else:
                return jsonify({'success': False, 'error': 'Design not found or unauthorized'}), 403
        else:
            # Create new design
            design = CustomDesign(
                user_id=current_user.id,
                title=data.get('title', 'Untitled Design'),
                canvas_data=data.get('canvas_data'),
                thumbnail_url=data.get('thumbnail')
            )
            db.session.add(design)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'design_id': design.id,
            'message': 'Design saved successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@main.route('/api/load-design/<design_id>', methods=['GET'])
@login_required
def load_design(design_id):
    """Load custom design from database"""
    try:
        from app.models import CustomDesign
        design = CustomDesign.query.get_or_404(design_id)
        
        # Verify ownership
        if design.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        return jsonify({
            'success': True,
            'design': {
                'id': design.id,
                'title': design.title,
                'canvas_data': design.canvas_data,
                'thumbnail_url': design.thumbnail_url,
                'created_at': design.created_at.isoformat(),
                'updated_at': design.updated_at.isoformat()
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@main.route('/api/my-designs', methods=['GET'])
@login_required
def get_my_designs():
    """Get all designs for current user"""
    try:
        from app.models import CustomDesign
        designs = CustomDesign.query.filter_by(user_id=current_user.id).order_by(
            CustomDesign.updated_at.desc()
        ).all()
        
        return jsonify({
            'success': True,
            'designs': [{
                'id': d.id,
                'title': d.title,
                'thumbnail_url': d.thumbnail_url,
                'created_at': d.created_at.isoformat(),
                'updated_at': d.updated_at.isoformat()
            } for d in designs]
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@main.route('/api/delete-design/<design_id>', methods=['DELETE'])
@login_required
def delete_design(design_id):
    """Delete custom design"""
    try:
        from app.models import CustomDesign
        design = CustomDesign.query.get_or_404(design_id)
        
        # Verify ownership
        if design.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        db.session.delete(design)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Design deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

