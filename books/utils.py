from django.db import models
from django.conf import settings
from django.core.mail import send_mail


class TrackableModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def send_email(subject, message, recipient_list):
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list,
        fail_silently=False,
    )


"""
   
1) Создать таблицу SignupInfo и связать с таблицей User
2) SignupInfo поля:
    user, info, created_at
3) Сделать поле info JsonField
4) При регистрации определите ip пользователя и сделайте запрос на 
    https://www.abstractapi.com/api/ip-geolocation-api, платформа вернет детальное
    инфо пользователя по ip адресу.
5) Сохраните полученные данные в SignupInfo таблицу
6) Также продумайте валидацию на весь этот процесс

"""