# Generated by Django 5.1 on 2024-10-04 01:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ISO22301', '0045_outcome_colors_survey'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='survey',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ISO22301.surveys'),
        ),
    ]
