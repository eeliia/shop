import random
import requests
from io import BytesIO
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from business_app.models import Gallery
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Populates the gallery with random images from Unsplash'
    
    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=10, help='Number of images to add')
        parser.add_argument('--category', type=str, default='', help='Category for the images')
    
    def handle(self, *args, **options):
        count = options['count']
        category = options['category']
        
        # Categories to use if none specified
        categories = ['interior', 'exterior', 'products', 'team', 'work']
        
        self.stdout.write(self.style.SUCCESS(f'Adding {count} images to the gallery...'))
        
        for i in range(count):
            # Choose a random category if none specified
            img_category = category if category else random.choice(categories)
            
            # Generate a title
            title = f'{img_category.title()} Image {i+1}'
            
            # Get a random image from Unsplash
            width = 800
            height = 600
            url = f'https://source.unsplash.com/random/{width}x{height}/?{img_category}'
            
            try:
                # Download the image
                response = requests.get(url)
                if response.status_code == 200:
                    # Create a new gallery item
                    gallery_item = Gallery(
                        title=title,
                        description=f'A beautiful {img_category} image for our gallery.',
                        category=img_category,
                        order=i,
                        is_featured=(i < 5)  # First 5 images are featured
                    )
                    
                    # Save the image to the gallery item
                    image_name = f"{slugify(title)}.jpg"
                    gallery_item.image.save(image_name, ContentFile(response.content), save=True)
                    
                    self.stdout.write(self.style.SUCCESS(f'Added image: {title}'))
                else:
                    self.stdout.write(self.style.ERROR(f'Failed to download image {i+1}: HTTP {response.status_code}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error adding image {i+1}: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS(f'Successfully added {count} images to the gallery!'))