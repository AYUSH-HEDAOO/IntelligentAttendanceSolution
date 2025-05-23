# Generated by Django 5.0.7 on 2024-12-07 08:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutes', '0007_delete_staff'),
        ('students', '0002_remove_student_grade_student_institute'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='department',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='student_department',
                to='institutes.department'
            ),
        ),
    ]
