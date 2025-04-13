from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import User

# Business Information Models
class BusinessInfo(models.Model):
    """Store basic information about the business"""
    name = models.CharField(_('Business Name'), max_length=100)
    logo = models.ImageField(_('Logo'), upload_to='business/logos/', blank=True, null=True)
    slogan = models.CharField(_('Slogan'), max_length=200, blank=True)
    description = models.TextField(_('Description'))
    established_date = models.DateField(_('Established Date'), blank=True, null=True)
    
    # Contact Information
    email = models.EmailField(_('Email'), blank=True)
    phone = models.CharField(_('Phone'), max_length=20, blank=True)
    address = models.TextField(_('Address'), blank=True)
    
    # Social Media
    facebook = models.URLField(_('Facebook'), blank=True)
    instagram = models.URLField(_('Instagram'), blank=True)
    twitter = models.URLField(_('Twitter'), blank=True)
    linkedin = models.URLField(_('LinkedIn'), blank=True)
    
    # SEO Fields
    meta_description = models.TextField(_('Meta Description'), max_length=160, blank=True, 
                                      help_text=_('Description for search engines, max 160 characters'))
    meta_keywords = models.CharField(_('Meta Keywords'), max_length=255, blank=True,
                                   help_text=_('Keywords for search engines, comma separated'))
    
    class Meta:
        verbose_name = _('Business Information')
        verbose_name_plural = _('Business Information')
    
    def __str__(self):
        return self.name

class BusinessHours(models.Model):
    """Store business operating hours"""
    DAYS_OF_WEEK = (
        (0, _('Monday')),
        (1, _('Tuesday')),
        (2, _('Wednesday')),
        (3, _('Thursday')),
        (4, _('Friday')),
        (5, _('Saturday')),
        (6, _('Sunday')),
    )
    
    business = models.ForeignKey(BusinessInfo, on_delete=models.CASCADE, related_name='hours')
    day = models.IntegerField(_('Day'), choices=DAYS_OF_WEEK)
    opening_time = models.TimeField(_('Opening Time'))
    closing_time = models.TimeField(_('Closing Time'))
    is_closed = models.BooleanField(_('Closed'), default=False)
    
    class Meta:
        verbose_name = _('Business Hours')
        verbose_name_plural = _('Business Hours')
        ordering = ['day']
        unique_together = ['business', 'day']
    
    def __str__(self):
        if self.is_closed:
            return f"{self.get_day_display()}: Closed"
        return f"{self.get_day_display()}: {self.opening_time.strftime('%H:%M')} - {self.closing_time.strftime('%H:%M')}"

# Service Models
class ServiceCategory(models.Model):
    """Categories for services offered"""
    name = models.CharField(_('Name'), max_length=100)
    description = models.TextField(_('Description'), blank=True)
    icon = models.CharField(_('Icon Class'), max_length=50, blank=True, 
                          help_text=_('Font Awesome or other icon class'))
    order = models.PositiveIntegerField(_('Display Order'), default=0)
    
    class Meta:
        verbose_name = _('Service Category')
        verbose_name_plural = _('Service Categories')
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name

class Service(models.Model):
    """Services offered by the business"""
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(_('Name'), max_length=100)
    description = models.TextField(_('Description'))
    price = models.DecimalField(_('Price'), max_digits=10, decimal_places=2, blank=True, null=True)
    duration = models.DurationField(_('Duration'), blank=True, null=True, 
                                  help_text=_('Approximate duration of the service'))
    image = models.ImageField(_('Image'), upload_to='services/', blank=True, null=True)
    is_featured = models.BooleanField(_('Featured'), default=False)
    order = models.PositiveIntegerField(_('Display Order'), default=0)
    
    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')
        ordering = ['category', 'order', 'name']
    
    def __str__(self):
        return self.name

# Content Models
class Testimonial(models.Model):
    """Customer testimonials"""
    name = models.CharField(_('Customer Name'), max_length=100)
    position = models.CharField(_('Position/Company'), max_length=100, blank=True)
    photo = models.ImageField(_('Photo'), upload_to='testimonials/', blank=True, null=True)
    content = models.TextField(_('Testimonial'))
    rating = models.PositiveSmallIntegerField(_('Rating'), default=5, 
                                            help_text=_('Rating from 1-5'))
    date = models.DateField(_('Date'), default=timezone.now)
    is_active = models.BooleanField(_('Active'), default=True)
    
    class Meta:
        verbose_name = _('Testimonial')
        verbose_name_plural = _('Testimonials')
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.name} - {self.rating}/5"

class FAQ(models.Model):
    """Frequently Asked Questions"""
    question = models.CharField(_('Question'), max_length=255)
    answer = models.TextField(_('Answer'))
    category = models.CharField(_('Category'), max_length=100, blank=True)
    order = models.PositiveIntegerField(_('Display Order'), default=0)
    
    class Meta:
        verbose_name = _('FAQ')
        verbose_name_plural = _('FAQs')
        ordering = ['order', 'question']
    
    def __str__(self):
        return self.question

