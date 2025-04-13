// Main JavaScript for Local Business Website

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Gallery image modal
    const galleryImages = document.querySelectorAll('.gallery-item img');
    galleryImages.forEach(img => {
        img.addEventListener('click', function() {
            const modal = new bootstrap.Modal(document.getElementById('imageModal'));
            const modalImg = document.getElementById('modalImage');
            modalImg.src = this.src;
            modal.show();
        });
    });

    // Appointment date validation
    const appointmentDate = document.getElementById('id_date');
    if (appointmentDate) {
        appointmentDate.addEventListener('change', function() {
            const selected = new Date(this.value);
            const now = new Date();
            if (selected < now) {
                this.value = '';
                alert('لطفاً تاریخی در آینده را انتخاب کنید.');
            }
        });
    }

    // Service filter
    const serviceFilters = document.querySelectorAll('.service-filter');
    serviceFilters.forEach(filter => {
        filter.addEventListener('click', function(e) {
            e.preventDefault();
            const category = this.dataset.category;
            const services = document.querySelectorAll('.service-item');
            
            serviceFilters.forEach(f => f.classList.remove('active'));
            this.classList.add('active');

            services.forEach(service => {
                if (category === 'all' || service.dataset.category === category) {
                    service.style.display = 'block';
                } else {
                    service.style.display = 'none';
                }
            });
        });
    });

    // Back to top button
    const backToTop = document.getElementById('back-to-top');
    if (backToTop) {
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 100) {
                backToTop.classList.add('show');
            } else {
                backToTop.classList.remove('show');
            }
        });

        backToTop.addEventListener('click', function(e) {
            e.preventDefault();
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
});