from django import forms

class HomeForm(forms.Form):
    SeedUrl=forms.CharField(required=True)
    Depth=forms.IntegerField(required=True)