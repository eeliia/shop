import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check if Firebase is already initialized
if not firebase_admin._apps:
    # Path to service account key file
    # Note: In production, use environment variables or secure storage for credentials
    # For development, you can place your service account key in the project root
    try:
        # Try to initialize with service account file if available
        cred = credentials.Certificate('firebase-service-account.json')
        firebase_app = firebase_admin.initialize_app(cred, {
            'storageBucket': os.getenv('FIREBASE_STORAGE_BUCKET')
        })
    except (FileNotFoundError, ValueError):
        # If service account file is not available, use environment variables
        # This is useful for production environments like Firebase Hosting
        firebase_app = firebase_admin.initialize_app()

# Get Firestore database instance
def get_firestore_db():
    return firestore.client()

# Get Firebase Storage bucket
def get_storage_bucket():
    return storage.bucket()