from django.shortcuts import render, redirect, get_object_or_404
from .models import Case, Patient, Address
from .forms import PatientForm, AddressForm, CaseForm
from django.db import transaction
from django.utils import timezone

from gmplot import gmplot
from pathlib import Path
from django.conf import settings
import googlemaps
import webbrowser
import os

static_dir = Path(__file__).resolve().parent / 'static'

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

    addresses_without_coords = Address.objects.filter(deleted=False, latitude__isnull=True).exists()
    addresses_with_coords = Address.objects.filter(deleted=False, latitude__isnull=False).exists()

    dengue_static_dir = Path(__file__).resolve().parent / 'static'
    os.makedirs(dengue_static_dir, exist_ok=True)
    map_file = os.path.join(dengue_static_dir, 'map.html')

    map_url = settings.STATIC_URL + 'map.html'

    if addresses_with_coords and not os.path.exists(map_file):
        apikey = 'AIzaSyCXiKI8zhQ4pZwbxwyunA-rdKFe2CzMpkA'
        gmap = gmplot.GoogleMapPlotter(-21.4857339, -51.532612, 14, apikey=apikey)

        for ad in Address.objects.filter(deleted=False, latitude__isnull=False):
            gmap.marker(float(ad.latitude), float(ad.longitude), color='red')

        gmap.draw(map_file)

    context = {
        'map_url': map_url if addresses_with_coords else None,
        'needs_update': addresses_without_coords,
        'has_addresses': addresses_with_coords or addresses_without_coords
    }

    return render(request, 'home_dashboard.html', context)

def set_lat_long(): # Funcao que vai chamar a api. Serve unicamente para setar os valores
    addresses = Address.objects.filter(deleted=False, latitude__isnull=True, longitude__isnull=True) # So coleta os enderecos que ainda nao tem valor em 'latitude' e 'longitude'
      
    apikey = 'AIzaSyCXiKI8zhQ4pZwbxwyunA-rdKFe2CzMpkA'
    coord = googlemaps.Client(key=apikey)  

    for ad in addresses:

        message = f'{ad.cep}, {ad.street}, {ad.district}, {ad.number}, Dracena, SP'

        geocode_result = coord.geocode(message)

        ad.latitude = geocode_result[0]['geometry']['location']['lat']
        ad.longitude = geocode_result[0]['geometry']['location']['lng']
        print('kurintiaa')
        street_name = ad.street
        for i in (0, 1):
            short = geocode_result[0]['address_components'][i]['long_name']
            print(short)
            if short.startswith('R.') or short.startswith('Rua') or short.startswith('Avenida') or short.startswith('Av.'):
                street_name = short
                break

        ad.street = street_name
        ad.save()


def generate_map(request):
    addresses_without_coords = Address.objects.filter(deleted=False, latitude__isnull=True, longitude__isnull=True)
    if addresses_without_coords.exists():
        print('chamouu')
        set_lat_long()

    addresses = Address.objects.filter(deleted=False, latitude__isnull=False, longitude__isnull=False)

    apikey = 'AIzaSyCXiKI8zhQ4pZwbxwyunA-rdKFe2CzMpkA'
    gmap = gmplot.GoogleMapPlotter(-21.4857339, -51.532612, 14, apikey=apikey)

    for ad in addresses:
        gmap.marker(float(ad.latitude), float(ad.longitude), color='red')

    # Caminho para salvar o mapa apenas em static dentro do app
    dengue_static_dir = Path(__file__).resolve().parent / 'static'
    dengue_static_dir.mkdir(exist_ok=True)
    map_file = dengue_static_dir / 'map.html'

    gmap.draw(str(map_file))

    return redirect('home_dashboard')