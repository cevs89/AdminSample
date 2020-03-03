from django.contrib import admin
from surveys.models import (
            SurveysMain, SurveyAnswers, SurveyAnswersOptions, SurveyQuestion,
            AnswersQuestions, RelationshipQuestion
        )


admin.site.register(SurveysMain)
admin.site.register(SurveyAnswers)
admin.site.register(SurveyQuestion)
admin.site.register(AnswersQuestions)
admin.site.register(SurveyAnswersOptions)
admin.site.register(RelationshipQuestion)
