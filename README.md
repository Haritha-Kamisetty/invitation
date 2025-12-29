# Professional Event Invitation Platform 🎉

A modern, feature-rich web application for creating and managing event invitations with professional features inspired by Evite.

## ✨ Features

### Core Features
- 🎨 **Beautiful Templates** - Multiple professionally designed templates for birthdays, weddings, anniversaries, and baby showers
- 📍 **Smart Location** - Venue autocomplete using OpenStreetMap (free, no API key required)
- 🗺️ **Interactive Maps** - Automatic map display with directions
- 📧 **Email Invitations** - Send professional HTML email invitations
- ✅ **RSVP Management** - Track guest responses with dietary restrictions
- 💬 **Guest Comments** - Interactive guestbook for messages
- 📊 **Analytics Dashboard** - Track views, RSVPs, and engagement

### Professional Features
- 📥 **Guest Import/Export** - Import guests from CSV, export to Excel/PDF
- 🔗 **QR Codes** - Generate QR codes for easy invitation sharing
- 📱 **Responsive Design** - Works perfectly on all devices
- 🍽️ **Dietary Tracking** - Collect and manage dietary restrictions
- 📈 **Statistics** - Comprehensive event analytics
- 🎯 **Personalized Links** - Unique invitation links for each guest
- 📧 **Email Tracking** - Track sent invitations and confirmations

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or download the project**
   ```bash
   cd "c:\Users\Suneel Reddy\Downloads\invitation web"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Email (Optional but recommended)**
   
   Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```
   
   Edit `.env` and add your email credentials:
   
   **For Gmail:**
   - Enable 2-factor authentication
   - Generate an App Password at https://myaccount.google.com/apppasswords
   - Update `.env` with your Gmail and app password
   
   **For SendGrid (Professional):**
   - Sign up at https://sendgrid.com (100 emails/day free)
   - Get your API key
   - Update `.env` with SendGrid settings

4. **Run the application**
   ```bash
   python run.py
   ```

5. **Open in browser**
   ```
   http://localhost:5000
   ```

## 📖 Usage Guide

### Creating an Event

1. **Sign Up/Login**
   - Create an account or login
   - Access your dashboard

2. **Choose a Template**
   - Browse templates by category
   - Select your favorite design

3. **Customize Your Invitation**
   - Add event details (date, time, venue)
   - Use venue autocomplete for accurate locations
   - Add a personal message
   - Preview in real-time

4. **Manage Guests**
   - Add guests manually
   - Import from CSV file
   - Send email invitations

5. **Track Responses**
   - View RSVP statistics
   - See dietary restrictions
   - Export guest list to Excel

### Guest Features

1. **Receive Invitation**
   - Get beautiful HTML email
   - Click to view full invitation

2. **RSVP**
   - Select attendance status
   - Add plus ones
   - Specify dietary restrictions
   - Leave a message

3. **Confirmation**
   - Receive RSVP confirmation email
   - View event details
   - Get directions to venue

## 📁 Project Structure

```
invitation web/
├── app/
│   ├── __init__.py           # App initialization
│   ├── models.py             # Database models
│   ├── routes.py             # API endpoints
│   ├── email_service.py      # Email functionality
│   ├── export_service.py     # Import/Export features
│   ├── venue_service.py      # Location services
│   ├── static/
│   │   ├── css/              # Stylesheets
│   │   ├── js/               # JavaScript
│   │   ├── uploads/          # User uploads
│   │   └── qrcodes/          # Generated QR codes
│   └── templates/
│       ├── emails/           # Email templates
│       ├── base.html         # Base template
│       ├── index.html        # Homepage
│       ├── editor.html       # Event editor
│       ├── invite.html       # Invitation view
│       └── dashboard.html    # Event dashboard
├── config.py                 # Configuration
├── requirements.txt          # Dependencies
├── run.py                    # Application entry point
└── .env.example             # Environment variables template
```

## 🔧 API Endpoints

### Events
- `POST /api/events` - Create event
- `GET /api/events/<id>` - Get event details
- `GET /api/events/<id>/statistics` - Get event statistics

### Guests
- `POST /api/events/<id>/guests` - Add guest
- `GET /api/events/<id>/guests` - List guests
- `POST /api/events/<id>/guests/import` - Import from CSV
- `GET /api/events/<id>/guests/export` - Export to Excel/CSV

### RSVP
- `POST /api/events/<id>/rsvp` - Submit RSVP
- `PUT /api/rsvp/<guest_id>/dietary` - Update dietary restrictions

### Venue
- `GET /api/venues/autocomplete?q=<query>` - Search venues
- `POST /api/venues/geocode` - Geocode address

### Email & Sharing
- `POST /api/events/<id>/send-invitations` - Send email invitations
- `GET /api/events/<id>/qrcode` - Generate QR code

## 🎨 Customization

### Adding New Templates

Edit `app/static/js/app.js` and add to the `TEMPLATES` object:

```javascript
birthday: [
    {
        id: 'my_template',
        title: 'My Custom Template',
        style: 'Modern',
        text: "Your invitation text with {{placeholders}}",
        image: 'https://your-image-url.com/image.jpg'
    }
]
```

### Email Templates

Edit HTML templates in `app/templates/emails/`:
- `invitation_email.html` - Invitation emails
- `rsvp_confirmation_email.html` - RSVP confirmations

## 📊 CSV Import Format

Create a CSV file with these columns:

```csv
Name,Email,Phone,Dietary Restrictions,Notes
John Doe,john@example.com,+1234567890,Vegetarian,Close friend
Jane Smith,jane@example.com,+0987654321,Gluten-free,College roommate
```

**Required:** Name  
**Optional:** Email, Phone, Dietary Restrictions, Notes

## 🔒 Security Features

- Password hashing with Werkzeug
- CSRF protection
- SQL injection prevention
- XSS protection
- Secure session cookies
- File upload validation

## 🌐 Deployment

### Production Checklist

1. **Update `.env`**
   - Set strong `SECRET_KEY`
   - Configure production email service
   - Set `FLASK_ENV=production`

2. **Database**
   - Consider PostgreSQL for production
   - Set up regular backups

3. **Security**
   - Enable HTTPS
   - Set `SESSION_COOKIE_SECURE=True`
   - Configure proper CORS settings

4. **Email**
   - Use SendGrid or similar service
   - Verify sender domain

## 🐛 Troubleshooting

### Email not sending
- Check `.env` configuration
- Verify Gmail app password (not regular password)
- Check spam folder
- Ensure 2FA is enabled for Gmail

### Map not showing
- Check venue address format
- Try more specific address
- Verify internet connection
- Check browser console for errors

### CSV import failing
- Ensure CSV has "Name" column
- Check file encoding (UTF-8)
- Verify no special characters in names

## 📝 License

This project is open source and available for personal and commercial use.

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the code comments
3. Check browser console for errors

## 🎯 Future Enhancements

- [ ] Photo gallery for events
- [ ] Calendar integration (.ics files)
- [ ] SMS notifications
- [ ] Multi-language support
- [ ] Custom domain support
- [ ] Payment integration for paid events
- [ ] Seating chart planner
- [ ] Gift registry integration

---

**Made with ❤️ for creating memorable events**
