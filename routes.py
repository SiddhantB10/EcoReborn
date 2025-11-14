"""
Main application routes: home, services, contact, dashboard.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user

from models import ContactMessage, ServiceRequest, NewsletterSubscriber
from forms import ContactForm, ServiceRequestForm, NewsletterForm
from utils import (
    save_uploaded_file, send_email,
    create_contact_confirmation_email,
    create_service_request_confirmation_email
)


main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home():
    """Home page - public."""
    newsletter_form = NewsletterForm()
    return render_template('home.html', newsletter_form=newsletter_form, title='Home')


@main_bp.route('/services', methods=['GET', 'POST'])
def services():
    """Services page - public with request form."""
    form = ServiceRequestForm()
    
    if form.validate_on_submit():
        db = current_app.db
        
        # Create service request
        request_id = ServiceRequest.create(
            db,
            service_name=form.service_name.data,
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            company=form.company.data,
            message=form.message.data
        )
        
        if request_id:
            # Send confirmation email to user
            subject, body = create_service_request_confirmation_email(
                form.name.data,
                form.service_name.data
            )
            send_email(form.email.data, subject, body)
            
            # Notify admin
            admin_email = current_app.config.get('ADMIN_EMAIL', 'admin@ecoreborn.example')
            admin_subject = f"New Service Request: {form.service_name.data}"
            admin_body = f"""New service request received:

Service: {form.service_name.data}
Name: {form.name.data}
Email: {form.email.data}
Phone: {form.phone.data or 'Not provided'}
Company: {form.company.data or 'Not provided'}

Message:
{form.message.data}

---
Request ID: {request_id}
"""
            send_email(admin_email, admin_subject, admin_body)
            
            flash('Your service request has been submitted successfully! We will contact you soon.', 'success')
            return redirect(url_for('main.services'))
        else:
            flash('An error occurred. Please try again.', 'error')
    
    # Define services
    services_list = [
        {
            'id': 'fabric-recycling',
            'name': 'Fabric Recycling',
            'description': 'We collect and recycle discarded textiles, converting them into high-quality fibers for re-spinning. Perfect for fashion brands looking to reduce waste.',
            'pricing': 'Volume-based pricing. Contact us for a custom quote.'
        },
        {
            'id': 'custom-fabric',
            'name': 'Custom Re-spun Fabric Orders',
            'description': 'Order custom re-spun fabrics made from recycled materials. Choose your specifications, colors, and quantities.',
            'pricing': 'Starting from ₹250/meter. Minimum order: 50 meters.'
        },
        {
            'id': 'b2b-partnerships',
            'name': 'B2B Partnerships',
            'description': 'Partner with us to integrate sustainable practices into your supply chain. We work with fashion brands, manufacturers, and retailers.',
            'pricing': 'Custom partnership packages available.'
        },
        {
            'id': 'consulting',
            'name': 'Consulting for Textile Brands',
            'description': 'Expert consulting on sustainable textile practices, circular economy implementation, and waste reduction strategies.',
            'pricing': '₹5,000/day or custom project rates.'
        },
        {
            'id': 'collection-drives',
            'name': 'Student/Community Collection Drives',
            'description': 'We organize and support textile collection drives for schools, colleges, and community organizations. Educational workshops included.',
            'pricing': 'Free for educational institutions and nonprofits.'
        }
    ]
    
    return render_template('services.html', form=form, services=services_list, title='Services')


@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page - public."""
    form = ContactForm()
    
    if form.validate_on_submit():
        db = current_app.db
        
        # Handle file upload
        filename = None
        if form.attachment.data:
            upload_folder = current_app.config.get('UPLOAD_FOLDER', './uploads')
            filename = save_uploaded_file(form.attachment.data, upload_folder)
        
        # Save contact message
        message_id = ContactMessage.create(
            db,
            name=form.name.data,
            email=form.email.data,
            subject=form.subject.data,
            message=form.message.data,
            filename=filename
        )
        
        if message_id:
            # Send confirmation to user
            subject, body = create_contact_confirmation_email(form.name.data)
            send_email(form.email.data, subject, body)
            
            # Notify admin
            admin_email = current_app.config.get('ADMIN_EMAIL', 'admin@ecoreborn.example')
            admin_subject = f"New Contact Message: {form.subject.data}"
            admin_body = f"""New contact form submission:

From: {form.name.data} <{form.email.data}>
Subject: {form.subject.data}

Message:
{form.message.data}

{f"Attachment: {filename}" if filename else "No attachment"}

---
Message ID: {message_id}
"""
            send_email(admin_email, admin_subject, admin_body)
            
            flash('Thank you for your message! We will get back to you soon.', 'success')
            return redirect(url_for('main.contact'))
        else:
            flash('An error occurred. Please try again.', 'error')
    
    return render_template('contact.html', form=form, title='Contact Us')


@main_bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard - protected."""
    db = current_app.db
    
    # Get user's service requests
    service_requests = ServiceRequest.get_by_user_email(db, current_user.email, limit=10)
    
    return render_template(
        'dashboard.html',
        service_requests=service_requests,
        title='Dashboard'
    )


@main_bp.route('/newsletter/subscribe', methods=['POST'])
def newsletter_subscribe():
    """Newsletter subscription endpoint."""
    form = NewsletterForm()
    
    if form.validate_on_submit():
        db = current_app.db
        
        result = NewsletterSubscriber.subscribe(db, form.email.data)
        
        if result:
            flash('Thank you for subscribing to our newsletter!', 'success')
        else:
            flash('You are already subscribed to our newsletter.', 'info')
    else:
        flash('Please enter a valid email address.', 'error')
    
    # Redirect back to the page they came from
    return redirect(request.referrer or url_for('main.home'))


@main_bp.route('/sitemap.xml')
def sitemap():
    """Generate sitemap.xml."""
    from flask import Response
    from utils import generate_sitemap_xml
    
    base_url = current_app.config.get('APP_URL', 'http://localhost:5000')
    
    routes = [
        ('/', '1.0', 'daily'),
        ('/services', '0.9', 'weekly'),
        ('/contact', '0.8', 'monthly'),
        ('/login', '0.5', 'monthly'),
        ('/signup', '0.5', 'monthly'),
    ]
    
    xml_content = generate_sitemap_xml(base_url, routes)
    
    return Response(xml_content, mimetype='application/xml')


@main_bp.route('/robots.txt')
def robots():
    """Generate robots.txt."""
    from flask import Response
    
    content = """User-agent: *
Allow: /
Disallow: /dashboard
Disallow: /logout
Disallow: /reset-password/

Sitemap: {}/sitemap.xml
""".format(current_app.config.get('APP_URL', 'http://localhost:5000'))
    
    return Response(content, mimetype='text/plain')


# Error handlers
@main_bp.app_errorhandler(404)
def not_found_error(error):
    """Handle 404 errors."""
    return render_template('errors/404.html', title='Page Not Found'), 404


@main_bp.app_errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    current_app.logger.error(f'Server Error: {error}')
    return render_template('errors/500.html', title='Server Error'), 500


@main_bp.app_errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large errors."""
    flash('The uploaded file is too large. Maximum size is 2MB.', 'error')
    return redirect(url_for('main.contact'))
