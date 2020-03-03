from django.shortcuts import render, get_object_or_404
from django.views.generic import View, ListView, CreateView
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib import messages
from surveys.models import SurveysMain, SurveyAnswers, SurveyAnswersOptions, \
                            SurveyQuestion, AnswersQuestions, \
                            RelationshipQuestion

from surveys.forms import FormQuestionsSurveys, FormSureysMain
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# API
from surveys.serializers import (
    SurveysMainSerializer, AnswersOptionsSerializer, AnswersSerializer,
    QuestionSerializer, AnswersQuestionsSerializer,
    RelationshipQuestionSerializer, SurveysAllSerializer
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets


class ListSurveysView(ListView):
    model = SurveysMain
    template_name = "list_survey.html"

    def get_queryset(self):
        queryset = super(ListSurveysView, self).get_queryset()
        return queryset


class CreateSurveysView(CreateView):
    template_name = "survey.html"

    def get(self, request, *args, **kwargs):
        context = {}
        context['form'] = FormSureysMain
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        form = FormSureysMain(request.POST)
        context['form'] = form

        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            messages.add_message(request, messages.SUCCESS, 'Se creo de manera correcta')
        else:
            return render(request, self.template_name, context)

        return HttpResponseRedirect(reverse('list_survey'))


class EditSurveysView(View):
    template_name = "survey.html"

    def get(self, request, *args, **kwargs):
        context = {}
        get_id = kwargs['id']
        object_get = get_object_or_404(SurveysMain, pk=get_id)
        context['form'] = FormSureysMain(instance=object_get)
        context['get_id'] = get_id
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        get_id = request.POST.get('get_id')
        object_post = get_object_or_404(SurveysMain, pk=get_id)

        form = FormSureysMain(request.POST, instance=object_post)
        context['form'] = form
        context['get_id'] = get_id

        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            messages.add_message(request, messages.SUCCESS, 'Se Edito de manera correcta')
        else:
            return render(request, self.template_name, context)
        return HttpResponseRedirect(reverse('list_survey'))


class CreateQuestionsView(CreateView):
    template_name = "questions.html"

    def get(self, request, *args, **kwargs):
        context = {}
        id_survey = kwargs['id']
        query_set = SurveysMain.objects.get(pk=id_survey)
        context['form'] = FormQuestionsSurveys
        context['query_set'] = query_set
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        form = FormQuestionsSurveys(request.POST)
        context['form'] = form

        id_survey = request.POST['get_id_surveys']
        query_set = SurveysMain.objects.get(pk=id_survey)
        context['query_set'] = query_set

        if form.is_valid():
            data = request.POST
            print(data)
            get_file = request.FILES

            query_verify = SurveyQuestion.objects.filter(
                position=data['position'], pages=data['pages'],
                survey_id=data['get_id_surveys']
                ).exists()

            if query_verify:
                messages.add_message(request, messages.ERROR, 'Ya existe la posición para esta pagina')
                return render(request, self.template_name, context)

            options_answer = data['options_answer']
            query_save = SurveyQuestion()
            query_save.survey_id = data['get_id_surveys']
            query_save.options_answer = data['options_answer']
            query_save.type_questions = data['type_questions']
            query_save.position = data['position']
            query_save.pages = data['pages']
            query_save.others = request.POST.get('others', 0)
            query_save.comment = request.POST.get('comment', False)
            type_questions = int(data['type_questions'])

            if type_questions == 0 or type_questions == 2 or type_questions == 4:
                query_save.question_text = data['question_text']
            elif type_questions == 1:
                query_save.question_image = get_file['question_image']
            elif type_questions == 3:
                query_save.question_foto_firma = get_file['question_image']
            else:
                query_save.question_html = data['question_html']

            query_save.save()

            query_many = SurveyAnswersOptions.objects.create(
                survey_question=query_save)

            if not options_answer == "3":
                list_answer = request.POST.getlist('answers')
            else:
                list_answer = ['SI', 'NO']

            for i in range(len(list_answer)):
                query_answer = SurveyAnswers.objects.create(
                    name_answer=list_answer[i],
                    position=i+1
                )
                query_many.ansewrs_options.add(query_answer)
        else:
            return render(request, self.template_name, context)

        messages.add_message(request, messages.SUCCESS, 'Se creo la pregunta')
        return HttpResponseRedirect(
            reverse(
                'details_survey',
                kwargs={
                  'id': query_set.pk,
                },
            )
        )


class DetailsSurveysView(View):
    template_name = "details_survey.html"

    def get(self, request, *args, **kwargs):
        context = {}
        get_id = kwargs['id']
        try:
            query_set = SurveysMain.objects.get(pk=get_id)
        except SurveysMain.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'No Existe la encuenta')
            return HttpResponseRedirect(reverse('list_survey'))

        page = int(request.GET.get('page', 1))

        query_question = SurveyQuestion.objects.filter(survey_id=query_set.pk).order_by('position')
        context['query_survey'] = query_set
        context['query_question'] = query_question

        list_response = []
        list_pages = []

        for pagina in query_question:
            list_pages.append(pagina.pages)

        for value in query_question.filter(pages=page):
            query_options = SurveyAnswersOptions.objects.get(survey_question_id=value.pk)
            if value.options_answer == 0 or value.options_answer == 1 or value.options_answer == 3:
                list_answers = list(
                        filter(
                            lambda x: {'Options': x},
                            [a.name_answer for a in query_options.ansewrs_options.all()]
                        )
                    )
            else:
                list_answers = 'Respuesta de Texto'
            quer_relations = RelationshipQuestion.objects.filter(questions_relations_id=value.pk)

            questions = value.question_text if (value.type_questions == 0 or value.type_questions == 2 or value.type_questions == 4) else value.question_image

            if value.type_questions == 3:
                questions = value.question_foto_firma

            if value.type_questions == 5:
                questions = value.question_html

            array_one = {
                'id_question': value.pk,
                'quetions': questions,
                'answer': list_answers,
                'options_answer': value.get_options_answer_display(),
                'type_question': value.get_type_questions_display(),
                'options_answer_id': value.options_answer,
                'type_question_id': value.type_questions,
                'position': value.position,
                'pages': value.pages,
                'others': value.has_other,
                'redireccion': value.has_redirection,
                'data_redirection': quer_relations,
                'comment': value.comment
            }

            list_response.append(array_one)


        pages_num = list(set(list_pages))

        if list_pages:
            # paginator = Paginator(list_response, list_pages.count(page))
            # list_question = paginator.get_page(page)
            context['list_pages'] = pages_num
            context['objct_list'] = list_response
            context['page_next'] = page + 1 if not len(pages_num) == page else False
            context['page_prev'] = page - 1 if page > 1 else False

            context['page_stay'] = page
            context['of_page'] = len(pages_num)

        return render(request, self.template_name, context)


