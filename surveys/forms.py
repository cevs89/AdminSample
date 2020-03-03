from django import forms
from surveys.models import SurveysMain, SurveyAnswers, SurveyAnswersOptions, SurveyQuestion


OPTION_ANSWERS = [
    (0, 'Seleccion Unica'),
    (1, 'Seleccion Multiple'),
    (2, 'Texto'),
    (3, 'Seleccion Unica SI/NO')
]

TYPE_QUESTIONS_SELECT = [
    (0, 'Question Text'), (1, 'Question Image'),
    (2, 'Firma'), (3, 'Foto Firma'),
    (4, 'Imagen Input'), (5, 'HTML'),
]


class FormSureysMain(forms.ModelForm):
    class Meta:
        model = SurveysMain
        fields = (
            'title', 'descripcion'
        )
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(
                attrs={
                    'class': 'form-control', 'rows': '4',
                    'cols': '50'
                 }
            ),
        }


class FormQuestionsSurveys(forms.Form):
    question_text = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Question", required=False
    )
    question_image = forms.ImageField(label="Question", required=False)
    question_html = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'id': 'ckeditor'
            }
        )
    )
    options_answer = forms.ChoiceField(
        required=False,
        choices=OPTION_ANSWERS,
        widget=forms.Select(
            attrs={'class': 'form-control'}
        ),

    )
    type_questions = forms.ChoiceField(
        required=True,
        choices=TYPE_QUESTIONS_SELECT,
        label="Tipo de pregunta",
        widget=forms.Select(
            attrs={'class': 'form-control selectpicker'}
        ),
    )
    position = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Posicion", required=True,
    )
    pages = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Pagina", required=True,
    )
    answers = forms.CharField(
        label="Respuestas", required=False,
        widget=forms.Select(attrs={'class': 'form-control', 'data-role': 'tagsinput', 'multiple': 'true'}),
    )
    others = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'checkbox', 'value': '1'}),
        label="¿Tendra la opcion de otros?", required=False
    )

    comment = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Comentarios", required=False
    )
