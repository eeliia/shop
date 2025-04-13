from .models import BusinessInfo, TemplateSettings

def template_settings(request):
    """
    Context processor that adds template settings to all templates
    """
    try:
        # Get the template settings or create default if not exists
        settings = TemplateSettings.objects.first()
        if not settings:
            settings = TemplateSettings.objects.create()
            
        # Create a CSS variables string for inline styling
        css_variables = f"""
        :root {{
            --md-primary: {settings.primary_color};
            --md-primary-variant: {settings.primary_variant_color};
            --md-secondary: {settings.secondary_color};
            --md-secondary-variant: {settings.secondary_variant_color};
            --md-background: {settings.background_color};
            --md-surface: {settings.surface_color};
            --md-error: {settings.error_color};
            --md-on-primary: {settings.on_primary_color};
            --md-on-secondary: {settings.on_secondary_color};
            --md-on-background: {settings.on_background_color};
            --md-on-surface: {settings.on_surface_color};
            --md-on-error: {settings.on_error_color};
            --md-border-radius: {settings.border_radius};
            --md-footer-bg: {settings.footer_background_color};
            --md-footer-text: {settings.footer_text_color};
        }}
        """
        
        # Add custom font family if specified
        font_styles = ""
        if settings.font_family:
            font_styles += f"body {{ font-family: {settings.font_family}; }}\n"
        
        if settings.heading_font_family:
            font_styles += f"h1, h2, h3, h4, h5, h6 {{ font-family: {settings.heading_font_family}; }}\n"
        
        # Combine all custom CSS
        custom_css = css_variables + font_styles
        if settings.custom_css:
            custom_css += settings.custom_css
            
        # Get hero image URL if exists
        hero_image_url = settings.hero_background_image.url if settings.hero_background_image else None
        hero_overlay_opacity = settings.hero_overlay_opacity
        
        return {
            'template_settings': settings,
            'custom_css': custom_css,
            'hero_image_url': hero_image_url,
            'hero_overlay_opacity': hero_overlay_opacity,
        }
    except Exception as e:
        # Return empty context in case of error
        return {
            'template_settings': None,
            'custom_css': '',
            'hero_image_url': None,
            'hero_overlay_opacity': 0.5,
        }