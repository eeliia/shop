from django.contrib import admin
from .models import (
    BusinessInfo, BusinessHours, ServiceCategory, Service,
    Testimonial, FAQ, Appointment, ContactMessage, Gallery,
    TemplateSettings
)

# Business Information Admin
class BusinessHoursInline(admin.TabularInline):
    model = BusinessHours
    extra = 7  # One for each day of the week

@admin.register(BusinessInfo)
class BusinessInfoAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'logo', 'slogan', 'description', 'established_date')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'address')
        }),
        ('Social Media', {
            'fields': ('facebook', 'instagram', 'twitter', 'linkedin')
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords')
        }),
    )
    inlines = [BusinessHoursInline]

# Service Admin
@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    search_fields = ('name',)

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_featured', 'order')
    list_filter = ('category', 'is_featured')
    search_fields = ('name', 'description')
    list_editable = ('is_featured', 'order')

admin.site.register(Service, ServiceAdmin)

# Content Admin
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'date', 'is_active')
    list_filter = ('rating', 'is_active')
    search_fields = ('name', 'content')
    list_editable = ('is_active',)

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'order')
    list_filter = ('category',)
    search_fields = ('question', 'answer')
    list_editable = ('order',)

# Booking System Admin
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'service', 'date', 'time', 'status')
    list_filter = ('status', 'date', 'service')
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('status',)
    date_hierarchy = 'date'

# Contact Admin
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)
    list_editable = ('is_read',)

# Gallery Admin
@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_featured', 'order')
    list_filter = ('category', 'is_featured')
    search_fields = ('title', 'description')
    list_editable = ('is_featured', 'order')

# Template Settings Admin
@admin.register(TemplateSettings)
class TemplateSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Colors', {
            'fields': (
                'primary_color', 'primary_variant_color',
                'secondary_color', 'secondary_variant_color',
                'background_color', 'surface_color', 'error_color'
            ),
            'classes': ('wide',)
        }),
        ('Text Colors', {
            'fields': (
                'on_primary_color', 'on_secondary_color',
                'on_background_color', 'on_surface_color', 'on_error_color'
            ),
            'classes': ('wide',)
        }),
        ('Typography', {
            'fields': ('font_family', 'heading_font_family'),
            'classes': ('wide',)
        }),
        ('Layout', {
            'fields': ('border_radius',),
            'classes': ('wide',)
        }),
        ('Hero Section', {
            'fields': ('hero_background_image', 'hero_overlay_opacity'),
            'classes': ('wide',)
        }),
        ('Footer', {
            'fields': ('footer_background_color', 'footer_text_color'),
            'classes': ('wide',)
        }),
        ('Advanced', {
            'fields': ('custom_css',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('updated_at',)
    
    def has_add_permission(self, request):
        # Prevent creating multiple instances
        return not TemplateSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deleting the instance
        return False
