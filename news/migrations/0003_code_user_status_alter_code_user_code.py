# Generated by Django 4.1.4 on 2023-01-03 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_code_user_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='code',
            name='user_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='code',
            name='user_code',
            field=models.CharField(default='5227', max_length=4),
        ),
    ]
