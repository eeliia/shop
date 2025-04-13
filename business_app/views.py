from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from .models import (
    BusinessInfo, ServiceCategory, Service, 
    Testimonial, FAQ, Appointment, ContactMessage, Gallery
)

# Home Page View
class HomeView(TemplateView):
    template_name = 'business_app/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get business information
        try:
            context['business'] = BusinessInfo.objects.first()
        except BusinessInfo.DoesNotExist:
            context['business'] = None
            
        # Get featured services
        context['featured_services'] = Service.objects.filter(is_featured=True)[:6]
        
        # Get service categories
        context['service_categories'] = ServiceCategory.objects.all()[:6]
        
        # Get testimonials
        context['testimonials'] = Testimonial.objects.filter(is_active=True)[:6]
        
        # Get FAQs
        context['faqs'] = FAQ.objects.all()[:6]
        
        # Get gallery items
        context['gallery_items'] = Gallery.objects.filter(is_featured=True)[:8]
        
        return context

# About Page View
class AboutView(TemplateView):
    template_name = 'business_app/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['business'] = BusinessInfo.objects.first()
        return context

# Services Views
class ServiceListView(ListView):
    model = Service
    template_name = 'business_app/services.html'
    context_object_name = 'services'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ServiceCategory.objects.all()
        context['business'] = BusinessInfo.objects.first()
        return context

class ServiceDetailView(DetailView):
    model = Service
    template_name = 'business_app/service_detail.html'
    context_object_name = 'service'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['business'] = BusinessInfo.objects.first()
        context['related_services'] = Service.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)[:4]
        return context

# Gallery View
class GalleryView(ListView):
    model = Gallery
    template_name = 'business_app/gallery.html'
    context_object_name = 'gallery_items'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['business'] = BusinessInfo.objects.first()
        context['categories'] = Gallery.objects.values_list('category', flat=True).distinct()
        return context

# Testimonials View
class TestimonialListView(ListView):
    model = Testimonial
    template_name = 'business_app/testimonials.html'
    context_object_name = 'testimonials'
    queryset = Testimonial.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['business'] = BusinessInfo.objects.first()
        return context

# FAQ View
class FAQView(ListView):
    model = FAQ
    template_name = 'business_app/faq.html'
    context_object_name = 'faqs'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['business'] = BusinessInfo.objects.first()
        context['categories'] = FAQ.objects.values_list('category', flat=True).distinct()
        return context

# Appointment Views
class AppointmentCreateView(CreateView):
    model = Appointment
    template_name = 'business_app/appointment_form.html'
    fields = ['service', 'date', 'time', 'name', 'email', 'phone', 'notes']
    success_url = reverse_lazy('appointment_success')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['business'] = BusinessInfo.objects.first()
        context['services'] = Service.objects.all()
        return context
    
    def form_valid(self, form):
        # Check if the user is authenticated
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
        
        messages.success(self.request, 'Your appointment has been scheduled. We will contact you shortly to confirm.')
        return super().form_valid(form)

class AppointmentSuccessView(TemplateView):
    template_name = 'business_app/appointment_success.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['business'] = BusinessInfo.objects.first()
        return context

# Contact Views
class ContactView(CreateView):
    model = ContactMessage
    template_name = 'business_app/contact.html'
    fields = ['name', 'email', 'phone', 'subject', 'message']
    success_url = reverse_lazy('contact_success')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['business'] = BusinessInfo.objects.first()
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Your message has been sent. We will get back to you soon.')
        return super().form_valid(form)

class ContactSuccessView(TemplateView):
    template_name = 'business_app/contact_success.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['business'] = BusinessInfo.objects.first()
        return context
