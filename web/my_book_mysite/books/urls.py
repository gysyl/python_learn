from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_book, name='add_book'),
    path('query/', views.query_books, name='query_books'),
    path('sort/', views.sort_books, name='sort_books'),
    path('edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('list/', views.book_list, name='book_list'),
    path('delete/<int:book_id>/', views.delete_book, name='delete_book'),
]
