# Generated by Django 2.2.1 on 2019-05-14 14:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recognition', '0002_auto_20190513_2015'),
    ]

    operations = [
        migrations.AddField(
            model_name='recognitionelement',
            name='estimated_date',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='recognitionelement',
            name='state',
            field=models.SmallIntegerField(choices=[(0, 'En Espera'), (1, 'Completado'), (2, 'Rechazado')], default=0),
        ),
    ]
