# Generated by Django 4.2 on 2025-03-02 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0004_attendance_academic_class_section'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='a_status',
            field=models.CharField(
                choices=[('present', 'Present'), ('absent', 'Absent'), ('on leave', 'On Leave'), ('holiday', 'Holiday'),
                         ('weekend', 'Weekend')],
                default='absent',
                max_length=10
            ),
        ),
    ]
