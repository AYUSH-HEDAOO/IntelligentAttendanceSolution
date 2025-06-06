# Generated by Django 5.0.7 on 2024-11-03 11:57

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutes', '0005_designation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('pkid', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('staff_name', models.CharField(max_length=200)),
                (
                    'institute',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name='staff', to='institutes.institute'
                    )
                ),
            ],
            options={
                'ordering': ['-created_at', '-updated_at'],
                'abstract': False,
            },
        ),
    ]
