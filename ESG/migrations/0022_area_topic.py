# Generated by Django 5.1 on 2024-09-10 17:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ESG', '0021_area_areatext'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area_Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('areatopic', models.CharField(max_length=400)),
                ('area', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ESG.area')),
            ],
        ),
    ]
