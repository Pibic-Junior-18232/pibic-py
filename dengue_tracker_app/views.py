from django.shortcuts import render, redirect, get_object_or_404
from .models import Case, Patient, Address
from .forms import PatientForm, AddressForm, CaseForm
from django.db import transaction
from django.utils import timezone

def home_page(request):
    return render(request, 'home_page.html')

def list_cases(request):
    cases = Case.objects.filter(deleted=False).order_by('-created_at')
    return render (request, 'cases_registered.html', {"cases": cases})


def case_register_or_edit(request, case_id=None): # Funcao responsavel pela criacao e a edicao de casos.

    if case_id:
        case = get_object_or_404(Case, id=case_id, deleted=False) # Procura um objeto caso nao encontre retorna 404
        patient = case.patient
        address = case.address

    else: 
        case = None
        patient = None
        address = None

    if request.method == 'POST':
        case_form = CaseForm(request.POST, instance=case)
        patient_form = PatientForm(request.POST, instance=patient)
        address_form = AddressForm(request.POST, instance=address)

        if all([patient_form.is_valid(), address_form.is_valid(), case_form.is_valid()]):

            try: # Tente fazer tudo que esta ai dentro se der erro aborta tudo
                with transaction.atomic():

                    patient = patient_form.save()
                    address = address_form.save()

                    case = case_form.save(commit=False)

                    case.address = address
                    case.patient = patient

                    case.save()
                    case_form.save_m2m()
        
                return redirect('registros')

            except Exception as ex:
                print("Erro: ", e)    
    else:
        case_form = CaseForm(instance=case)
        patient_form = PatientForm(instance=patient)
        address_form = AddressForm(instance=address)

    return render(request, 'form_case.html', {
        'case_form': case_form,
        'patient_form': patient_form,
        'address_form': address_form,
        'mode_edit': case_id is not None, 
    })


def case_delete(request, case_id):
    
    case = get_object_or_404(Case, id=case_id, deleted=False)
    address = get_object_or_404(Address, id=case.address.id, deleted=False)

    address.deleted = True
    address.deleted_at = timezone.now()
    address.save()

    case.deleted = True
    case.deleted_at = timezone.now()
    case.save()

    return redirect('registros')    