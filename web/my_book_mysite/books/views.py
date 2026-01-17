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
    query = request.GET.get('q', '')
    if query:
        books = Book.objects.filter(name__icontains=query) | Book.objects.filter(author__icontains=query)
    else:
        books = Book.objects.all()
        
    return render(request, "books/query_books.html", {"books": books, "query": query})

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

def book_list(request):
    books = Book.objects.all()
    return render(request, "books/book_list.html", {"books": books})

def index(request):
    book_count = Book.objects.count()
    author_count = Book.objects.values('author').distinct().count()
    return render(request, "books/index.html", {
        "book_count": book_count,
        "author_count": author_count
    })

def delete_book(request, book_id):
    Book.objects.filter(id=book_id).delete()
    return redirect('book_list')

