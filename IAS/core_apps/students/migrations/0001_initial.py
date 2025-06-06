# Generated by Django 5.0.7 on 2024-07-23 12:44

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0002_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('pkid', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('enrollment_number', models.CharField(max_length=100)),
                ('grade', models.CharField(max_length=50)),
                ('role', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.role')),
            ],
            options={
                'ordering': ['-created_at', '-updated_at'],
                'abstract': False,
            },
        ),
    ]
