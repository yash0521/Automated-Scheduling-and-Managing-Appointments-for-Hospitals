from django.contrib import admin

from AutoAppointApp.models import Doctor
from AutoAppointApp.models import Patient
from AutoAppointApp.models import DoctorLeave
from AutoAppointApp.models import HosAppointment
from AutoAppointApp.models import LabAppointment

admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(DoctorLeave)
admin.site.register(HosAppointment)
admin.site.register(LabAppointment)
