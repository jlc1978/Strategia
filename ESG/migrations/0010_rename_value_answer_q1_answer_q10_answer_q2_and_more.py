# Generated by Django 5.1 on 2024-09-01 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ESG', '0009_alter_question_question_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='value',
            new_name='Q1',
        ),
        migrations.AddField(
            model_name='answer',
            name='Q10',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='Q2',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='Q3',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='Q4',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='Q5',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='Q6',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='Q7',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='Q8',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='Q9',
            field=models.IntegerField(null=True),
        ),
    ]
