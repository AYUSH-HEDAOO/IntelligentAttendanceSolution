# Generated by Django 3.2 on 2025-02-09 17:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0016_alter_student_role'),
    ]

    operations = [
        migrations.DeleteModel(name='Attendance',),
    ]
