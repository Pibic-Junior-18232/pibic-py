from django import forms
from .models import Patient, Address, Case
from django.forms.widgets import DateInput, TextInput, Select, Textarea, NumberInput

class PatientForm(forms.ModelForm): # "ModelForm" nos permite transitar com os dados.
    class Meta: # Classe interna do django
        model = Patient # Neste campo defino o model que quero manipular
        fields = ['name', 'birth_date', 'gender', 'phone'] # Neste campo defino os campos que serao incluidos no formulario
        widgets = { # "Widgets" com os fields acima voce define a ele um "widget" (TextInput) que sera renderizado no HTML como um "input" do type="text"
            'name': TextInput(attrs={'class': 'form-control'}), # Tambem e possivel inserir classes do CSS
            'birth_date': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': Select(attrs={'class': 'form-select'}),
            'phone': TextInput(attrs={'class': 'form-control'}),
        }

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['city', 'cep', 'street', 'number', 'district', 'patient']
        widgets = {
            'city': Select(attrs={'class': 'form-select'}),
            'cep': NumberInput(attrs={'class': 'form-control'}),
            'street': TextInput(attrs={'class': 'form-control'}),
            'number': TextInput(attrs={'class': 'form-control'}),
            'district': TextInput(attrs={'class': 'form-control'}),
        }

class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['status', 'notes', 'symptoms']
        widgets = {
            'status': Select(attrs={'class': 'form-select'}),
            'notes': Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'symptoms': forms.CheckboxSelectMultiple(),
        }

def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['symptoms'].required = False