def DeleteQuestionSurvey(request, id):
    try:
        query_set = SurveyQuestion.objects.get(pk=id)
    except SurveyQuestion.DoesNotExist:
        return JsonResponse(
            {"msg": "No existe el registro que desea eliminar"}, status=400)

    try:
        query_questions = SurveyAnswersOptions.objects.get(
                survey_question_id=id)
    except SurveyAnswersOptions.DoesNotExist:
        query_set.delete()
        return JsonResponse(
            {"msg": "El registro de borro de manera correcta"}, status=200)

    query_answer = SurveyAnswers.objects.filter(
        pk__in=[v.pk for v in query_questions.ansewrs_options.all()]
    )
    query_answer.delete()
    query_set.delete()

    return JsonResponse(
        {"msg": "El registro de borro de manera correcta"}, status=200)


class AnswersQuestionsView(View):
    template_name = "answers_surveys.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(AnswersQuestionsView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {}
        get_id = kwargs['id']
        try:
            query_set = SurveysMain.objects.get(pk=get_id)
        except SurveysMain.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'No Existe la encuenta')
            return HttpResponseRedirect(reverse('list_survey'))

        page = int(request.GET.get('page', 1))

        query_question = SurveyQuestion.objects.filter(survey_id=query_set.pk).order_by('position')
        context['query_survey'] = query_set
        context['query_question'] = query_question

        list_response = []
        list_pages = []
        for pagina in query_question:
            list_pages.append(pagina.pages)

        for value in query_question:
            query_options = SurveyAnswersOptions.objects.get(survey_question_id=value.pk)
            if value.options_answer == 0 or value.options_answer == 1 or value.options_answer == 3:
                list_answers = list(
                        map(
                            lambda x, y: {'name_answer': y, 'id_answer': x},
                            [a.pk for a in query_options.ansewrs_options.all()],
                            [a.name_answer for a in query_options.ansewrs_options.all()]
                        )
                    )
            else:
                list_answers = 'Respuesta de Texto'

            quer_relations = RelationshipQuestion.objects.filter(questions_relations_id=value.pk)

            questions = value.question_text if (value.type_questions == 0 or value.type_questions == 2 or value.type_questions == 4) else value.question_image

            if value.type_questions == 3:
                questions = value.question_foto_firma

            if value.type_questions == 5:
                questions = value.question_html


            array_one = {
                'id_question': value.pk,
                'quetions': questions,
                'answer': list_answers,
                'options_answer': value.get_options_answer_display(),
                'type_question': value.get_type_questions_display(),
                'options_answer_id': value.options_answer,
                'type_question_id': value.type_questions,
                'position': value.position,
                'pages': value.pages,
                'others': value.has_other,
                'id_survey': query_set.pk,
                'data_redirection': quer_relations,
                'comment': value.comment
            }

            list_response.append(array_one)

        pages_num = list(set(list_pages))

        # for i in range(len(pages_num)):
        #     print(pages_num[i], list_pages.count(pages_num[i]))

        paginator = Paginator(list_response, list_pages.count(page))
        list_question = paginator.get_page(page)

        context['contacts'] = list_question
        context['list_pages'] = list(set(list_pages))
        context['objct_list'] = list_response
        context['page'] = pages_num

        context['page_next'] = page + 1 if not len(pages_num) == page else False
        context['page_prev'] = page - 1 if page > 1 else False
        context['page_stay'] = page

        return render(request, self.template_name, context)


    def post(self, request, *alist_surveyrgs, **kwargs):
        context = {}
        data = request.POST
        # print(data)
        id_questions_list = list(data.getlist('get_id_questions'))
        id_survey = data['id_survey']

        try:
            query_set = SurveysMain.objects.get(pk=id_survey)
        except SurveysMain.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'No Existe la encuenta')
            return HttpResponseRedirect(reverse('list_survey'))

        answers_qustion_otros = data['answers_qustion'] if 'answers_qustion' in data else False
        checkbox = data.getlist('grupo_checkbox') if 'grupo_checkbox' in data else False

        query_question = SurveyQuestion.objects.filter(survey_id=query_set.pk)
        answers_radio = query_question.filter(options_answer__in=[0, 3]).values_list('pk', flat=True)

        query_checkbox = query_question.filter(options_answer=1).values_list('pk', flat=True)
        query_text = query_question.filter(options_answer=2).values_list('pk', flat=True)

        for txt in range(len(query_text)):
            input_text = data['answers_text_' + str(query_text[txt])] if 'answers_text_' + str(query_text[txt]) in data else False
            AnswersQuestions.objects.create(
                survey_id=data['id_survey'],
                survey_question_id=query_text[txt],
                answers=input_text
            )

        for check in query_checkbox:
            for chk in checkbox:
                AnswersQuestions.objects.create(
                    survey_id=data['id_survey'],
                    survey_question_id=check,
                    answers=chk
                )

        for i in range(len(answers_radio)):
            answers_txt = data['grupo_' + str(answers_radio[i])] if 'grupo_' + str(answers_radio[i]) in data else False

            AnswersQuestions.objects.create(
                survey_id=data['id_survey'],
                survey_question_id=answers_radio[i],
                answers=answers_txt,
                others=answers_qustion_otros if answers_txt == 'SI' else 0
            )

        return HttpResponseRedirect(reverse('list_survey'))


