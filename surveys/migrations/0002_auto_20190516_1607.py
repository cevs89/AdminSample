# Generated by Django 2.2.1 on 2019-05-16 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveyanswers',
            name='position',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='surveyquestion',
            name='pages',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='surveyquestion',
            name='position',
            field=models.IntegerField(default=0),
        ),
    ]
