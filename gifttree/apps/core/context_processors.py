from apps.products.models import Category


def global_context(request):
    """
    Global context processor to provide common data to all templates
    """
    # Get main categories for navigation
    main_categories = Category.objects.filter(
        parent=None,
        is_active=True
    ).prefetch_related('children')[:6]
    
    # Get cart count
    cart_count = 0
    if hasattr(request, 'session') and 'cart' in request.session:
        cart_count = sum(item.get('quantity', 0) for item in request.session['cart'].values())
    
    return {
        'main_categories': main_categories,
        'cart_count': cart_count,
    }