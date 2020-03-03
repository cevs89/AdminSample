# encoding: utf-8
import serpy
from surveys.models import RelationshipQuestion


class SurveysMainSerializer(serpy.Serializer):
    id = serpy.Field()
    title = serpy.Field()
    descripcion = serpy.Field()
    pub_date = serpy.Field()


class AnswersSerializer(serpy.Serializer):
    id = serpy.Field()
    name_answer = serpy.Field()
    position = serpy.Field()


class QuestionSerializer(serpy.Serializer):
    id = serpy.Field()
    question_text = serpy.Field()
    question_image = serpy.MethodField()
    question_foto_firma = serpy.MethodField()
    question_html = serpy.Field()
    survey = serpy.MethodField()  # SurveysMain
    pub_date = serpy.Field()
    options_answer = serpy.MethodField()
    type_questions = serpy.MethodField()
    position = serpy.Field()
    pages = serpy.Field()
    others = serpy.Field()
    redirection = serpy.MethodField()

    def get_survey(self, obj):
        if obj.survey is not None:
            return obj.survey.pk

    def get_question_image(self, obj):
        if not obj.question_image:
            return None
        else:
            return '/media/' + str(obj.question_image)

    def get_question_foto_firma(self, obj):
        if not obj.question_foto_firma:
            return None
        else:
            return '/media/' + str(obj.question_foto_firma)

    def get_options_answer(self, obj):
        if obj.options_answer is not None:
            array = {
                'id_options_answer': obj.options_answer,
                'name_options_answer': obj.get_options_answer_display()
            }
            return array

    def get_type_questions(self, obj):
        if obj.type_questions is not None:
            array = {
                'id_type_questions': obj.type_questions,
                'name_type_questions': obj.get_type_questions_display()
            }
            return array

    def get_redirection(self, obj):
        if obj.redirection:
            query_set = RelationshipQuestion.objects.get(
                questions_relations_id=obj.id)
            array = {
                'redirection': obj.redirection,
                'page': query_set.questions_redirect.pages,
                'position': query_set.questions_redirect.position,
            }
            return array
        else:
            return obj.redirection


class AnswersQuestionsSerializer(serpy.Serializer):
    id = serpy.Field()
    survey_question = serpy.MethodField()
    answers = serpy.Field()
    others = serpy.Field()

    def get_survey_question(self, obj):
        if obj.survey_question is not None:
            array = {
                'id_question': obj.survey_question.pk,
                'id_survey': obj.survey_question.survey.pk,
                'survey': obj.survey_question.survey.title,
            }
            return array


class RelationshipQuestionSerializer(serpy.Serializer):
    id = serpy.Field()
    questions_relations = serpy.MethodField()
    when_answer = serpy.MethodField()
    questions_redirect = serpy.MethodField()

    def get_questions_relations(self, obj):
        if obj.questions_relations is not None:
            array_question_relation = {
                'id_question_relation': obj.questions_relations.pk,
                'page_question_relation': obj.questions_relations.pages,
                'position_question_relation': obj.questions_relations.position,

            }
            return array_question_relation

    def get_when_answer(self, obj):
        if obj.when_answer is not None:
            array_when_answer = {
                'id_array_when': obj.when_answer.pk,
                'name_when_answer': obj.when_answer.name_answer,
            }
            return array_when_answer

    def get_questions_redirect(self, obj):
        if obj.questions_redirect is not None:
            array_question_redirect = {
                'id_question_redirect': obj.questions_redirect.pk,
                'page_question_redirect': obj.questions_redirect.pages,
                'position_question_redirect': obj.questions_redirect.position,

            }
            return array_question_redirect


class SurveysAllSerializer(serpy.Serializer):
    id = serpy.Field()
    email = serpy.Field()
    content = serpy.Field()
    created = serpy.Field()


class AnswersOptionsSerializer(serpy.Serializer):
    survey = serpy.MethodField('survey_main')
    survey_question = QuestionSerializer()
    ansewrs_options = serpy.MethodField()

    def survey_main(self, obj):
        if obj.survey_question is not None:
            list_response = []
            array = {
              "id": obj.survey_question.survey_id,
              "title": obj.survey_question.survey.title,
              "descripcion": obj.survey_question.survey.descripcion
            }
            list_response.append(array)
            return list_response

    def get_ansewrs_options(self, obj):
        if obj.ansewrs_options is not None:
            list_response = []
            for a in obj.ansewrs_options.all():
                array = {
                    'id_answer': a.pk,
                    'name_Answerer': a.name_answer,
                    'position_answer': a.position,
                }
                list_response.append(array)
            return list_response
