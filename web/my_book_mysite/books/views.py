from django.shortcuts import render, HttpResponse, redirect
from .models import Book

# Create your views here.
def add_book(request):
    if request.method == "POST":
        name = request.POST.get("name")
        author = request.POST.get("author")
        price = request.POST.get("price")
        
        Book.objects.create(name=name, author=author, price=price)
        return HttpResponse("Book added successfully")
        
    return render(request, "books/add_book.html")

def query_books(request):
    # 1. 查询所有
    all_books = Book.objects.all()
    all_books_str = ", ".join([f"{b.name} ({b.author})" for b in all_books])

    # 2. 条件过滤 (查找作者是 '龚毅' 的书)
    gongyi_books = Book.objects.filter(author="龚毅")
    gongyi_books_str = ", ".join([b.name for b in gongyi_books])

    # 3. 获取单条 (查找第一本书，如果存在)
    first_book = Book.objects.first()
    first_book_str = first_book.name if first_book else "None"
    
    # 构造返回内容
    result = f"""
    <h1>Data Retrieval Examples</h1>
    <h3>1. All Books:</h3>
    <p>{all_books_str}</p>
    
    <h3>2. Books by '龚毅':</h3>
    <p>{gongyi_books_str}</p>
    
    <h3>3. First Book:</h3>
    <p>{first_book_str}</p>
    """
    
    return HttpResponse(result)

def sort_books(request):
    # 按价格升序
    books_asc = Book.objects.order_by('price')
    asc_str = ", ".join([f"{b.name}: {b.price}" for b in books_asc])
    
    # 按价格降序
    books_desc = Book.objects.order_by('-price')
    desc_str = ", ".join([f"{b.name}: {b.price}" for b in books_desc])
    
    result = f"""
    <h1>Sorting Examples</h1>
    <h3>Price Ascending (Low to High):</h3>
    <p>{asc_str}</p>
    
    <h3>Price Descending (High to Low):</h3>
    <p>{desc_str}</p>
    """
    return HttpResponse(result)

def edit_book(request, book_id):
    book = Book.objects.get(id=book_id)
    
    if request.method == "POST":
        book.name = request.POST.get("name")
        book.author = request.POST.get("author")
        book.price = request.POST.get("price")
        book.save()
        
        return HttpResponse("Book updated successfully")
        
    return render(request, "books/edit_book.html", {"book": book})

