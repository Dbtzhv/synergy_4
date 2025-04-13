from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone


from bookstore.models import Book, Rental
from bookstore.forms import CustomUserCreationForm


# Регистрация пользователя
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('book_list')  # Перенаправляем на список книг
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

# Логин пользователя
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('book_list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


# Логаут пользователя
def user_logout(request):
    logout(request)
    return redirect('login')



# Вьюхи для отображения книг и покупки/аренды

@login_required
def book_list(request):
    sort_by = request.GET.get('sort', '')
    books = Book.objects.all()
    
    if sort_by == 'year':
        books = books.order_by('year')
    elif sort_by == 'author':
        books = books.order_by('author')
    elif sort_by == 'category':
        books = books.order_by('category')
    
    return render(request, 'books.html', {'books': books})

@login_required
def buy_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if book.available:
        book.available = False
        book.save()
    return redirect('book_list')


@login_required
def rent_book(request, book_id, duration):
    book = get_object_or_404(Book, id=book_id)
    if book.available:
        Rental.objects.create(
            user=request.user,
            book=book,
            start_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(weeks=duration)  # по умолчанию 2 недели
        )
        book.available = False
        book.save()
    return redirect('book_list')