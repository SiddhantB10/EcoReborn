"""
Utility functions for email, file handling, and security.
"""

import os
import secrets
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename


def send_email(to_email, subject, body, html_body=None):
    """
    Send email via SMTP or log to file if SMTP not configured.
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        body: Plain text email body
        html_body: HTML email body (optional)
    """
    from flask import current_app
    
    smtp_host = current_app.config.get('SMTP_HOST')
    
    # If SMTP is configured, send actual email
    if smtp_host:
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            smtp_port = current_app.config.get('SMTP_PORT', 587)
            smtp_user = current_app.config.get('SMTP_USER')
            smtp_pass = current_app.config.get('SMTP_PASS')
            smtp_from = current_app.config.get('SMTP_FROM', 'noreply@ecoreborn.example')
            
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = smtp_from
            msg['To'] = to_email
            
            # Attach plain text
            part1 = MIMEText(body, 'plain')
            msg.attach(part1)
            
            # Attach HTML if provided
            if html_body:
                part2 = MIMEText(html_body, 'html')
                msg.attach(part2)
            
            # Send email
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.send_message(msg)
            
            current_app.logger.info(f'Email sent to {to_email}: {subject}')
            return True
            
        except Exception as e:
            current_app.logger.error(f'Failed to send email: {str(e)}')
            # Fall back to logging
    
    # Log email to file (development mode or SMTP failure)
    log_email_to_file(to_email, subject, body, html_body)
    return True


def log_email_to_file(to_email, subject, body, html_body=None):
    """Log email to file for development/testing (or console in production)."""
    from flask import current_app
    
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    
    # In production (Vercel), log to console only (read-only filesystem)
    if os.getenv('FLASK_ENV') == 'production':
        current_app.logger.info(f'Email would be sent to: {to_email}')
        current_app.logger.info(f'Subject: {subject}')
        current_app.logger.info(f'Body: {body[:100]}...')  # Log first 100 chars
    else:
        # In development, log to file
        log_dir = os.path.join(current_app.root_path, 'logs')
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, 'email.log')
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f'\n{"="*80}\n')
            f.write(f'Timestamp: {timestamp}\n')
            f.write(f'To: {to_email}\n')
            f.write(f'Subject: {subject}\n')
            f.write(f'{"-"*80}\n')
            f.write(f'{body}\n')
            if html_body:
                f.write(f'{"-"*80}\n')
                f.write(f'HTML Version:\n{html_body}\n')
            f.write(f'{"="*80}\n\n')
        
        current_app.logger.info(f'Email logged to file: {to_email} - {subject}')


def generate_reset_token():
    """Generate a secure random token for password reset."""
    return secrets.token_urlsafe(32)


def allowed_file(filename, allowed_extensions=None):
    """
    Check if uploaded file has allowed extension.
    
    Args:
        filename: Name of the file
        allowed_extensions: Set of allowed extensions (default: common safe types)
    
    Returns:
        Boolean indicating if file is allowed
    """
    if allowed_extensions is None:
        allowed_extensions = {'pdf', 'doc', 'docx', 'txt', 'jpg', 'jpeg', 'png', 'gif'}
    
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def save_uploaded_file(file_storage, upload_folder):
    """
    Save uploaded file securely.
    In production (Vercel), files can't be saved to disk (read-only filesystem).
    File uploads are disabled in production - use cloud storage instead.
    
    Args:
        file_storage: FileStorage object from request.files
        upload_folder: Directory to save files
    
    Returns:
        Filename if successful, None otherwise
    """
    if not file_storage or file_storage.filename == '':
        return None
    
    if not allowed_file(file_storage.filename):
        return None
    
    # In production (Vercel), skip file saving (read-only filesystem)
    # You would need to integrate with cloud storage (AWS S3, Cloudinary, etc.)
    if os.getenv('FLASK_ENV') == 'production':
        from flask import current_app
        current_app.logger.warning('File upload attempted in production - files not saved (use cloud storage)')
        # Return a dummy filename so the form doesn't break
        return secure_filename(file_storage.filename)
    
    # In development, save files locally
    # Secure the filename
    filename = secure_filename(file_storage.filename)
    
    # Add timestamp to prevent collisions
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    name, ext = os.path.splitext(filename)
    filename = f"{name}_{timestamp}{ext}"
    
    # Ensure upload directory exists
    os.makedirs(upload_folder, exist_ok=True)
    
    # Save file
    filepath = os.path.join(upload_folder, filename)
    file_storage.save(filepath)
    
    return filename