class RelationshipQuestionView(View):
    template_name = "relationship_questions.html"

    def get(self, request, *args, **kwargs):
        context = {}
        id_question = kwargs['id_question']
        id_survey = kwargs['id']
        query_set = SurveyQuestion.objects.get(pk=id_question)
        query_option = SurveyAnswersOptions.objects.get(survey_question_id=id_question)

        context['form'] = SurveyQuestion.objects.exclude(pages=query_set.pages).filter(survey_id=id_survey).order_by('pages')
        context['query_sert'] = query_set
        context['query_option'] = query_option
        context['id_survey'] = id_survey
        context['id_question'] = id_question

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        data = request.POST

        if RelationshipQuestion.objects.filter(questions_relations_id=data['id_question']).exists():
            messages.add_message(request, messages.ERROR, 'Ya hay una relacion para esta pregunta')
            return HttpResponseRedirect(
                reverse(
                    'details_survey',
                    kwargs={
                      'id': data['id_survey'],
                    },
                )
            )

        try:
            query_set = SurveyQuestion.objects.get(pk=data['id_question'])
        except SurveysMain.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'No Existe la pregunta')
            return HttpResponseRedirect(
                reverse(
                    'details_survey',
                    kwargs={
                      'id': data['id_survey'],
                    },
                )
            )

        query = RelationshipQuestion()
        if data:
            query.questions_relations_id = data['id_question']
            query.when_answer_id = data['when_answer']
            query.questions_redirect_id = data['questions_redirect']
            query.save()

            query_set.redirection = True
            query_set.save()

            messages.add_message(request, messages.SUCCESS, 'Se creo de manera correcta')
            return HttpResponseRedirect(
                reverse(
                    'details_survey',
                    kwargs={
                      'id': data['id_survey'],
                    },
                )
            )
        messages.add_message(request, messages.ERROR, 'Sucedio un error, vuelva a intentarlo')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class SurveyMainViewSets(viewsets.ModelViewSet):
    queryset = SurveysMain.objects.filter()
    serializer_class = SurveysMainSerializer


