from django.shortcuts import render, redirect
from .models import Case
from .forms import PatientForm, AddressForm, CaseForm
from django.db import transaction

def home_page(request):
    return render(request, 'home_page.html')

def list_cases(request):
    cases = Case.objects.all()
    return render (request, 'cases_registered.html', {"cases": cases})


def register_case(request):
    
    if request.method == 'POST':
        patient_form = PatientForm(request.POST)
        address_form = AddressForm(request.POST)
        case_form = CaseForm(request.POST)
        
        if all([patient_form.is_valid(), address_form.is_valid(), case_form.is_valid()]):
            patient = patient_form.save()
            address = address_form.save(commit=False)
            address.patient = patient
            address.save()
            
            case = case_form.save(commit=False)
            case.patient = patient
            case.address = address
            case.save()
            case_form.save_m2m()  # para salvar os sintomas

            return redirect('registros')
    else:
        patient_form = PatientForm()
        address_form = AddressForm()
        case_form = CaseForm()

    
    context = {
        'patient_form': patient_form,
        'address_form': address_form,
        'case_form': case_form,
    }

    return render(request, 'register_case.html', context)