# Generated by Django 5.0.7 on 2024-11-05 07:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutes', '0007_delete_staff'),
        ('staffs', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff',
            name='enrollment_number',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='grade',
        ),
        migrations.AddField(
            model_name='staff',
            name='department',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='staff_department',
                to='institutes.department'
            ),
        ),
        migrations.AddField(
            model_name='staff',
            name='designation',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='staff_designation',
                to='institutes.designation'
            ),
        ),
    ]
