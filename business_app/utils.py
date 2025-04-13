import requests
from django.core.files.base import ContentFile
from django.core.files import File
from io import BytesIO

def get_random_image(width=800, height=600, category=None):
    """
    Fetch a random image from Lorem Picsum API
    Args:
        width (int): Desired image width
        height (int): Desired image height
        category (str): Optional category for contextual images (not used by Picsum but kept for future use)
    Returns:
        ContentFile: A Django ContentFile object containing the image
    """
    try:
        # Generate random image URL from Lorem Picsum
        image_url = f'https://picsum.photos/{width}/{height}'
        response = requests.get(image_url, stream=True)
        
        if response.status_code == 200:
            # Create a ContentFile from the image data
            image_content = ContentFile(response.content)
            return image_content
        return None
    except Exception as e:
        print(f'Error fetching random image: {str(e)}')
        return None

def populate_model_images():
    """
    Populate all image fields in the models with random images
    """
    from .models import BusinessInfo, Service, Testimonial, Gallery
    
    # Populate BusinessInfo logo
    business = BusinessInfo.objects.first()
    if business and not business.logo:
        if image_content := get_random_image(400, 400):
            business.logo.save('business_logo.jpg', image_content, save=True)
    
    # Populate Service images
    for service in Service.objects.filter(image__isnull=True):
        if image_content := get_random_image(800, 600):
            service.image.save(f'service_{service.id}.jpg', image_content, save=True)
    
    # Populate Testimonial photos
    for testimonial in Testimonial.objects.filter(photo__isnull=True):
        if image_content := get_random_image(300, 300):
            testimonial.photo.save(f'testimonial_{testimonial.id}.jpg', image_content, save=True)
    
    # Populate Gallery images
    for gallery_item in Gallery.objects.filter(image__isnull=True):
        if image_content := get_random_image(1024, 768):
            gallery_item.image.save(f'gallery_{gallery_item.id}.jpg', image_content, save=True)