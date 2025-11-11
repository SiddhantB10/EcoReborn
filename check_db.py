"""
Database diagnostic script - Check MongoDB connection and collections
"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_database():
    """Check database connection and show collections data."""
    
    mongodb_uri = os.getenv('MONGODB_URI')
    db_name = os.getenv('MONGODB_DB_NAME', 'ecoreborn')
    
    print("="*70)
    print("MONGODB DATABASE DIAGNOSTIC")
    print("="*70)
    
    # Check if environment variables are set
    print("\n1. CHECKING ENVIRONMENT VARIABLES:")
    print("-" * 70)
    if mongodb_uri:
        # Hide password for security
        safe_uri = mongodb_uri
        if '@' in safe_uri:
            parts = safe_uri.split('@')
            if '://' in parts[0]:
                cred_part = parts[0].split('://')[1]
                if ':' in cred_part:
                    user = cred_part.split(':')[0]
                    safe_uri = safe_uri.replace(cred_part, f"{user}:****")
        print(f"✓ MONGODB_URI: {safe_uri}")
    else:
        print("✗ MONGODB_URI: NOT SET")
        print("\n❌ ERROR: MONGODB_URI is not set!")
        print("Please check your .env file.")
        return
    
    print(f"✓ MONGODB_DB_NAME: {db_name}")
    
    # Try to connect
    print("\n2. TESTING DATABASE CONNECTION:")
    print("-" * 70)
    try:
        client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
        client.server_info()
        print("✓ Connection successful!")
        db = client[db_name]
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        print("\n❌ Possible issues:")
        print("   - Check MongoDB Atlas username/password")
        print("   - Check IP whitelist (should have 0.0.0.0/0)")
        print("   - Check database user permissions")
        return
    
    # List all collections
    print("\n3. DATABASE COLLECTIONS:")
    print("-" * 70)
    collections = db.list_collection_names()
    if collections:
        print(f"✓ Found {len(collections)} collection(s):")
        for coll in collections:
            count = db[coll].count_documents({})
            print(f"  • {coll}: {count} document(s)")
    else:
        print("✗ No collections found!")
        print("\n⚠️  Database has not been initialized.")
        print("   Run: python init_db.py")
    
    # Check each collection
    print("\n4. COLLECTION DETAILS:")
    print("-" * 70)
    
    expected_collections = [
        'users',
        'password_reset_tokens',
        'contact_messages',
        'service_requests',
        'newsletter_subscribers',
        'login_attempts'
    ]
    
    for coll_name in expected_collections:
        if coll_name in collections:
            count = db[coll_name].count_documents({})
            print(f"\n✓ {coll_name}:")
            print(f"  Documents: {count}")
            
            # Show sample data (without sensitive info)
            if count > 0:
                sample = db[coll_name].find_one()
                if sample:
                    print(f"  Sample fields: {list(sample.keys())}")
                    
                    # Show specific details for some collections
                    if coll_name == 'users':
                        users = list(db[coll_name].find({}, {'email': 1, 'name': 1}))
                        print("  Users:")
                        for user in users:
                            print(f"    - {user.get('name')} ({user.get('email')})")
                    
                    elif coll_name == 'newsletter_subscribers':
                        subs = list(db[coll_name].find({}, {'email': 1}))
                        print("  Subscribers:")
                        for sub in subs:
                            print(f"    - {sub.get('email')}")
        else:
            print(f"\n✗ {coll_name}: MISSING")
    
    # Final diagnosis
    print("\n" + "="*70)
    print("DIAGNOSIS:")
    print("="*70)
    
    if not collections:
        print("\n❌ ISSUE: Database is empty")
        print("\n📝 SOLUTION:")
        print("   1. Run the initialization script:")
        print("      python init_db.py")
        print("\n   2. If on Render, run in Shell:")
        print("      python init_db.py")
    
    elif len(collections) < len(expected_collections):
        print("\n⚠️  ISSUE: Some collections are missing")
        print("\n📝 SOLUTION:")
        print("   Re-run initialization script:")
        print("   python init_db.py")
    
    else:
        total_docs = sum(db[coll].count_documents({}) for coll in collections)
        if total_docs == 0:
            print("\n⚠️  ISSUE: Collections exist but are empty")
            print("\n📝 SOLUTION:")
            print("   1. Check if init_db.py completed successfully")
            print("   2. Try running again: python init_db.py")
            print("   3. Use the application to create data (signup, contact form, etc.)")
        else:
            print("\n✅ DATABASE IS WORKING PROPERLY!")
            print(f"\n   Total documents: {total_docs}")
            print("   All collections present with data.")
    
    print("="*70)


if __name__ == '__main__':
    check_database()