# Booking System Models
class Appointment(models.Model):
    """Customer appointments/bookings"""
    STATUS_CHOICES = (
        ('pending', _('Pending')),
        ('confirmed', _('Confirmed')),
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled')),
    )
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                            related_name='appointments')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField(_('Date'))
    time = models.TimeField(_('Time'))
    name = models.CharField(_('Name'), max_length=100)
    email = models.EmailField(_('Email'))
    phone = models.CharField(_('Phone'), max_length=20)
    notes = models.TextField(_('Notes'), blank=True)
    status = models.CharField(_('Status'), max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    
    class Meta:
        verbose_name = _('Appointment')
        verbose_name_plural = _('Appointments')
        ordering = ['date', 'time']
    
    def __str__(self):
        return f"{self.name} - {self.service.name} on {self.date} at {self.time}"

# Contact and Messaging Models
class ContactMessage(models.Model):
    """Messages from the contact form"""
    name = models.CharField(_('Name'), max_length=100)
    email = models.EmailField(_('Email'))
    phone = models.CharField(_('Phone'), max_length=20, blank=True)
    subject = models.CharField(_('Subject'), max_length=200)
    message = models.TextField(_('Message'))
    created_at = models.DateTimeField(_('Sent At'), auto_now_add=True)
    is_read = models.BooleanField(_('Read'), default=False)
    
    class Meta:
        verbose_name = _('Contact Message')
        verbose_name_plural = _('Contact Messages')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"

# Gallery Models
class Gallery(models.Model):
    """Photo gallery for the business"""
    title = models.CharField(_('Title'), max_length=100)
    description = models.TextField(_('Description'), blank=True)
    image = models.ImageField(_('Image'), upload_to='gallery/')
    category = models.CharField(_('Category'), max_length=100, blank=True)
    order = models.PositiveIntegerField(_('Display Order'), default=0)
    is_featured = models.BooleanField(_('Featured'), default=False)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Gallery Item')
        verbose_name_plural = _('Gallery')
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.title

# Template Customization Model
class TemplateSettings(models.Model):
    """Settings for website template customization"""
    # Primary Colors
    primary_color = models.CharField(_('Primary Color'), max_length=20, default='#6200ee',
                                  help_text=_('Main color for buttons and highlights (hex code)'))
    primary_variant_color = models.CharField(_('Primary Variant Color'), max_length=20, default='#3700b3',
                                          help_text=_('Darker variant of primary color (hex code)'))
    secondary_color = models.CharField(_('Secondary Color'), max_length=20, default='#03dac6',
                                    help_text=_('Accent color for secondary elements (hex code)'))
    secondary_variant_color = models.CharField(_('Secondary Variant Color'), max_length=20, default='#018786',
                                            help_text=_('Darker variant of secondary color (hex code)'))
    
    # Background Colors
    background_color = models.CharField(_('Background Color'), max_length=20, default='#ffffff',
                                     help_text=_('Main background color (hex code)'))
    surface_color = models.CharField(_('Surface Color'), max_length=20, default='#ffffff',
                                   help_text=_('Surface elements color (hex code)'))
    error_color = models.CharField(_('Error Color'), max_length=20, default='#b00020',
                                help_text=_('Color for error states (hex code)'))
    
    # Text Colors
    on_primary_color = models.CharField(_('On Primary Color'), max_length=20, default='#ffffff',
                                      help_text=_('Text color on primary background (hex code)'))
    on_secondary_color = models.CharField(_('On Secondary Color'), max_length=20, default='#000000',
                                        help_text=_('Text color on secondary background (hex code)'))
    on_background_color = models.CharField(_('On Background Color'), max_length=20, default='#000000',
                                         help_text=_('Text color on main background (hex code)'))
    on_surface_color = models.CharField(_('On Surface Color'), max_length=20, default='#000000',
                                       help_text=_('Text color on surface elements (hex code)'))
    on_error_color = models.CharField(_('On Error Color'), max_length=20, default='#ffffff',
                                    help_text=_('Text color on error elements (hex code)'))
    
    # Typography
    font_family = models.CharField(_('Font Family'), max_length=100, default='Vazirmatn, sans-serif',
                                help_text=_('Main font family for the website'))
    heading_font_family = models.CharField(_('Heading Font Family'), max_length=100, blank=True,
                                        help_text=_('Font family for headings (leave blank to use main font)'))
    
    # Layout
    border_radius = models.CharField(_('Border Radius'), max_length=20, default='8px',
                                  help_text=_('Border radius for elements (e.g., 8px)'))
    
    # Hero Section
    hero_background_image = models.ImageField(_('Hero Background Image'), upload_to='template/',
                                           blank=True, null=True,
                                           help_text=_('Background image for the hero section'))
    hero_overlay_opacity = models.DecimalField(_('Hero Overlay Opacity'), max_digits=3, decimal_places=2,
                                            default=0.5, help_text=_('Opacity for the dark overlay on hero image (0-1)'))
    
    # Custom CSS
    custom_css = models.TextField(_('Custom CSS'), blank=True,
                               help_text=_('Additional custom CSS for the website'))
    
    # Footer
    footer_background_color = models.CharField(_('Footer Background Color'), max_length=20, default='#212529',
                                            help_text=_('Background color for the footer (hex code)'))
    footer_text_color = models.CharField(_('Footer Text Color'), max_length=20, default='#ffffff',
                                       help_text=_('Text color for the footer (hex code)'))
    
    # Last Updated
    updated_at = models.DateTimeField(_('Last Updated'), auto_now=True)
    
    class Meta:
        verbose_name = _('Template Settings')
        verbose_name_plural = _('Template Settings')
    
    def __str__(self):
        return _('Template Settings')
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and TemplateSettings.objects.exists():
            # Update existing instance instead of creating a new one
            self.pk = TemplateSettings.objects.first().pk
        super().save(*args, **kwargs)
