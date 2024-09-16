# Generated by Django 5.1 on 2024-09-01 17:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ISO22301', '0004_area_header_area'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dashboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dashboard', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.CharField(max_length=30)),
                ('project_text', models.CharField(max_length=120)),
                ('outcome', models.CharField(max_length=30)),
                ('outcome_text', models.CharField(max_length=120)),
                ('dashboard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ISO22301.dashboard')),
            ],
        ),
    ]
