from django.db import models
from django.contrib.auth.models import User


class SignupInfo(models.Model):
    CHECK_FAILED = 'failed'
    CHECK_IN_PROGRESS = 'in_progress'
    CHECK_PASSED_SUCCESS = 'passed'

    EMAIL_CHECK_STATUSES = (
        (CHECK_FAILED, 'Check failed'),
        (CHECK_IN_PROGRESS, 'Check in progress'),
        (CHECK_PASSED_SUCCESS, 'Check passed'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    info = models.JSONField(default={})
    email_check_status = models.CharField(choices=EMAIL_CHECK_STATUSES,
                                          default=CHECK_IN_PROGRESS)
    is_signup_finished = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
