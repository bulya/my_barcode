from django import forms


class MyScanner(forms.Form):
    bar_code = forms.ImageField()
