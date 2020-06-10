from django import forms
from .models import MovieReport
 
 
class ReportForm(forms.ModelForm):
    class Meta:
        model = MovieReport
        fields = ['title','text']
