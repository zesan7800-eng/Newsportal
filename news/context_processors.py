from .models import Category

def categories_processor(request):
    """
    This function runs on every request
    and sends categories to all templates
    """
    categories = Category.objects.all()
    return {
        'categories': categories
    }
