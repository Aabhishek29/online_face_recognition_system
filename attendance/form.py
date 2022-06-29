from django import forms
from .models import EnrollStudent


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = EnrollStudent
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input-field', 'required': 'True','autocomplete':"off"}),
            'sid': forms.NumberInput(attrs={'class': 'input-field', 'required': 'True','autocomplete':"off"}),
            'emailId' : forms.EmailInput(attrs={'class': 'input-field','required':'True', 'autocomplete':'off'}),
            'img' : forms.FileInput(attrs= {'class': 'input-field','required':'True', 'autocomplete':'off'})
        }
        labels = {
            'name': 'Student Name:',
            'sid': 'Student Id:',
            'emailId' : 'Email Id',
            'img' : 'Upload your image:'
        }