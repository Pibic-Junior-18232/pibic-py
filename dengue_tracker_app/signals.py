from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Symptom, City


@receiver(post_migrate)
def create_defaults_symptom(sender, **kwargs):

    if Symptom.objects.exists():
        return

    symptoms = [
        Symptom(name="Febre alta", description="Início súbito, geralmente acima de 38.5°C."),
        Symptom(name="Dor de cabeça", description="Dor intensa, principalmente atrás dos olhos."),
        Symptom(name="Dor no corpo", description="Dores musculares e nas articulações."),
        Symptom(name="Fadiga", description="Cansaço extremo, mesmo em repouso."),
        Symptom(name="Náusea e vômito", description="Sensação de enjoo e episódios de vômito."),
        Symptom(name="Manchas vermelhas", description="Erupções cutâneas que podem aparecer pelo corpo."),
        Symptom(name="Dor abdominal", description="Dor persistente na região do abdômen."),
        Symptom(name="Perda de apetite", description="Falta de vontade de se alimentar."),
        Symptom(name="Sangramentos", description="Gengivais, nasais ou nas fezes em casos mais graves."),
    ]
    Symptom.objects.bulk_create(symptoms)

@receiver(post_migrate)
def create_default_city(sender, **kwargs):

    if City.objects.exists():
        return
    
    city = [
        City(name="Dracena", state="SP")
    ]
    City.objects.bulk_create(city)
    
