# Generated by Django 5.1 on 2024-09-14 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ISO22301', '0025_answer_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='company',
            field=models.CharField(max_length=75, null=True),
        ),
    ]
