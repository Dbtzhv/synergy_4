from django.core.mail import send_mail
from django.conf import settings

def send_rental_email(rental):
    subject = "Подтверждение аренды книги"
    message = (
        f"Здравствуйте, {rental.user.username}!\n\n"
        f"Вы арендовали книгу: {rental.book.title}\n"
        f"Дата начала аренды: {rental.start_date.strftime('%Y-%m-%d')}\n"
        f"Дата окончания аренды: {rental.end_date.strftime('%Y-%m-%d')}\n\n"
        "Спасибо, что пользуетесь нашей библиотекой!"
    )
    
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [rental.user.email])