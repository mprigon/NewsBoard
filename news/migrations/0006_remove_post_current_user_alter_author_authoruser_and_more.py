# Generated by Django 4.1.4 on 2023-01-04 13:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0005_alter_author_authoruser_alter_code_user_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='current_user',
        ),
        migrations.AlterField(
            model_name='author',
            name='authorUser',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='code',
            name='user_code',
            field=models.CharField(default='1973', max_length=4),
        ),
    ]