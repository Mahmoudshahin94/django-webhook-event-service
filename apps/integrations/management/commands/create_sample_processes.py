"""
Management command to create sample process records.
Usage: python manage.py create_sample_processes
"""
from django.core.management.base import BaseCommand
from apps.integrations.github_backup import create_sample_processes


class Command(BaseCommand):
    help = 'Create sample process records in the database'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Creating sample processes...'))
        
        try:
            result = create_sample_processes()
            
            self.stdout.write(self.style.SUCCESS('✓ Sample processes created'))
            self.stdout.write(f"  Total processes: {result['total']}")
            
            if result['created']:
                self.stdout.write(f"  New processes: {', '.join(result['created'])}")
            else:
                self.stdout.write('  All processes already existed')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error: {str(e)}'))
            raise

