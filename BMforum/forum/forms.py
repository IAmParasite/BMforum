from django import forms
from .models import GroupPost

class GroupPostForm(forms.ModelForm):
    class Meta:
        model = GroupPost
        fields = [ 'title', 'body']
