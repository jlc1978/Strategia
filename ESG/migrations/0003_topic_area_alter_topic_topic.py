# Generated by Django 5.1 on 2024-09-01 14:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ESG', '0002_alter_topic_topic'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='area',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ESG.area'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='topic',
            field=models.CharField(max_length=30),
        ),
    ]
