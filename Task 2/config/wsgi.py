"""
WSGI config for config project with Vercel serverless deployment support.
"""

import os
import sys
from pathlib import Path

# Ensure Task 2 directory is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
app = application

# Auto-migrate and seed sample data on Vercel cold-start if using /tmp SQLite
if 'VERCEL' in os.environ or os.getenv('VERCEL') == '1':
    try:
        from django.core.management import call_command
        call_command('migrate', interactive=False)
        
        from students.models import Student
        from datetime import date
        if not Student.objects.exists():
            Student.objects.bulk_create([
                Student(student_id='STU1001', first_name='Alexander', last_name='Hamilton', email='alexander@university.edu', phone='+12025550101', date_of_birth=date(2001,1,11), course='Computer Science', year=3),
                Student(student_id='STU1002', first_name='Elizabeth', last_name='Schuyler', email='elizabeth@university.edu', phone='+12025550102', date_of_birth=date(2002,8,9), course='Data Science', year=2),
                Student(student_id='STU1003', first_name='Aaron', last_name='Burr', email='aaron.burr@university.edu', phone='+12025550103', date_of_birth=date(2000,2,6), course='Law & Governance', year=4),
                Student(student_id='STU1004', first_name='Angelica', last_name='Church', email='angelica@university.edu', phone='+12025550104', date_of_birth=date(1999,2,20), course='Computer Science', year=5),
            ])
    except Exception as exc:
        print("Vercel auto-migration/seed notification:", exc)
