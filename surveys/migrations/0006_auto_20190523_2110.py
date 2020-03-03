# Generated by Django 2.2.1 on 2019-05-23 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0005_relations'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveyquestion',
            name='redirection',
            field=models.BooleanField(default=0),
        ),
        migrations.AlterField(
            model_name='surveyquestion',
            name='options_answer',
            field=models.SmallIntegerField(choices=[(0, 'Seleccion Unica'), (1, 'Seleccion Multiple'), (2, 'Texto'), (3, 'Seleccion Unica SI/NO')], default=0),
        ),
    ]
