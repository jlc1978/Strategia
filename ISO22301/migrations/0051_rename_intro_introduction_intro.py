# Generated by Django 5.1 on 2024-12-30 12:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ISO22301', '0050_alter_introduction_intro'),
    ]

    operations = [
        migrations.RenameField(
            model_name='introduction',
            old_name='Intro',
            new_name='intro',
        ),
    ]
