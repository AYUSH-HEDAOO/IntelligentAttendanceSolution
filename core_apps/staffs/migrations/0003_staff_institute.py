# Generated by Django 5.0.7 on 2024-11-08 17:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutes', '0007_delete_staff'),
        ('staffs', '0002_remove_staff_enrollment_number_remove_staff_grade_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='institute',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='institute_staff', to='institutes.institute'),
        ),
    ]