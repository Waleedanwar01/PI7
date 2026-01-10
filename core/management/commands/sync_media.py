import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files import File

class Command(BaseCommand):
    help = 'Syncs local media files to Cloudinary'

    def handle(self, *args, **options):
        media_root = settings.MEDIA_ROOT
        if not os.path.exists(media_root):
            self.stdout.write(self.style.WARNING(f"Media root {media_root} does not exist."))
            return

        self.stdout.write(f"Scanning {media_root} for files to upload...")

        for root, dirs, files in os.walk(media_root):
            for filename in files:
                # Skip hidden files
                if filename.startswith('.'):
                    continue

                full_path = os.path.join(root, filename)
                relative_path = os.path.relpath(full_path, media_root)
                
                # Convert backslashes to forward slashes for storage consistency
                storage_path = relative_path.replace('\\', '/')

                try:
                    if not default_storage.exists(storage_path):
                        self.stdout.write(f"Uploading {storage_path}...")
                        with open(full_path, 'rb') as f:
                            saved_name = default_storage.save(storage_path, File(f))
                            if saved_name != storage_path:
                                self.stdout.write(self.style.WARNING(f"  Warning: Saved as {saved_name} instead of {storage_path}"))
                            else:
                                self.stdout.write(self.style.SUCCESS(f"  Successfully uploaded {storage_path}"))
                    else:
                        self.stdout.write(f"Skipping {storage_path} (already exists)")
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Failed to upload {storage_path}: {str(e)}"))
