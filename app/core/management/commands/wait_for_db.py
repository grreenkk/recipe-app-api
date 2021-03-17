import time

from django.db import connections # This is what we use to test if the dtatbase connection is available
from django.db.utils import OperationalError # This is the error that will be thrown if the database is not available
from django.core.management.base import BaseCommand # This is the class we have to build on in other to create our
# custom base command

class Command(BaseCommand):
    """Django command to pause execution until database is available"""

    def handle(self, *args, **options):
        self.stdout.write('Waiting for Database...')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available'))
