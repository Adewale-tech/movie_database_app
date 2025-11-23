"""
WSGI config for movie_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_project.settings')

application = get_wsgi_application()

# Vercel: Run migrations on startup (because /tmp/db.sqlite3 is ephemeral)
if os.getenv('VERCEL'):
    from django.core.management import call_command
    try:
        call_command('migrate')
        print("Migrations executed successfully.")
    except Exception as e:
        print(f"Error running migrations: {e}")

app = application
