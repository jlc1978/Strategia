# Generated by Django 5.1 on 2025-02-01 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ISO22301', '0062_final_result_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='final_result_question',
            name='question',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