def sanitize_filename(filename):
    """Sanitize filename to prevent directory traversal attacks."""
    return secure_filename(filename)


def format_datetime(dt, format='%B %d, %Y at %I:%M %p'):
    """Format datetime for display."""
    if dt is None:
        return ''
    return dt.strftime(format)


def get_client_ip(request):
    """Get client IP address, considering proxies."""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    else:
        return request.remote_addr


def generate_sitemap_xml(base_url, routes):
    """
    Generate sitemap.xml content.
    
    Args:
        base_url: Base URL of the site
        routes: List of tuples (path, priority, changefreq)
    
    Returns:
        XML string
    """
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for path, priority, changefreq in routes:
        xml += '  <url>\n'
        xml += f'    <loc>{base_url}{path}</loc>\n'
        xml += f'    <priority>{priority}</priority>\n'
        xml += f'    <changefreq>{changefreq}</changefreq>\n'
        xml += '  </url>\n'
    
    xml += '</urlset>'
    return xml


def create_password_reset_email(reset_url, user_name):
    """Create password reset email content."""
    subject = "Password Reset Request - Ecoreborn"
    
    body = f"""Hello {user_name},

You recently requested to reset your password for your Ecoreborn account.

Click the link below to reset your password:
{reset_url}

This link will expire in 1 hour.

If you did not request a password reset, please ignore this email or contact us if you have concerns.

Best regards,
The Ecoreborn Team

---
Ecoreborn — Reborn fabrics. Reborn future.
"""
    
    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <h2 style="color: #2d5016;">Password Reset Request</h2>
        <p>Hello {user_name},</p>
        <p>You recently requested to reset your password for your Ecoreborn account.</p>
        <p>Click the button below to reset your password:</p>
        <p style="margin: 30px 0;">
            <a href="{reset_url}" 
               style="background-color: #2d5016; color: white; padding: 12px 24px; 
                      text-decoration: none; border-radius: 4px; display: inline-block;">
                Reset Password
            </a>
        </p>
        <p>Or copy and paste this link into your browser:</p>
        <p style="background-color: #f5f5f5; padding: 10px; border-radius: 4px; word-break: break-all;">
            {reset_url}
        </p>
        <p><strong>This link will expire in 1 hour.</strong></p>
        <p>If you did not request a password reset, please ignore this email or contact us if you have concerns.</p>
        <hr style="margin: 30px 0; border: none; border-top: 1px solid #ddd;">
        <p style="color: #666; font-size: 14px;">
            Best regards,<br>
            The Ecoreborn Team<br>
            <em>Ecoreborn — Reborn fabrics. Reborn future.</em>
        </p>
    </body>
    </html>
    """
    
    return subject, body, html_body


def create_contact_confirmation_email(name):
    """Create contact form confirmation email."""
    subject = "Thank you for contacting Ecoreborn"
    
    body = f"""Hello {name},

Thank you for reaching out to Ecoreborn!

We have received your message and will get back to you as soon as possible, typically within 24-48 hours.

In the meantime, feel free to explore our services and learn more about our sustainable textile recycling process at our website.

Best regards,
The Ecoreborn Team

---
Ecoreborn — Reborn fabrics. Reborn future.
"""
    
    return subject, body


def create_service_request_confirmation_email(name, service_name):
    """Create service request confirmation email."""
    subject = f"Service Request Received - {service_name}"
    
    body = f"""Hello {name},

Thank you for your interest in our {service_name} service!

We have received your request and our team will review it shortly. We'll be in touch within 1-2 business days to discuss your needs and next steps.

If you have any urgent questions, please feel free to contact us directly.

Best regards,
The Ecoreborn Team

---
Ecoreborn — Reborn fabrics. Reborn future.
"""
    
    return subject, body
