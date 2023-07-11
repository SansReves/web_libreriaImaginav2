from django import forms
from .models import Libro, CatgLibro,Cliente,TipoCliente
from django.contrib.auth.forms import UserCreationForm

class LibroForm(forms.ModelForm):
    id_catg = forms.ModelChoiceField(queryset=CatgLibro.objects.all(), empty_label=None)

    class Meta:
        model = Libro
        fields = '__all__'

class ClienteForm(forms.ModelForm):

    id_tp_cli = forms.ModelChoiceField(queryset=TipoCliente.objects.all(), empty_label=None)

    class Meta:
        model = Cliente
        fields = '__all__'

class CustomUserCreationForm(UserCreationForm):
    pass