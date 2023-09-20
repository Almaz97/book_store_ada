import requests
import json
from celery import app
from django.contrib.auth.models import User
from django.conf import settings
from .models import SignupInfo


@app.shared_task
def check_email(user_id):
    user = User.objects.filter(id=user_id).first()
    if not user:
        return

    signup_info = SignupInfo.objects.create(user=user)

    # check if email is valid
    url = f"{settings.EMAIL_CHECK_URL}/?api_key={settings.EMAIL_API_KEY}&email={user.email}"
    response = requests.get(url)

    # Probably unreliable condition. There might be a case, when third party service
    # is just crashed, but since this is a test task will keep logic simple
    error_msg = 'Email validation failed: '
    if response.status_code != 200:
        error_msg += f'status_code: {response.status_code}'
        return

    response_body = json.loads(response.content)
    if response_body["is_valid_format"]["value"] is False:
        signup_info.email_check_status = SignupInfo.CHECK_FAILED
    elif response_body["deliverability"] in ["RISKY", "UNKNOWN", "UNDELIVERABLE"]:
        signup_info.email_check_status = SignupInfo.CHECK_FAILED
    else:
        signup_info.email_check_status = SignupInfo.CHECK_PASSED_SUCCESS
        signup_info.is_signup_finished = True

    signup_info.save(update_fields=['email_check_status', 'is_signup_finished'])


@app.shared_task
def save_signup_info(user_id):
    url = f"{settings.IP_INFO_URL}/?api_key={settings.IP_API_KEY}"
    response = requests.get(url)
    response_body = json.loads(response.content)
    signup_info, _ = SignupInfo.objects.get_or_create(user_id=user_id)
    signup_info.info = response_body
    signup_info.save(update_fields=['info'])


"""
1) Создайте celery cron task с периодичностью в неделю 1 раз, который будет
экспортировать все книги за прошлую неделю в excel файл и отправит в виде
отчета только админ пользователям системы (is_super_user = True) 

Примечание!
У нас уже была задача на @action декоратор который экспортировал книги.
Нужно будет вынести эту логику на функцию чтоб им можно было также пользоваться
в celery task
"""