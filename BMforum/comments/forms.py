from django import forms
from .models import Comment,MovieComment
 
 
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class CommentForm2(forms.ModelForm):
    class Meta:
        model = MovieComment
        fields = ['text']