# Generated by Django 5.1 on 2024-12-30 12:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ESG', '0048_area_topic_survey'),
    ]

    operations = [
        migrations.CreateModel(
            name='Introduction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Intro', models.CharField(max_length=10)),
                ('survey', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ESG.surveys')),
            ],
        ),
    ]
