from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_book, name='add_book'),
    path('query/', views.query_books, name='query_books'),
    path('sort/', views.sort_books, name='sort_books'),
    path('edit/<int:book_id>/', views.edit_book, name='edit_book'),
]
