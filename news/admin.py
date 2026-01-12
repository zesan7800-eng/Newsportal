from django.contrib import admin
from .models import Category, Article, JournalistProfile


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'is_published', 'created_at')
    list_filter = ('category', 'is_published', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}

    def save_model(self, request, obj, form, change):
        # Auto-set author when created from admin
        if not obj.pk:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(JournalistProfile)
class JournalistProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
