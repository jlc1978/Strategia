# Generated by Django 5.1 on 2024-10-04 00:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ESG', '0044_comment_survey'),
    ]

    operations = [
        migrations.AddField(
            model_name='outcome_colors',
            name='survey',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ESG.surveys'),
        ),
    ]
