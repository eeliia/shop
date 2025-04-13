#!/usr/bin/env python
"""
Script to create a Django admin superuser
"""
import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'local_business_website.settings')
django.setup()

# Import User model
from django.contrib.auth.models import User

def create_superuser():
    username = 'admin'
    email = 'admin@example.com'
    password = 'Admin123!'
    
    # Check if admin user already exists
    if User.objects.filter(username=username).exists():
        print(f'Admin user with username "{username}" already exists.')
        return
    
    # Create superuser
    try:
        admin_user = User.objects.create_superuser(username, email, password)
        print(f'Successfully created superuser:')
        print(f'Username: {username}')
        print(f'Email: {email}')
        print(f'Password: {password}')
        print('\nYou can now log in to the admin panel at: http://127.0.0.1:8000/admin/')
    except Exception as e:
        print(f'Error creating superuser: {e}')

if __name__ == '__main__':
    create_superuser()