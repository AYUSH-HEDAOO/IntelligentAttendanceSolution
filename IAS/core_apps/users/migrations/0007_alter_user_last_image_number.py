# Generated by Django 4.2 on 2025-03-02 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_last_image_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='last_image_number',
            field=models.IntegerField(default=0),
        ),
    ]
