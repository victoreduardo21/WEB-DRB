from django import forms
from .models import Terminal, Caminhoneiro

class TerminalForm(forms.ModelForm):
    class Meta:
        model = Terminal
        fields = ['nome', 'latitude', 'longitude', 'raio']

class CaminhoneiroForm(forms.ModelForm):
    class Meta:
        model = Caminhoneiro
        fields = ['nome', 'cpf', 'id_motorista']
