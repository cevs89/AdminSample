"""knowledge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from crud_base.views import ListKnowledgeView, CreatetKnowledgeView, \
                            DeleteRecordView, EditKnowledgeView

from recognition.views import ListRecognitionView, CreatetRecognitionView, \
                                EditRecognitionView, DeleteRecognition

from upload_csv.views import ViewUploadCSV
from surveys.views import ListSurveysView, CreateSurveysView, \
                            EditSurveysView, CreateQuestionsView, \
                            DetailsSurveysView, DeleteQuestionSurvey, \
                            AnswersQuestionsView, RelationshipQuestionView, \
                            SurveyMainViewSets, AnswersOptionsViewSets, \
                            AnswersViewSets, QuestionsViewSets, \
                            AnswersQuestionViewSets, RelationshipViewSets, \
                            SurveysAllView, SurveysQuestionsView


from rest_framework.routers import DefaultRouter
from django.conf.urls import include

router = DefaultRouter()
router.register(r'surveys', SurveyMainViewSets, basename='survey')
router.register(r'answers-options', AnswersOptionsViewSets, basename='answers_options')
router.register(r'answers', AnswersViewSets, basename='answers')
router.register(r'question', QuestionsViewSets, basename='question')
router.register(r'answers-question', AnswersQuestionViewSets, basename='answers_question')
router.register(r'relationship', RelationshipViewSets, basename='relations')

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        '', ListKnowledgeView.as_view(),
        name='home'
    ),
    path(
        'dashboard/knowledge/list/', ListKnowledgeView.as_view(),
        name='list_know'
    ),
    path(
        'dashboard/knowledge/create/', CreatetKnowledgeView.as_view(),
        name='create_know'
    ),
    path(
        'dashboard/knowledge/<int:id>/edit/', EditKnowledgeView.as_view(),
        name='edit_know'
    ),
    path(
        'dashboard/knowledge/delete/<int:id>/', DeleteRecordView,
        name='delete_know'
    ),

    #  Recognition
    path(
        'dashboard/recognition/list/', ListRecognitionView.as_view(),
        name='list_recon'
    ),
    path(
        'dashboard/recognition/create/', CreatetRecognitionView.as_view(),
        name='create_recon'
    ),
    path(
        'dashboard/recognition/<int:id>/edit/', EditRecognitionView.as_view(),
        name='edit_recon'
    ),

    path(
        'dashboard/recognition/delete/<int:id>/', DeleteRecognition,
        name='delete_recon'
    ),
    # Upload File CSV
    path('upload/file/cvs/', ViewUploadCSV.as_view(), name='upload_csv'),

    # Surveys
    path(
        'dashboard/survey/list/', ListSurveysView.as_view(),
        name='list_survey'
    ),
    path(
        'dashboard/survey/create/', CreateSurveysView.as_view(),
        name='create_survey'
    ),
    path(
        'dashboard/survey/<int:id>/edit/', EditSurveysView.as_view(),
        name='edit_survey'
    ),
    path(
        'dashboard/survey/<int:id>/questions/create/',
        CreateQuestionsView.as_view(),
        name='create_questions_survey'
    ),
    path(
        'dashboard/survey/<int:id>/questions/<int:id_question>/relationship/',
        RelationshipQuestionView.as_view(),
        name='relationship_questions'
    ),
    path(
        'dashboard/survey/questions/<int:id>/delete/', DeleteQuestionSurvey,
        name='delete_questions_survey'
    ),
    path(
        'dashboard/survey/<int:id>/details/',
        DetailsSurveysView.as_view(),
        name='details_survey'
    ),
    path(
        'dashboard/survey/<int:id>/ansewrs_questions/',
        AnswersQuestionsView.as_view(),
        name='answers_questions_survey'
    ),

    # API.
    path('api/v1/', include(router.urls)),
    path(
        'api/v1/suveys/all/', SurveysAllView.as_view(),
    ),
    path(
        'api/v1/suveys/questions/', SurveysQuestionsView.as_view(),
        name='surveys_questions_ajax'
    ),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
