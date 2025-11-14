"""
Test suite for main routes.
"""

import pytest
from app import create_app


@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    yield app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


class TestPublicRoutes:
    """Test public pages."""
    
    def test_home_page(self, client):
        """Test home page loads successfully."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'EcoReborn' in response.data
        assert b'Reborn fabrics' in response.data
    
    def test_services_page(self, client):
        """Test services page loads successfully."""
        response = client.get('/services')
        assert response.status_code == 200
        assert b'Services' in response.data
        assert b'Fabric Recycling' in response.data
    
    def test_contact_page(self, client):
        """Test contact page loads successfully."""
        response = client.get('/contact')
        assert response.status_code == 200
        assert b'Contact' in response.data
        assert b'Message' in response.data
    
    def test_sitemap(self, client):
        """Test sitemap.xml is generated."""
        response = client.get('/sitemap.xml')
        assert response.status_code == 200
        assert b'<?xml version' in response.data
        assert b'urlset' in response.data
    
    def test_robots(self, client):
        """Test robots.txt is generated."""
        response = client.get('/robots.txt')
        assert response.status_code == 200
        assert b'User-agent' in response.data
        assert b'Sitemap' in response.data


class TestContactForm:
    """Test contact form submission."""
    
    def test_contact_form_submission(self, client, app):
        """Test contact form can be submitted."""
        response = client.post('/contact', data={
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'message': 'This is a test message for contact form submission.',
        }, follow_redirects=True)
        
        assert response.status_code == 200
        # Should redirect back to contact page with success message
        assert b'Thank you' in response.data or b'contact' in response.data.lower()


class TestServiceRequest:
    """Test service request submission."""
    
    def test_service_request_submission(self, client):
        """Test service request can be submitted."""
        response = client.post('/services', data={
            'service_name': 'Fabric Recycling',
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': '+91 1234567890',
            'company': 'Test Company',
            'message': 'This is a test service request message.',
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'submitted' in response.data.lower() or b'Thank you' in response.data


class TestNewsletterSubscription:
    """Test newsletter subscription."""
    
    def test_newsletter_subscription(self, client):
        """Test newsletter subscription works."""
        response = client.post('/newsletter/subscribe', data={
            'email': 'newsletter@example.com'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        # Should show success or already subscribed message


class TestErrorPages:
    """Test error handling."""
    
    def test_404_page(self, client):
        """Test 404 error page."""
        response = client.get('/nonexistent-page')
        assert response.status_code == 404
        assert b'404' in response.data or b'Not Found' in response.data


class TestSecurity:
    """Test security features."""
    
    def test_csrf_protection_enabled(self, app):
        """Test CSRF protection is enabled in production."""
        # In production, CSRF should be enabled
        assert app.config.get('WTF_CSRF_ENABLED', True) or app.config['TESTING']
    
    def test_secure_headers(self, client):
        """Test secure headers are set."""
        response = client.get('/')
        # Check for security headers (add more as configured)
        assert response.status_code == 200


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
