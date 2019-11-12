from django import forms
from .models import Feedback
class BlogCommentsForm(forms.ModelForm):
    class Meta:
        model= Feedback
        fields= ['id','feed']


