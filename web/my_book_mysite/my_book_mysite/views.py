from django.http import HttpResponse
from django.shortcuts import render


def hello(request):
    return render(request, "hello.html", {"message": "欢迎学习 Django 模版！"})

def books(request):
    sample_books = [
        {"id": 1, "title": "Django 入门"},
        {"id": 2, "title": "Python 进阶"},
        {"id": 3, "title": "Web 开发实践"},
    ]
    return render(request, "books.html", {"books": sample_books})


def base_demo(request):
    return render(request, "base.html")

# 定义图书详情视图
def book_detail(request, book_id):
    return HttpResponse(f"Hello, Django from my_book_mysite! 这是图书ID为{book_id}的详情。")

# 使用get方法获取图书详情
def book_detail_get(request):
    book_id = request.GET.get("book_id")
    if book_id:
        return HttpResponse(f"Hello, Django from my_book_mysite! 这是图书ID为{book_id}的详情。")
    else:
        return HttpResponse("请提供图书ID参数。")
