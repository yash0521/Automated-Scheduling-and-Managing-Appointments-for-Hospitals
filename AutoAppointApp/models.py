from django.db import models
from datetime import datetime, time

DOC_TYPE = (
    ('hospital', 'HOSPITAL'),
    ('laboratory', 'LABORATORY'),
)


class Doctor(models.Model):
    name = models.CharField(max_length=40)
    mobile_no = models.IntegerField()
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=50)
    doc_type = models.CharField(choices=DOC_TYPE, max_length=10)
    degree = models.CharField(max_length=20)
    speciality = models.CharField(max_length=50)
    consult_time = models.CharField(max_length=2)
    slot1_start_time = models.TimeField()
    slot1_end_time = models.TimeField()
    slot2_start_time = models.TimeField()
    slot2_end_time = models.TimeField()


class Patient(models.Model):
    name = models.CharField(max_length=40)
    mobile_no = models.IntegerField()
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=50)
    age = models.IntegerField()
    city = models.CharField(max_length=20)
    address = models.CharField(max_length=250)


class DoctorLeave(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    slot1_start_time = models.TimeField(null=True, blank=True)
    slot1_end_time = models.TimeField(null=True, blank=True)
    slot2_start_time = models.TimeField(null=True, blank=True)
    slot2_end_time = models.TimeField(null=True, blank=True)


class HosAppointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=20)


class LabAppointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=20)
