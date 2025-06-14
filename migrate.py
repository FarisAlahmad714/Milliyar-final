#!/usr/bin/env python
"""
Script to run Django migrations on Vercel deployment
"""
import os
import django
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EcomProj.settings')
    django.setup()
    
    # Run migrations
    execute_from_command_line(['manage.py', 'migrate', '--noinput'])
    
    # Create superuser if it doesn't exist
    from django.contrib.auth.models import User
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("Superuser created: admin/admin123")