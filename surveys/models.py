from django.db import models
from django.core.validators import validate_image_file_extension


class SurveysMain(models.Model):
    title = models.CharField(max_length=255)
    descripcion = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Survey Main"

    def __str__(self):
        return str(self.title)


class SurveyAnswersOptions(models.Model):
    ansewrs_options = models.ManyToManyField(
        'SurveyAnswers', related_name="survey_answers_options",
    )
    survey_question = models.ForeignKey(
        'SurveyQuestion', on_delete=models.CASCADE,
        related_name="survey_answer_question",
    )

    class Meta:
        verbose_name_plural = "Survey Answers Options"

    def __str__(self):
        return str(self.pk)


class SurveyQuestion(models.Model):
    question_text = models.CharField(max_length=255, null=True, blank=True)
    question_image = models.ImageField(
        upload_to='question_image/',
        validators=[validate_image_file_extension],
        null=True, blank=True
    )
    question_foto_firma = models.ImageField(
        upload_to='question_foto_firma/',
        validators=[validate_image_file_extension],
        null=True, blank=True
    )
    question_html = models.TextField(default='')
    survey = models.ForeignKey(
        'SurveysMain', on_delete=models.CASCADE,
        related_name="survey_question_survey",
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    options_answer = models.SmallIntegerField(
        choices=(
            (0, 'Seleccion Unica'), (1, 'Seleccion Multiple'), (2, 'Texto'),
            (3, 'Seleccion Unica SI/NO')
         ), default=0
    )
    type_questions = models.SmallIntegerField(
        choices=(
            (0, 'Question Text'), (1, 'Question Image'),
            (2, 'Firma'), (3, 'Foto Firma'),
            (4, 'Imagen Input'), (5, 'HTML'),
         ), default=0
    )
    position = models.IntegerField(default=0)
    pages = models.IntegerField(default=0)
    others = models.BooleanField(default=1)
    redirection = models.BooleanField(default=0)
    comment = models.CharField(max_length=255, null=True, blank=True)

    @property
    def has_other(self):
        return bool(self.others)

    @property
    def has_redirection(self):
        return bool(self.redirection)

    class Meta:
        verbose_name_plural = "Survey Question"

    def __str__(self):
        return "Pagina " + str(self.pages) + " - " + str(self.question_text)


class SurveyAnswers(models.Model):
    name_answer = models.CharField(max_length=255)
    position = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Survey Answers"

    def __str__(self):
        return str(self.position) + " - " + str(self.name_answer)


class AnswersQuestions(models.Model):
    survey = models.ForeignKey(
        'SurveysMain', on_delete=models.CASCADE,
        related_name="answers_questions_survey",
    )
    survey_question = models.ForeignKey(
        'SurveyQuestion', on_delete=models.CASCADE,
        related_name="answers_questions_question",
    )
    answers = models.CharField(max_length=255, null=True, blank=True)
    others = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Answers Questions Client"

    def __str__(self):
        return str(self.survey) + " - " + str(self.survey_question)


class RelationshipQuestion(models.Model):
    questions_relations = models.ForeignKey(
        'SurveyQuestion', on_delete=models.CASCADE,
        related_name="relation_question_relation",
    )
    when_answer = models.ForeignKey(
        'SurveyAnswers', on_delete=models.CASCADE,
        related_name="relation_question_when_answer",
    )
    questions_redirect = models.ForeignKey(
        'SurveyQuestion', on_delete=models.CASCADE,
        related_name="relation_question_redirect",
    )

    class Meta:
        verbose_name_plural = "Relationship Question"

    def __str__(self):
        return "Relacion:" + str(self.questions_relations) + " Redireccion:" + str(self.questions_redirect)
