# Generated by Django 4.1.4 on 2023-01-03 21:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0004_post_current_user_alter_code_user_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='authorUser',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='author_of', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='code',
            name='user_code',
            field=models.CharField(default='8223', max_length=4),
        ),
    ]
