"""
Management command to backup processes to GitHub.
Usage: python manage.py backup_processes
"""
from django.core.management.base import BaseCommand
from apps.integrations.github_backup import backup_processes_to_github


class Command(BaseCommand):
    help = 'Backup process scripts to GitHub repository'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Starting GitHub backup...'))
        
        try:
            result = backup_processes_to_github()
            
            self.stdout.write(self.style.SUCCESS('✓ Backup completed successfully'))
            self.stdout.write(f"  Total processes: {result['total']}")
            self.stdout.write(f"  Created: {result['created']}")
            self.stdout.write(f"  Updated: {result['updated']}")
            self.stdout.write(f"  Repository: {result['repository_url']}")
            
            if result.get('errors'):
                self.stdout.write(self.style.WARNING('\nErrors encountered:'))
                for error in result['errors']:
                    self.stdout.write(f"  - {error}")
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Backup failed: {str(e)}'))
            raise

