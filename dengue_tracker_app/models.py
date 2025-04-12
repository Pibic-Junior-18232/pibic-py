from django.db import models

from django.db import models
from django.contrib.postgres.fields import CICharField
from django.utils import timezone

class GenderEnum(models.TextChoices):
    M = 'M', 'Masculino'
    F = 'F', 'Feminino'
    N = 'N', 'Não especificado'

class CaseEnum(models.TextChoices):
    SUSPEITO = 'suspeito', 'Suspeito'
    CONFIRMADO = 'confirmado', 'Confirmado'

class DefaultColumnsModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    created_user_id = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    updated_user_id = models.IntegerField(null=True, blank=True)
    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_user_id = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True


class City(DefaultColumnsModel):
    name = models.CharField(max_length=255)
    state = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.name} - {self.state}"


class Patient(DefaultColumnsModel):
    name = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GenderEnum.choices)
    phone = models.CharField(max_length=16, null=True, blank=True)

    def __str__(self):
        return self.name


class Address(DefaultColumnsModel):
    patient = models.ForeignKey(Patient, null=True, blank=True, on_delete=models.SET_NULL)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    cep = models.IntegerField(null=True, blank=True)
    street = models.CharField(max_length=150, null=True, blank=True)
    number = models.CharField(max_length=20, null=True, blank=True)
    district = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return f"{self.street}, {self.number} - {self.district}"


class Symptom(DefaultColumnsModel):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Case(DefaultColumnsModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=CaseEnum.choices)
    notes = models.TextField(null=True, blank=True)
    symptoms = models.ManyToManyField(Symptom, through='CaseSymptom')

    def __str__(self):
        return f"Case #{self.id} - {self.status}"


class CaseSymptom(DefaultColumnsModel):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    symptom = models.ForeignKey(Symptom, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('case', 'symptom'),)
