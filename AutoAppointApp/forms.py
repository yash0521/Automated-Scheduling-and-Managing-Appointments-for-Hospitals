from django.core.validators import RegexValidator
from django.forms import ModelForm
from django import forms

from AutoAppointApp.models import Patient, Doctor, DoctorLeave


class PatientRegisterForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control floating'}))
    mobile_no = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control floating'}), validators=[RegexValidator('^[6-9]{1}[0-9]{9}$', message='Please Enter Valid Mobile Number')])
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control floating'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control floating'}))
    age = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control floating'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control floating'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control floating'}))

    class Meta:
        model = Patient
        fields = "__all__"


class PatientEditForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    mobile_no = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), validators=[RegexValidator('^[6-9]{1}[0-9]{9}$', message='Please Enter Valid Mobile Number')])
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    age = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Patient
        fields = {'name', 'mobile_no', 'email', 'age', 'city', 'address'}


DOC_TYPE = (
    ('hospital', 'HOSPITAL'),
    ('laboratory', 'LABORATORY'),
)


class DoctorRegisterForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control floating'}))
    mobile_no = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control floating'}), validators=[RegexValidator('^[6-9]{1}[0-9]{9}$', message='Please Enter Valid Mobile Number')])
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control floating'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control floating'}))
    doc_type = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control floating'}), choices=DOC_TYPE)
    degree = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control floating'}))
    speciality = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control floating'}))
    consult_time = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control floating'}), validators=[RegexValidator('^[0-5]{1}[0-9]{1}$', message='Please Enter Valid Time Format(in minutes)')])
    slot1_start_time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control floating', 'type': 'time'}))
    slot1_end_time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control floating', 'type': 'time'}))
    slot2_start_time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control floating', 'type': 'time'}))
    slot2_end_time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control floating', 'type': 'time'}))

    class Meta:
        model = Doctor
        fields = "__all__"


class DoctorEditForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control floating'}))
    mobile_no = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control floating'}), validators=[
        RegexValidator('^[6-9]{1}[0-9]{9}$', message='Please Enter Valid Mobile Number')])
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control floating'}))
    doc_type = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control floating'}), choices=DOC_TYPE)
    degree = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control floating'}))
    speciality = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control floating'}))
    consult_time = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control floating'}), validators=[
        RegexValidator('^[0-5]{1}[0-9]{1}$', message='Please Enter Valid Time Format(in minutes)')])
    slot1_start_time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control floating', 'type': 'time'}))
    slot1_end_time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control floating', 'type': 'time'}))
    slot2_start_time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control floating', 'type': 'time'}))
    slot2_end_time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control floating', 'type': 'time'}))

    class Meta:
        model = Doctor
        fields = {'name', 'mobile_no', 'email', 'doc_type', 'degree', 'speciality', 'consult_time', 'slot1_start_time',
                  'slot1_end_time', 'slot2_start_time', 'slot2_end_time'}



