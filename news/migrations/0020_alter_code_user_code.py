# Generated by Django 4.1.4 on 2023-01-10 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0019_alter_code_user_code_alter_post_category_news'),
    ]

    operations = [
        migrations.AlterField(
            model_name='code',
            name='user_code',
            field=models.CharField(default='8073', max_length=4),
        ),
    ]