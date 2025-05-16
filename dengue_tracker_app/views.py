from django.shortcuts import render, redirect, get_object_or_404
from .models import Case, Patient, Address
from .forms import PatientForm, AddressForm, CaseForm
from django.db import transaction
from django.utils import timezone

from gmplot import gmplot
import googlemaps
import webbrowser

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
        address.latitude = None
        address.longitude = None

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

                    address = address_form.save(commit=False)
                    address.patient_id = patient.id
                    address.save()         

                    case = case_form.save(commit=False)
                    case.address_id = address.id
                    case.patient_id = patient.id

                    case.save()
                    case_form.save_m2m()
        
                return redirect('registros')

            except Exception as ex:
                print("Erro: ", ex)    
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
    patient = get_object_or_404(Patient, id=case.patient.id, deleted=False)

    address.deleted = True
    address.deleted_at = timezone.now()
    address.save()

    patient.deleted = True
    patient.deleted_at = timezone.now()
    patient.save()

    case.deleted = True
    case.deleted_at = timezone.now()
    case.save()

    return redirect('registros')    

def home_dashboard(request):
    return render(request, 'home_dashboard.html')

def set_lat_long(): # Funcao que vai chamar a api. Serve unicamente para setar os valores
    addresses = Address.objects.filter(latitude=None, longitude=None) # So coleta os enderecos que ainda nao tem valor em 'latitude' e 'longitude'
      
    apikey = 'AIzaSyCXiKI8zhQ4pZwbxwyunA-rdKFe2CzMpkA'
    coord = googlemaps.Client(key=apikey)  

    for ad in addresses:
        message = f'{ad.street}, {ad.district}, {ad.number}, Dracena, SP'

        geocode_result = coord.geocode(message)
        print(ad)

        latitude = geocode_result[0]['geometry']['location']['lat']
        longitude = geocode_result[0]['geometry']['location']['lng']

        ad.latitude = latitude
        ad.longitude = longitude
        ad.street = geocode_result[0]['address_components'][0]['short_name']
        print('setou')
        ad.save()


def generate_map(request):
    set_lat_long()

    addresses = Address.objects.all()

    apikey = 'AIzaSyCXiKI8zhQ4pZwbxwyunA-rdKFe2CzMpkA'
    coord = googlemaps.Client(key=apikey)  

    # Onde Abre o Google maps
    gmap = gmplot.GoogleMapPlotter(-21.4857339, -51.532612, 14, apikey=apikey)


    for ad in addresses:
        gmap.marker(ad.latitude, ad.longitude, color='red')
        print('marker')

    gmap.draw('map.html')

    return redirect('registros')