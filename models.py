"""
Database models for EcoReborn application.
Uses MongoDB with PyMongo for data persistence.
"""

from datetime import datetime
from bson import ObjectId
import bcrypt


class User:
    """User model for authentication and profile management."""
    
    COLLECTION = 'users'
    
    @staticmethod
    def create(db, email, password, name):
        """
        Create a new user with hashed password.
        
        Args:
            db: MongoDB database instance
            email: User email (unique)
            password: Plain text password (will be hashed)
            name: User's full name
            
        Returns:
            User document ID if successful, None otherwise
        """
        # Check if user already exists
        if db[User.COLLECTION].find_one({'email': email.lower()}):
            return None
        
        # Hash password using bcrypt
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        user_doc = {
            'email': email.lower(),
            'password_hash': password_hash,
            'name': name,
            'is_active': True,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = db[User.COLLECTION].insert_one(user_doc)
        return result.inserted_id
    
    @staticmethod
    def find_by_email(db, email):
        """Find user by email address."""
        return db[User.COLLECTION].find_one({'email': email.lower()})
    
    @staticmethod
    def find_by_id(db, user_id):
        """Find user by ObjectId."""
        if isinstance(user_id, str):
            user_id = ObjectId(user_id)
        return db[User.COLLECTION].find_one({'_id': user_id})
    
    @staticmethod
    def verify_password(stored_hash, password):
        """Verify password against stored hash."""
        return bcrypt.checkpw(password.encode('utf-8'), stored_hash)
    
    @staticmethod
    def update_password(db, user_id, new_password):
        """Update user password."""
        if isinstance(user_id, str):
            user_id = ObjectId(user_id)
        
        password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        
        db[User.COLLECTION].update_one(
            {'_id': user_id},
            {
                '$set': {
                    'password_hash': password_hash,
                    'updated_at': datetime.utcnow()
                }
            }
        )
        return True
    
    @staticmethod
    def update_last_login(db, email):
        """Update user's last login timestamp."""
        db[User.COLLECTION].update_one(
            {'email': email.lower()},
            {
                '$set': {
                    'last_login': datetime.utcnow(),
                    'updated_at': datetime.utcnow()
                }
            }
        )
        return True


class PasswordResetToken:
    """Password reset token management."""
    
    COLLECTION = 'password_reset_tokens'
    
    @staticmethod
    def create(db, user_id, token, expires_at):
        """Create a password reset token."""
        if isinstance(user_id, str):
            user_id = ObjectId(user_id)
        
        # Invalidate old tokens for this user
        db[PasswordResetToken.COLLECTION].delete_many({'user_id': user_id})
        
        token_doc = {
            'user_id': user_id,
            'token': token,
            'expires_at': expires_at,
            'used': False,
            'created_at': datetime.utcnow()
        }
        
        result = db[PasswordResetToken.COLLECTION].insert_one(token_doc)
        return result.inserted_id
    
    @staticmethod
    def find_valid_token(db, token):
        """Find a valid, unused token."""
        return db[PasswordResetToken.COLLECTION].find_one({
            'token': token,
            'used': False,
            'expires_at': {'$gt': datetime.utcnow()}
        })
    
    @staticmethod
    def mark_as_used(db, token):
        """Mark token as used."""
        db[PasswordResetToken.COLLECTION].update_one(
            {'token': token},
            {'$set': {'used': True}}
        )


class ContactMessage:
    """Contact form submissions."""
    
    COLLECTION = 'contact_messages'
    
    @staticmethod
    def create(db, name, email, subject, message, filename=None):
        """Create a new contact message."""
        message_doc = {
            'name': name,
            'email': email,
            'subject': subject,
            'message': message,
            'filename': filename,
            'status': 'unread',
            'created_at': datetime.utcnow()
        }
        
        result = db[ContactMessage.COLLECTION].insert_one(message_doc)
        return result.inserted_id
    
    @staticmethod
    def get_all(db, limit=100):
        """Get all contact messages."""
        return list(db[ContactMessage.COLLECTION].find().sort('created_at', -1).limit(limit))


class ServiceRequest:
    """Service request submissions."""
    
    COLLECTION = 'service_requests'
    
    @staticmethod
    def create(db, service_name, name, email, phone, company, message):
        """Create a new service request."""
        request_doc = {
            'service_name': service_name,
            'name': name,
            'email': email,
            'phone': phone,
            'company': company,
            'message': message,
            'status': 'pending',
            'created_at': datetime.utcnow()
        }
        
        result = db[ServiceRequest.COLLECTION].insert_one(request_doc)
        return result.inserted_id
    
    @staticmethod
    def get_by_user_email(db, email, limit=50):
        """Get service requests by user email."""
        return list(db[ServiceRequest.COLLECTION].find({'email': email}).sort('created_at', -1).limit(limit))


class NewsletterSubscriber:
    """Newsletter subscription management."""
    
    COLLECTION = 'newsletter_subscribers'
    
    @staticmethod
    def subscribe(db, email):
        """Subscribe an email to newsletter."""
        # Check if already subscribed
        existing = db[NewsletterSubscriber.COLLECTION].find_one({'email': email.lower()})
        if existing:
            if existing.get('unsubscribed', False):
                # Resubscribe
                db[NewsletterSubscriber.COLLECTION].update_one(
                    {'email': email.lower()},
                    {
                        '$set': {
                            'unsubscribed': False,
                            'updated_at': datetime.utcnow()
                        }
                    }
                )
                return True
            return False  # Already subscribed
        
        subscriber_doc = {
            'email': email.lower(),
            'unsubscribed': False,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = db[NewsletterSubscriber.COLLECTION].insert_one(subscriber_doc)
        return result.inserted_id
    
    @staticmethod
    def unsubscribe(db, email):
        """Unsubscribe an email from newsletter."""
        db[NewsletterSubscriber.COLLECTION].update_one(
            {'email': email.lower()},
            {
                '$set': {
                    'unsubscribed': True,
                    'updated_at': datetime.utcnow()
                }
            }
        )


class LoginAttempt:
    """Track login attempts for rate limiting."""
    
    COLLECTION = 'login_attempts'
    
    @staticmethod
    def record_attempt(db, email, success, ip_address):
        """Record a login attempt."""
        attempt_doc = {
            'email': email.lower(),
            'success': success,
            'ip_address': ip_address,
            'timestamp': datetime.utcnow()
        }
        
        db[LoginAttempt.COLLECTION].insert_one(attempt_doc)
    
    @staticmethod
    def get_recent_failed_attempts(db, email, minutes=15):
        """Get count of recent failed login attempts."""
        from datetime import timedelta
        cutoff = datetime.utcnow() - timedelta(minutes=minutes)
        
        count = db[LoginAttempt.COLLECTION].count_documents({
            'email': email.lower(),
            'success': False,
            'timestamp': {'$gte': cutoff}
        })
        
        return count
    
    @staticmethod
    def clear_attempts(db, email):
        """Clear login attempts for an email (after successful login)."""
        db[LoginAttempt.COLLECTION].delete_many({'email': email.lower()})
