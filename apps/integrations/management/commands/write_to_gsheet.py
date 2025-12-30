"""
Management command to write sample data to Google Sheet.
Usage: python manage.py write_to_gsheet
"""
from django.core.management.base import BaseCommand
from apps.integrations.google_sheets import write_sample_data


class Command(BaseCommand):
    help = 'Write sample data to Google Sheet with formatting'

    def add_arguments(self, parser):
        parser.add_argument(
            '--sheet-name',
            type=str,
            default='Webhook Service Test Sheet',
            help='Name of the Google Sheet'
        )

    def handle(self, *args, **options):
        sheet_name = options['sheet_name']
        
        self.stdout.write(self.style.WARNING(f'Writing sample data to Google Sheet: {sheet_name}...'))
        
        try:
            result = write_sample_data()
            
            self.stdout.write(self.style.SUCCESS('✓ Successfully wrote data to Google Sheet'))
            self.stdout.write(f"  Sheet URL: {result['url']}")
            self.stdout.write(f"  Rows written: {result['rows']}")
            self.stdout.write(f"  Columns: {result['cols']}")
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error: {str(e)}'))
            raise

