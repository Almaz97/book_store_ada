import datetime
from celery import app
from .models import Book
from .utils import send_email


@app.shared_task
def divide(x, y):
    import time
    time.sleep(5)
    return x / y


@app.shared_task
def send_statistics():
    swipe_in = datetime.datetime.today()
    new_swipe_in = (swipe_in - datetime.timedelta(minutes=2))

    books_in_last_2_mins = Book.objects.filter(
        created_at__gte=new_swipe_in,
    ).values_list('title', flat=True)

    subject = 'Books statistics in last 2 mins'
    message = f'Books created in last 2 mins {books_in_last_2_mins}'
    recipient_list = ['mositosi97@gmail.com']

    send_email(subject=subject,
               message=message,
               recipient_list=recipient_list)
