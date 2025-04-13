"""
URL configuration for synergy4 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from bookstore.views import book_list, buy_book, rent_book, user_logout, user_login, register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', book_list, name='book_list'),
    path('books/buy/<int:book_id>/', buy_book, name='buy_book'),
    path('books/rent/<int:book_id>/<int:duration>', rent_book, name='rent_book'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]
