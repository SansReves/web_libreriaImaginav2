from django import forms
from .models import Libro, CatgLibro

class LibroForm(forms.ModelForm):
    id_catg = forms.ModelChoiceField(queryset=CatgLibro.objects.all(), empty_label=None)

    class Meta:
        model = Libro
        fields = '__all__'

