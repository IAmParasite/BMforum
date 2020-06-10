from django import forms
from .models import MovieComment
 
 
class MovieCommentForm(forms.ModelForm):
    class Meta:
        model = MovieComment
        fields = ['title','text']
