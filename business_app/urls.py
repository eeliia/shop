from django.urls import path
from . import views

urlpatterns = [
    # Home and About
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    
    # Services
    path('services/', views.ServiceListView.as_view(), name='services'),
    path('services/<int:pk>/', views.ServiceDetailView.as_view(), name='service_detail'),
    
    # Gallery
    path('gallery/', views.GalleryView.as_view(), name='gallery'),
    
    # Testimonials
    path('testimonials/', views.TestimonialListView.as_view(), name='testimonials'),
    
    # FAQ
    path('faq/', views.FAQView.as_view(), name='faq'),
    
    # Appointment
    path('appointment/', views.AppointmentCreateView.as_view(), name='appointment'),
    path('appointment/success/', views.AppointmentSuccessView.as_view(), name='appointment_success'),
    
    # Contact
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('contact/success/', views.ContactSuccessView.as_view(), name='contact_success'),
]

# Media files are served from the main project's urls.py