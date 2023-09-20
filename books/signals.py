from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Book
from .utils import send_email


@receiver(post_save, sender=Book)
def send_book_email(instance, created, **kwargs):
    if created:
        subject = 'Book created successfully'
        message = f'You have been created book {instance.title}'
        recipient_list = [instance.created_by.email]
        send_email(subject=subject,
                   message=message,
                   recipient_list=recipient_list)
