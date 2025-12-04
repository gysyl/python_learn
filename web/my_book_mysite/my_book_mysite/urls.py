from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import *


urlpatterns = [
    path("admin/", admin.site.urls),
    path("hello/", hello, name="hello"),
    path("books/", books, name="books"),
    path("books/<int:book_id>/", book_detail, name="book_detail"),
    path("books/get/", book_detail_get, name="book_detail_get"),
    path("base/", base_demo, name="base_demo"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
