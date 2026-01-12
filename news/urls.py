from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<slug:slug>/', views.category_articles, name='category'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),

    path('articles/mine/', views.my_articles, name='my_articles'),
    path('articles/create/', views.create_article, name='create_article'),
    path('articles/edit/<int:pk>/', views.edit_article, name='edit_article'),
    path('articles/delete/<int:pk>/', views.delete_article, name='delete_article'),

    path('login/', auth_views.LoginView.as_view(template_name='news/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
]
