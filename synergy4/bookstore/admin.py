from django.contrib import admin
from django.utils.html import format_html
from django.shortcuts import redirect
from django.urls import path
from django.contrib import messages
from .services import send_rental_email  # Импортируем функцию

from bookstore.models import Book, Rental

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'year', 'price', 'available')
    search_fields = ('title', 'author')
    list_filter = ('category', 'year', 'available')


class RentalAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'start_date', 'end_date', 'send_email_button')
    search_fields = ('user__username', 'book__title')
    list_filter = ('start_date', 'end_date')

    def send_email_button(self, obj):
        return format_html('<a class="button" href="send-email/{}/">Отправить email</a>', obj.id)
    send_email_button.short_description = "Отправка email"
    send_email_button.allow_tags = True

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('send-email/<int:rental_id>/', self.admin_site.admin_view(self.send_email_view), name='send_rental_email'),
        ]
        return custom_urls + urls

    def send_email_view(self, request, rental_id):
        rental = Rental.objects.get(id=rental_id)
        if rental.user.email:
            send_rental_email(rental)
            self.message_user(request, f"Email отправлен пользователю {rental.user.email}", messages.SUCCESS)
        else:
            self.message_user(request, "У пользователя нет email", messages.ERROR)
        return redirect(request.META.get('HTTP_REFERER', 'admin:bookstore_rental_changelist'))

admin.site.register(Book, BookAdmin)
admin.site.register(Rental, RentalAdmin)