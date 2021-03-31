from django import forms

class ReportForm(forms.Form):
    message = forms.CharField()
