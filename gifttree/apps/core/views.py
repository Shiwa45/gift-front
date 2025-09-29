from django.shortcuts import render
from django.views.generic import TemplateView
from .models import SiteSettings
from apps.products.models import Product, Category, Occasion


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Site settings
        context['site_settings'] = SiteSettings.get_settings()
        
        # Featured products
        context['featured_products'] = Product.objects.filter(
            is_featured=True, 
            is_active=True,
            stock_quantity__gt=0
        ).select_related('category').prefetch_related('images')[:8]
        
        # Bestseller products
        context['bestseller_products'] = Product.objects.filter(
            is_bestseller=True, 
            is_active=True,
            stock_quantity__gt=0
        ).select_related('category').prefetch_related('images')[:8]
        
        # Main categories are now provided by context processor
        
        # Quick categories for action grid
        context['quick_categories'] = Category.objects.filter(
            is_featured=True,
            is_active=True
        ).prefetch_related('products')[:8]
        
        # Banner images (if you have a banner model, otherwise will use defaults)
        # context['banner_images'] = BannerImage.objects.filter(is_active=True)[:4]
        
        # Cart count is now provided by context processor
        
        return context


def home_view(request):
    """Simple home view with enhanced context"""
    # Featured products
    featured_products = Product.objects.filter(
        is_featured=True, 
        is_active=True,
        stock_quantity__gt=0
    ).select_related('category').prefetch_related('images')[:8]
    
    # Bestseller products
    bestseller_products = Product.objects.filter(
        is_bestseller=True, 
        is_active=True,
        stock_quantity__gt=0
    ).select_related('category').prefetch_related('images')[:8]
    
    # Main categories are now provided by context processor
    
    # Quick categories for action grid
    quick_categories = Category.objects.filter(
        is_featured=True,
        is_active=True
    ).prefetch_related('products')[:8]
    
    # Cart count is now provided by context processor
    
    context = {
        'site_settings': SiteSettings.get_settings(),
        'featured_products': featured_products,
        'bestseller_products': bestseller_products,
        'quick_categories': quick_categories,
    }
    return render(request, 'core/home.html', context)