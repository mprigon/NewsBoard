# Generated by Django 4.1.4 on 2023-01-08 10:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0011_remove_newsletter_authornewsletter_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsletter',
            name='userNewsletter',
            field=models.OneToOneField(default=2, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='code',
            name='user_code',
            field=models.CharField(default='4385', max_length=4),
        ),
    ]
