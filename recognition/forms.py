from django import forms
from .models import RecognitionElement


class PostFormRecognitionElement(forms.ModelForm):
    class Meta:
        model = RecognitionElement
        fields = (
            'label', 'image', 'modelo', 'descripcion', 'month', 'year',
            'note_img', 'estimated_date'
        )

        widgets = {
            'label': forms.TextInput(
                attrs={'class': 'form-control'}),
            'modelo': forms.Textarea(
                attrs={
                    'class': 'form-control', 'rows': '4',
                    'cols': '50'
                 }),
            'descripcion': forms.Textarea(
                attrs={
                    'class': 'form-control', 'rows': '4',
                    'cols': '50'
                }),
            'month': forms.TextInput(
                attrs={'class': 'form-control'}),
            'year': forms.TextInput(
                attrs={'class': 'form-control'}),
            'note_img': forms.Textarea(
                attrs={
                    'class': 'form-control', 'rows': '4',
                    'cols': '50'
                }
            ),
            'estimated_date': forms.TextInput(
                attrs={
                    'type': 'text', 'class': 'form-control datepicker'}
            ),
        }


class EditFormRecognitionElement(forms.ModelForm):
    class Meta:
        model = RecognitionElement
        fields = (
            'label', 'image', 'modelo', 'descripcion', 'month', 'year',
            'status', 'note_img', 'estimated_date', 'state'
        )

        widgets = {
            'label': forms.TextInput(
                attrs={'class': 'form-control'}),
            'modelo': forms.Textarea(
                attrs={
                    'class': 'form-control', 'rows': '4',
                    'cols': '50'
                 }),
            'descripcion': forms.Textarea(
                attrs={
                    'class': 'form-control', 'rows': '4',
                    'cols': '50'
                }),
            'month': forms.TextInput(
                attrs={'class': 'form-control'}),
            'year': forms.TextInput(
                attrs={'class': 'form-control'}),
            'note_img': forms.Textarea(
                attrs={
                    'class': 'form-control', 'rows': '4',
                    'cols': '50',
                }
            ),
            'estimated_date': forms.TextInput(
                attrs={
                    'type': 'text', 'class': 'form-control datepicker'}
            ),
            'state': forms.Select(
                attrs={
                    'class': 'form-control show-tick'}
            ),
        }
