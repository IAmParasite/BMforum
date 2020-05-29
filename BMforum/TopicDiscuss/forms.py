from django import forms
from .models import TopicDiscuss


class TopicDiscussForm(forms.ModelForm):
    class Meta:
        model = TopicDiscuss
        fields = ['text']
