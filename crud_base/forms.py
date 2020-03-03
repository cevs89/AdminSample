from django import forms
from .models import KnowledgeBase


class PostFormKnowledgeBase(forms.ModelForm):
    class Meta:
        model = KnowledgeBase
        fields = (
            'title', 'content', 'intro', 'image', 'start_date', 'end_time',
            'video_url'
        )
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control'}),
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control', 'rows': '4',
                    'cols': '50'
                 }),
            'intro': forms.Textarea(
                attrs={
                    'class': 'form-control', 'rows': '4',
                    'cols': '50'
                }),
            'start_date': forms.TextInput(
                attrs={
                    'type': 'text', 'class': 'form-control datetimepicker'}
                ),
            'end_time': forms.TextInput(
                attrs={
                    'type': 'text', 'class': 'form-control datetimepicker'}
                ),
            'video_url': forms.TextInput(
                attrs={'class': 'form-control'}),
        }
