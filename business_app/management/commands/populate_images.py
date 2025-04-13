from django.core.management.base import BaseCommand
from business_app.utils import populate_model_images

class Command(BaseCommand):
    help = 'Populate all image fields in models with random images from Lorem Picsum'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to populate random images...'))
        
        # Call the utility function to populate images
        populate_model_images()
        
        self.stdout.write(self.style.SUCCESS('Successfully populated random images!'))