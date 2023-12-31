# Generated by Django 4.2.4 on 2023-09-06 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0004_alter_signupinfo_email_check_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signupinfo',
            name='email_check_status',
            field=models.CharField(choices=[('failed', 'Check failed'), ('in_progress', 'Check in progress'), ('passed', 'Check passed')], default='in_progress'),
        ),
    ]
