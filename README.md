# Ecoreborn Website

**Ecoreborn — Reborn fabrics. Reborn future.**

A fully server-side rendered sustainable fashion website built with Flask and MongoDB Atlas. Zero client-side JavaScript for maximum accessibility and performance.

🌐 **Live Demo**: [https://ecoreborn.onrender.com](https://ecoreborn.onrender.com)

## Features

- 🔐 Secure authentication (bcrypt password hashing, CSRF protection)
- 📧 Server-side password reset with email simulation
- 🌍 Public pages: Home, Services, Contact
- 👤 Protected user dashboard
- 📝 Contact form with file upload support
- 🔄 Service request system
- 📰 Newsletter subscription
- ♿ Fully accessible (semantic HTML5, ARIA labels)
- 📱 Mobile-first responsive design
- 🔒 Security best practices (rate limiting, input validation, secure sessions)
- 🎨 CSS-only interactions (no JavaScript)

## Tech Stack

- **Backend**: Python 3.11+ with Flask
- **Database**: MongoDB Atlas
- **Template Engine**: Jinja2
- **Authentication**: Flask-Login with bcrypt
- **Forms**: Flask-WTF (CSRF protection)
- **Session**: Server-side sessions with secure cookies

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- MongoDB Atlas account (free tier works)

## Installation

### 1. Clone or extract the project

```bash
cd ecoreborn-website
```

### 2. Create virtual environment

```bash
python -m venv .venv
```

### 3. Activate virtual environment

**Windows:**
```cmd
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Copy the example environment file:

```bash
copy .env.example .env
```

Edit `.env` and update the following:

```env
# Required: Generate a secure random key
SECRET_KEY=your-secret-key-here

# Required: MongoDB Atlas connection string
MONGODB_URI=mongodb+srv://db_user:db_pass@ecoreborn.dkjdd4s.mongodb.net/ecoreborn?retryWrites=true&w=majority

# Optional: Email configuration (leave blank to use file logging)
SMTP_HOST=
SMTP_PORT=587
SMTP_USER=
SMTP_PASS=
SMTP_FROM=noreply@ecoreborn.example

# Optional: Configuration
FLASK_ENV=development
UPLOAD_FOLDER=./uploads
MAX_FILE_SIZE=2097152
```

**To generate a secure SECRET_KEY:**

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 6. Initialize the database

```bash
python init_db.py
```

This will:
- Create necessary collections
- Seed an admin user (email: `admin@ecoreborn.example`, password: `Ec0r3b0rn!`)
- Add sample service data

### 7. Run the application

```bash
python app.py
```

Or use the Flask CLI:

```bash
flask run
```

The application will be available at: **http://localhost:5000**

## Project Structure

```
ecoreborn-website/
├── app.py                 # Main application entry point
├── models.py              # Database models
├── forms.py               # WTForms definitions
├── auth.py                # Authentication routes
├── routes.py              # Main application routes
├── utils.py               # Helper functions
├── init_db.py             # Database initialization script
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore            # Git ignore file
├── LICENSE               # MIT License
├── CHANGELOG.md          # Version history
├── DEPLOYMENT.md         # Deployment guide
├── MAINTAINERS.md        # Maintenance guide
├── TODO.md               # Optional improvements
├── sitemap.xml           # SEO sitemap
├── robots.txt            # Search engine rules
├── templates/            # Jinja2 templates
│   ├── base.html
│   ├── home.html
│   ├── services.html
│   ├── contact.html
│   ├── login.html
│   ├── signup.html
│   ├── forgot_password.html
│   ├── reset_password.html
│   ├── dashboard.html
│   └── errors/
│       ├── 404.html
│       └── 500.html
├── static/               # Static assets
│   ├── css/
│   │   ├── main.css
│   │   └── print.css
│   ├── images/
│   │   ├── hero-bg.svg
│   │   ├── process-*.svg
│   │   └── map-placeholder.png
│   └── fonts/            # Web fonts (if self-hosted)
├── logs/                 # Application logs
│   └── email.log
├── uploads/              # User-uploaded files
├── tests/                # Test suite
│   ├── test_auth.py
│   ├── test_forms.py
│   └── test_routes.py
└── docs/                 # Documentation
    └── screenshots/
```

## Testing

Run the test suite:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=. --cov-report=html
```

## Default Admin Credentials

**For development/testing only:**

- Email: `admin@ecoreborn.example`
- Password: `Ec0r3b0rn!`

**⚠️ Change these credentials immediately in production!**

## Email Configuration

By default, the application logs emails to `logs/email.log` if SMTP is not configured. This is useful for development.

To enable actual email sending:
1. Set up an SMTP service (Gmail, SendGrid, Mailgun, etc.)
2. Update `.env` with SMTP credentials
3. Restart the application

## Security Features

- ✅ Bcrypt password hashing
- ✅ CSRF protection on all forms
- ✅ Secure session cookies (HttpOnly, Secure in production)
- ✅ Rate limiting on login attempts
- ✅ Input validation and sanitization
- ✅ File upload restrictions (2MB, safe extensions)
- ✅ SQL injection prevention (ORM)
- ✅ XSS prevention (template auto-escaping)

## Deployment

This project is **ready to deploy** to:

### ☁️ Recommended: Render
One-click deployment with `render.yaml`:
- See [DEPLOYMENT.md](DEPLOYMENT.md) for step-by-step guide
- Automatic builds on git push
- Free tier available

### ⚡ Vercel
Serverless deployment with `vercel.json`:
- Deploy with Vercel CLI or GitHub integration
- See [DEPLOYMENT.md](DEPLOYMENT.md) for configuration

### 📦 Other Platforms
Also supports:
- Heroku (with `Procfile`)
- Railway
- Any Linux VPS (Ubuntu + Gunicorn + Nginx)

**All deployment files are included and ready to use!**

## Maintenance

See [MAINTAINERS.md](MAINTAINERS.md) for:
- Updating brand colors and fonts
- Modifying content and copy
- Adding new services
- Database backup procedures

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Works without JavaScript enabled

## Accessibility

- ♿ WCAG 2.1 AA compliant
- 🎯 Semantic HTML5
- 🏷️ ARIA labels where needed
- ⌨️ Keyboard navigation
- 📱 Mobile-first responsive design

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Live Demo

🌐 **Production Site**: [https://ecoreborn.onrender.com](https://ecoreborn.onrender.com)

## Support

For issues or questions:
- GitHub Issues: [https://github.com/SiddhantB10/EcoReborn/issues](https://github.com/SiddhantB10/EcoReborn/issues)
- Repository: [https://github.com/SiddhantB10/EcoReborn](https://github.com/SiddhantB10/EcoReborn)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

---

**Made with ♻️ by Ecoreborn Team**
