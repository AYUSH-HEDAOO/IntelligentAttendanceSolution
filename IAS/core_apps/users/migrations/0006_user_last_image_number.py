# Generated by Django 4.2 on 2025-03-02 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_role_options_alter_role_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_image_number',
            field=models.IntegerField(default=1),
        ),
    ]
