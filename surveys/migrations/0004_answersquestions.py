# Generated by Django 2.2.1 on 2019-05-20 21:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0003_surveyquestion_others'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswersQuestions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answers', models.CharField(blank=True, max_length=255, null=True)),
                ('others', models.IntegerField(default=0)),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers_questions_survey', to='surveys.SurveysMain')),
                ('survey_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers_questions_question', to='surveys.SurveyQuestion')),
            ],
            options={
                'verbose_name_plural': 'Answers Questions Client',
            },
        ),
    ]