class AnswersOptionsViewSets(viewsets.ModelViewSet):
    queryset = SurveyAnswersOptions.objects.filter()
    serializer_class = AnswersOptionsSerializer


class AnswersViewSets(viewsets.ModelViewSet):
    queryset = SurveyAnswers.objects.filter()
    serializer_class = AnswersSerializer


class QuestionsViewSets(viewsets.ModelViewSet):
    queryset = SurveyQuestion.objects.filter()
    serializer_class = QuestionSerializer


class AnswersQuestionViewSets(viewsets.ModelViewSet):
    queryset = AnswersQuestions.objects.filter()
    serializer_class = AnswersQuestionsSerializer


class RelationshipViewSets(viewsets.ModelViewSet):
    queryset = RelationshipQuestion.objects.filter()
    serializer_class = RelationshipQuestionSerializer


class SurveysAllView(APIView):

    def get(self, request, *args, **kwargs):

        # context = {}
        # list_response = []
        # list_pages = []
        #
        # query_question = SurveyQuestion.objects.filter().order_by('position')
        #
        # for value in query_question:
        #     list_pages.append(value.pages)
        #     query_options = SurveyAnswersOptions.objects.get(survey_question_id=value.pk)
        #     if value.options_answer == 0 or value.options_answer == 1 or value.options_answer == 3:
        #         list_answers = list(
        #                 map(
        #                     lambda x, y: {'name_answer': y, 'id_answer': x},
        #                     [a.pk for a in query_options.ansewrs_options.all()],
        #                     [a.name_answer for a in query_options.ansewrs_options.all()]
        #                 )
        #             )
        #     else:
        #         list_answers = 'Respuesta de Texto'
        #
        #     array_one = {
        #         'id_question': value.pk,
        #         'quetions': value.question_text if(value.type_questions == 0) else value.question_image,
        #         'answer': list_answers,
        #         'options_answer': value.get_options_answer_display(),
        #         'type_question': value.get_type_questions_display(),
        #         'options_answer_id': value.options_answer,
        #         'type_question_id': value.type_questions,
        #         'position': value.position,
        #         'pages': value.pages,
        #         'others': value.has_other,
        #         'redirection': value.redirection,
        #         'id_survey': value.survey_id,
        #     }
        #
        #     list_response.append(array_one)
        #
        # pages_num = list(set(list_pages))
        #
        # context['list_pages'] = pages_num
        # context['count_page'] = len(pages_num)
        # context['data'] = list_response
        serializer_main = SurveysMainSerializer(SurveysMain.objects.filter(), many=True)
        data_main = serializer_main.data,
        list_a = []
        for a in data_main[0]:
            serializer_questions = QuestionSerializer(SurveyQuestion.objects.filter(survey_id=a['id']), many=True)
            data_questions = serializer_questions.data
            a['question'] = data_questions
            list_a.append(a)
        array = {
            'survey': list_a
        }
        return Response(
            array,
            status=status.HTTP_200_OK
        )


class SurveysQuestionsView(APIView):
    serializer_class = SurveysAllSerializer

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SurveysQuestionsView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = request.POST
        list_response = []

        if data['action'] == 'redirect':
            query_question = SurveyQuestion.objects.filter(
                    survey_id=data['id_survey'], redirection=True,
                    options_answer__in=[0, 3]).order_by('position')
        else:
            query_question = SurveyQuestion.objects.filter(
                    survey_id=data['id_survey'], others=True
                    ).order_by('position')

        for value in query_question:
            query_options = SurveyAnswersOptions.objects.get(survey_question_id=value.pk)
            if value.options_answer == 0 or value.options_answer == 1 or value.options_answer == 3:
                list_answers = list(
                        map(
                            lambda x, y: {'name_answer': y, 'id_answer': x},
                            [a.pk for a in query_options.ansewrs_options.all()],
                            [a.name_answer for a in query_options.ansewrs_options.all()]
                        )
                    )
            quer_relations = RelationshipQuestion.objects.filter(questions_relations_id=value.pk)
            array_one = {
                'id_question': value.pk,
                'answer': list_answers,
                'position': value.position,
                'pages': value.pages,
                'otros': value.others,
                'data_redirection': list(
                    map(
                        lambda x: {"when": x[0], "position_redirect": x[1], "page_redirect": x[2]},
                        [[a.when_answer_id, a.questions_redirect.position, a.questions_redirect.pages] for a in quer_relations]
                    )
                )
            }
            list_response.append(array_one)

        return Response(
            list_response,
            status=status.HTTP_200_OK
        )
