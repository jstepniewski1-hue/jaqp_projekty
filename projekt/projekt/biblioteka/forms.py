from django import forms
from .models import Osoba

# przykładowy formularz dla modelu Osoba
class OsobaForm(forms.ModelForm):
    class Meta:
        model = Osoba
        fields = ['imie', 'nazwisko', 'plec', 'stanowisko']  # pola do formularza