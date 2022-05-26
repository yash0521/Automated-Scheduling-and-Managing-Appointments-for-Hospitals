from django.contrib import admin
from django.urls import path

from AutoAppoint import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name="home"),
    path('index/', views.index, name="index"),

    path('register/', views.register, name="register"),
    path('login-patient/', views.login_patient, name="login"),
    path('patient-dashboard/', views.patient_dashboard, name="patient-dashboard"),
    path('profile-settings/', views.prof_settings, name="profile-settings"),
    path('change-password/', views.change_password, name="change-password"),
    path('doctor-profile/<int:id2>', views.doc_prof, name="doctor-profile"),
    path('hos-appointment/', views.book_hos_appointment, name="book_hos_appointment"),
    path('delete-hos-appointment/<int:id5>', views.delete_hos_appointment, name="delete-hos-appointment"),
    path('lab-appointment/', views.book_lab_appointment, name="book_lab_appointment"),
    path('delete-lab-appointment/<int:id6>', views.delete_lab_appointment, name="delete-lab-appointment"),
    path('booking/<int:id3>', views.booking, name="booking"),
    path('lab-booking/<int:id4>', views.lab_booking, name="lab-booking"),
    path('pat-logout/', views.pat_logout, name="pat-logout"),
    path('forgot-password/', views.forgot_password, name="forgot-password"),

    path('doctor-register/', views.doctor_register, name="doctor-register"),
    path('login-doctor/', views.login_doctor, name="login"),
    path('doctor-dashboard/', views.doc_dashboard, name="doc-dashboard"),
    path('status-edit/<int:id8>', views.status_edit, name="status-edit"),
    path('lab-status-edit/<int:id9>', views.lab_status_edit, name="lab-status-edit"),
    path('doc-delete-hos-appointment/<int:id10>', views.doc_delete_hos_appointment, name="doc-delete-hos-appointment"),
    path('doc-delete-lab-appointment/<int:id11>', views.doc_delete_lab_appointment, name="doc-delete-lab-appointment"),
    path('doctor-profile-settings/', views.doc_prof_settings, name="doctor-profile-settings"),
    path('doctor-change-password/', views.doc_change_password, name="doc-change-password"),
    path('my-patients/', views.my_patients, name="my-patients"),
    path('schedule-timings/', views.schedule_timings, name="schedule-timings"),
    path('leave-list/', views.leave_list, name="leave-list"),
    path('leave-delete/<int:id1>', views.leave_delete, name="leave-delete"),
    path('patient-profile/<int:id7>', views.patient_profile, name="patient-profile"),
    path('doc-lab-appointment/<int:id13>', views.doc_book_lab_appointment, name="doc_book_lab_appointment"),
    path('doc-side-lab-booking/<int:id12>/<int:id13>', views.doc_side_lab_booking, name="doc-side-lab-booking"),
    path('doc-logout/', views.doc_logout, name="doc-logout"),
]
