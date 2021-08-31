from django import forms


class ResumeForm(forms.Form):
    description = forms.CharField(max_length=1024, min_length=1)
