from django import forms
from django.forms import ModelForm
from defacements.models import Notifier, Defacements
from django.contrib.auth.models import User

class Defacements_Form(ModelForm):
    class Meta:
        model = Defacements

class Submit_Defacements_Form(forms.Form):
    notifier = forms.CharField(max_length=30, min_length=1)
    full_path = forms.URLField()
    notifier_words = forms.CharField(widget=forms.Textarea,required=False, label='notifier_words(options)')
    e_mail = forms.EmailField(required=False, label='E_mail(options)')
        

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100, min_length=10, label='subject')
    email = forms.EmailField(required=False)
    message = forms.CharField(widget=forms.Textarea)
    
    def clean_message(self):
        message = self.cleaned_data['message']
        num_words = len(message.split())
        if num_words < 4:
            raise forms.ValidationError("Not enough words")
        return message
