# Generated by Django 3.2 on 2025-02-26 06:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0002_auto_20250209_2316'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='academic_class',
        ),
        migrations.RemoveField(
            model_name='attendance',
            name='academic_section',
        ),
    ]
