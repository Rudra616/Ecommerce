# Generated by Django 5.0.7 on 2024-07-25 05:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0006_userregister_confirmpassword'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userregister',
            name='confirmpassword',
        ),
    ]
