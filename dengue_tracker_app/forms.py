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
            'phone': TextInput(attrs={'class': 'form-control', 'maxlength': '15'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['birth_date'].required = True
        self.fields['gender'].required = True
        self.fields['phone'].required = True

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['city', 'cep', 'street', 'number', 'district', 'patient']
        widgets = {
            'city': Select(attrs={'class': 'form-select'}),
            'cep': TextInput(attrs={'class': 'form-control', 'maxlength': '9'}),
            'street': TextInput(attrs={'class': 'form-control'}),
            'number': TextInput(attrs={'class': 'form-control'}),
            'district': TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].required = True
        self.fields['cep'].required = False
        self.fields['street'].required = True
        self.fields['number'].required = True
        self.fields['district'].required = True
        self.fields['cep'].initial = '17900-163'

    def clean(self):
        cleaned_data = super().clean()
        cep = cleaned_data.get('cep')
        if cep:
            cleaned_data['cep'] = int(str(cep).replace('-', ''))
        return cleaned_data

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
        self.fields['status'].required = True
        self.fields['notes'].required = False
        self.fields['symptoms'].required = False