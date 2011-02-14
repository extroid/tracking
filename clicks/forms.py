from django import forms

class SalesForm(forms.Form):
    subids = forms.CharField(widget=forms.Textarea)
    
