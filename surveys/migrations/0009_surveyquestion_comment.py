# Generated by Django 2.2.1 on 2019-06-04 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0008_auto_20190527_1618'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveyquestion',
            name='comment',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]