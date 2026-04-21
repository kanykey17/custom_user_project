from celery import shared_task
from django.core.mail import send_mail


@shared_task
def save_log(message):
    print(f"Сохраняю лог: {message}")


@shared_task
def delete_old_products():
    print("Удаляю старые продукты")


@shared_task
def send_welcome_email(email):
    send_mail(
        'Добро пожаловать',
        'Спасибо за регистрацию!',
        'from@gmail.com',
        [email],
        fail_silently=False,
    )