"""
GitHub backup system for Process scripts.
Automatically backs up database scripts to GitHub repository.
"""
from github import Github, GithubException
from django.conf import settings
from django.utils import timezone
from .models import Process
import logging

logger = logging.getLogger(__name__)


def get_github_client():
    """Get authenticated GitHub client."""
    if not settings.GITHUB_TOKEN:
        raise ValueError("GITHUB_TOKEN not configured in settings")
    
    if not settings.GITHUB_USERNAME:
        raise ValueError("GITHUB_USERNAME not configured in settings")
    
    return Github(settings.GITHUB_TOKEN)


def get_or_create_repository(github_client, repo_name):
    """
    Get existing repository or create new one.
    
    Args:
        github_client: Authenticated GitHub client
        repo_name: Name of the repository
    
    Returns:
        Repository object
    """
    user = github_client.get_user()
    
    try:
        # Try to get existing repository
        repo = user.get_repo(repo_name)
        logger.info(f"Found existing repository: {repo_name}")
        return repo
    except GithubException as e:
        if e.status == 404:
            # Repository doesn't exist, create it
            logger.info(f"Creating new repository: {repo_name}")
            repo = user.create_repo(
                repo_name,
                description="Automated backup of process scripts from Django Webhook Service",
                private=False,
                auto_init=True  # Initialize with README
            )
            return repo
        else:
            raise


def backup_processes_to_github():
    """
    Backup all processes from database to GitHub repository.
    Creates new files or updates existing ones.
    
    Returns:
        dict with backup results
    """
    try:
        # Get GitHub client
        github_client = get_github_client()
        
        # Get or create repository
        repo = get_or_create_repository(github_client, settings.GITHUB_REPO)
        
        # Get all processes from database
        processes = Process.objects.all()
        
        if not processes.exists():
            logger.warning("No processes found in database to backup")
            return {
                'status': 'success',
                'message': 'No processes to backup',
                'backed_up': 0,
                'created': 0,
                'updated': 0
            }
        
        created_count = 0
        updated_count = 0
        errors = []
        
        for process in processes:
            try:
                filename = f"{process.code}.py"
                content = process.script
                commit_message = f"Backup: {process.code} - {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}"
                
                # Try to get existing file
                try:
                    file = repo.get_contents(filename)
                    # File exists, update it
                    if file.decoded_content.decode('utf-8') != content:
                        repo.update_file(
                            path=filename,
                            message=commit_message,
                            content=content,
                            sha=file.sha
                        )
                        updated_count += 1
                        logger.info(f"Updated: {filename}")
                    else:
                        logger.info(f"No changes: {filename}")
                except GithubException as e:
                    if e.status == 404:
                        # File doesn't exist, create it
                        repo.create_file(
                            path=filename,
                            message=commit_message,
                            content=content
                        )
                        created_count += 1
                        logger.info(f"Created: {filename}")
                    else:
                        raise
                        
            except Exception as e:
                error_msg = f"Error backing up {process.code}: {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)
        
        result = {
            'status': 'success' if not errors else 'partial',
            'message': f'Backed up {created_count + updated_count} processes',
            'backed_up': created_count + updated_count,
            'created': created_count,
            'updated': updated_count,
            'total': processes.count(),
            'repository_url': repo.html_url
        }
        
        if errors:
            result['errors'] = errors
        
        logger.info(f"Backup completed: {result}")
        return result
        
    except Exception as e:
        error_msg = f"GitHub backup failed: {str(e)}"
        logger.error(error_msg)
        raise Exception(error_msg)


def create_sample_processes():
    """
    Create sample process records for testing.
    """
    processes = [
        {
            'name': 'Hello World Script',
            'code': 'hello_world',
            'script': '''#!/usr/bin/env python3
"""
Simple Hello World script.
"""

def main():
    print("Hello, World!")
    print("This is a sample process script.")
    
if __name__ == "__main__":
    main()
'''
        },
        {
            'name': 'Data Processor',
            'code': 'data_processor',
            'script': '''#!/usr/bin/env python3
"""
Data processing script.
"""
import json
from datetime import datetime

def process_data(data):
    """Process incoming data."""
    print(f"Processing data at {datetime.now()}")
    
    # Sample processing logic
    results = []
    for item in data:
        processed_item = {
            'original': item,
            'processed': item.upper() if isinstance(item, str) else item,
            'timestamp': datetime.now().isoformat()
        }
        results.append(processed_item)
    
    return results

def main():
    sample_data = ['hello', 'world', 'python', 'django']
    results = process_data(sample_data)
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
'''
        }
    ]
    
    created = []
    for process_data in processes:
        process, created_flag = Process.objects.get_or_create(
            code=process_data['code'],
            defaults={
                'name': process_data['name'],
                'script': process_data['script']
            }
        )
        if created_flag:
            created.append(process.code)
            logger.info(f"Created process: {process.code}")
        else:
            logger.info(f"Process already exists: {process.code}")
    
    return {
        'created': created,
        'total': len(processes)
    }

