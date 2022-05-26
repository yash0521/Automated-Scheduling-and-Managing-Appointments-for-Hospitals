from django.shortcuts import render, redirect
from AutoAppointApp.forms import PatientRegisterForm, DoctorRegisterForm, PatientEditForm, DoctorEditForm
from django.contrib import messages
from AutoAppointApp.models import Patient, Doctor, DoctorLeave, HosAppointment, LabAppointment
from datetime import timedelta, datetime, time


def home(request):
    d_data = Doctor.objects.all()
    context = {'d_data': d_data}
    return render(request, "index.html", context)


def index(request):
    return render(request, "index.html")


def register(request):
    form = PatientRegisterForm()
    if request.method == "POST":
        form = PatientRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Register successfully...", extra_tags='reg_success')
            return redirect(login_patient)

    return render(request, "register.html", {'form': form})


def login_patient(request):
    if request.method == 'POST':
        login_mobile = request.POST['mobile']
        login_password = request.POST['password']

        pcount = Patient.objects.filter(mobile_no=login_mobile, password=login_password).count()

        if pcount > 0:
            pget = Patient.objects.get(mobile_no=login_mobile, password=login_password)
            request.session['id'] = pget.id
            request.session['name'] = pget.name
            request.session['user_type'] = 'Patient'

            return redirect(patient_dashboard)
        else:
            messages.error(request, "Invalid username or password.", extra_tags='log_success')
            return redirect(login_patient)

    return render(request, "login.html")


def patient_dashboard(request):
    if "id" in request.session:
        id = request.session['id']
        p_data = Patient.objects.get(pk=id)
        h_appoint = HosAppointment.objects.filter(patient=id)
        l_appoint = LabAppointment.objects.filter(patient=id)
        context = {'p_data': p_data, 'h_appoint': h_appoint, 'l_appoint': l_appoint}
        return render(request, "patient-dashboard.html", context)
    else:
        return redirect(home)


def prof_settings(request):
    if "id" in request.session:
        pid = request.session['id']
        p_data = Patient.objects.get(id=pid)
        form = PatientEditForm(instance=p_data)

        if request.method == 'POST':
            form = PatientEditForm(request.POST, instance=p_data)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated successfully...")
                return redirect(prof_settings)
        context = {'form': form, 'p_data': p_data}
        return render(request, "profile-settings.html", context)
    else:
        return redirect(home)


def change_password(request):
    if "id" in request.session:
        pid = request.session['id']
        p_data = Patient.objects.get(id=pid)
        if request.method == 'POST':
            oldpass = request.POST['oldpass']
            newpass1 = request.POST['newpass1']
            newpass2 = request.POST['newpass2']

            pcount = Patient.objects.filter(id=pid, password=oldpass).count()

            if pcount > 0:
                if newpass1 == newpass2:
                    fm = Patient.objects.get(id=pid)
                    fm.password = newpass1
                    fm.save(force_update=True)
                    messages.success(request, "Password changed successfully...", extra_tags='success')
                else:
                    messages.error(request, "Invalid old password or Password does not match", extra_tags='error')
            else:
                messages.error(request, "You have entered wrong old password", extra_tags='error')
        context = {'p_data': p_data}
        return render(request, "change-password.html", context)
    else:
        return redirect(home)


def doc_prof(request, id2):
    if "id" in request.session:
        d_data = Doctor.objects.get(id=id2)
        context = {'d_data': d_data}
        return render(request, "doctor-profile.html", context)
    else:
        return redirect(home)


def book_hos_appointment(request):
    if "id" in request.session:
        pid = request.session['id']
        p_data = Patient.objects.get(id=pid)
        d_data = Doctor.objects.filter(doc_type='hospital')
        context = {'p_data': p_data, 'd_data': d_data}
        return render(request, "search.html", context)
    else:
        return redirect(home)


def delete_hos_appointment(request, id5):
    if "id" in request.session:
        d_data = HosAppointment.objects.get(id=id5)
        d_data.delete()
        return redirect(patient_dashboard)
    else:
        return redirect(home)


def book_lab_appointment(request):
    if "id" in request.session:
        pid = request.session['id']
        p_data = Patient.objects.get(id=pid)
        d_data = Doctor.objects.filter(doc_type='laboratory')
        context = {'p_data': p_data, 'd_data': d_data}
        return render(request, "lab-search.html", context)
    else:
        return redirect(home)


def delete_lab_appointment(request, id6):
    if "id" in request.session:
        d_data = LabAppointment.objects.get(id=id6)
        d_data.delete()
        return redirect(patient_dashboard)
    else:
        return redirect(home)


def time_slot(start, end, ct):
    s_time = datetime.strptime(start, '%H:%M:%S')
    e_time = datetime.strptime(end, '%H:%M:%S')

    curr = s_time
    range = []

    while curr < e_time:
        range.append(curr.strftime("%H:%M"))
        curr = curr + timedelta(minutes=ct)
    return range


def booking(request, id3):
    if "id" in request.session:
        pid = request.session['id']
        p_data = Patient.objects.get(id=pid)
        d_data = Doctor.objects.get(id=id3)

        if request.method == 'POST':
            dt = request.POST.get('date')
            st = 'pending'

            t1 = d_data.slot1_start_time
            t2 = d_data.slot1_end_time
            t3 = d_data.slot2_start_time
            t4 = d_data.slot2_end_time
            ct = int(d_data.consult_time)

            lcount = DoctorLeave.objects.filter(doctor=id3, date=dt).count()
            if lcount > 0:
                bcount = HosAppointment.objects.filter(patient=pid, doctor=id3, date=dt, status=st).count()
                if bcount > 0:
                    messages.error(request, 'Your appointment on this date is already pending', extra_tags='error')
                else:
                    leave_data = DoctorLeave.objects.get(doctor=id3, date=dt)

                    l1 = leave_data.slot1_start_time
                    l2 = leave_data.slot1_end_time
                    l3 = leave_data.slot2_start_time
                    l4 = leave_data.slot2_end_time

                    if l1 is None and l2 is None:
                        r1t1 = str(t1)
                        r1t2 = str(t2)
                        r2t1 = str(t2)
                        r2t2 = str(t2)
                        s1 = time_slot(r1t1, r1t2, ct)
                        s2 = time_slot(r2t1, r2t2, ct)
                    else:
                        r1t1 = str(t1)
                        r1t2 = str(l1)
                        r2t1 = str(l2)
                        r2t2 = str(t2)
                        s1 = time_slot(r1t1, r1t2, ct)
                        s2 = time_slot(r2t1, r2t2, ct)

                    if l3 is None and l4 is None:
                        r3t1 = str(t3)
                        r3t2 = str(t4)
                        r4t1 = str(t4)
                        r4t2 = str(t4)
                        s3 = time_slot(r3t1, r3t2, ct)
                        s4 = time_slot(r4t1, r4t2, ct)
                    else:
                        r3t1 = str(t3)
                        r3t2 = str(l3)
                        r4t1 = str(l4)
                        r4t2 = str(t4)
                        s3 = time_slot(r3t1, r3t2, ct)
                        s4 = time_slot(r4t1, r4t2, ct)

                    array = s1 + s2 + s3 + s4

                    for i in array:
                        time1 = datetime.strptime(i, '%H:%M').time()
                        hcount = HosAppointment.objects.filter(doctor=id3, date=dt, appointment_time=time1).count()

                        if hcount == 0:
                            hget = HosAppointment(patient=p_data, doctor=d_data, date=dt, appointment_time=time1, status=st)
                            hget.save()
                            messages.success(request, "Your appointment is booked successfully", extra_tags='book-success')
                            break

            else:
                bcount = HosAppointment.objects.filter(patient=pid, doctor=id3, date=dt, status=st).count()
                if bcount > 0:
                    messages.error(request, 'Your appointment on this date is already pending', extra_tags='error')
                else:
                    r1t1 = str(t1)
                    r1t2 = str(t2)
                    r2t1 = str(t3)
                    r2t2 = str(t4)

                    s1 = time_slot(r1t1, r1t2, ct)
                    s2 = time_slot(r2t1, r2t2, ct)

                    array = s1 + s2
                    for i in array:
                        time1 = datetime.strptime(i, '%H:%M').time()
                        hcount = HosAppointment.objects.filter(doctor=id3, date=dt, appointment_time=time1).count()

                        if hcount == 0:
                            hget = HosAppointment(patient=p_data, doctor=d_data, date=dt, appointment_time=time1, status=st)
                            hget.save()
                            messages.success(request, "Your appointment is booked successfully", extra_tags='book-success')
                            break

        context = {'p_data': p_data, 'd_data': d_data}
        return render(request, "booking.html", context)
    else:
        return redirect(home)


def lab_booking(request, id4):
    if "id" in request.session:
        pid = request.session['id']
        p_data = Patient.objects.get(id=pid)
        d_data = Doctor.objects.get(id=id4)

        if request.method == 'POST':
            dt = request.POST.get('date')
            st = 'pending'

            t1 = d_data.slot1_start_time
            t2 = d_data.slot1_end_time
            t3 = d_data.slot2_start_time
            t4 = d_data.slot2_end_time
            ct = int(d_data.consult_time)

            lcount = DoctorLeave.objects.filter(doctor=id4, date=dt).count()
            if lcount > 0:
                bcount = LabAppointment.objects.filter(patient=pid, doctor=id4, date=dt, status=st).count()
                if bcount > 0:
                    messages.error(request, 'Your appointment on this date is already pending', extra_tags='error')
                else:
                    leave_data = DoctorLeave.objects.get(doctor=id4, date=dt)

                    l1 = leave_data.slot1_start_time
                    l2 = leave_data.slot1_end_time
                    l3 = leave_data.slot2_start_time
                    l4 = leave_data.slot2_end_time

                    if l1 is None and l2 is None:
                        r1t1 = str(t1)
                        r1t2 = str(t2)
                        r2t1 = str(t2)
                        r2t2 = str(t2)
                        s1 = time_slot(r1t1, r1t2, ct)
                        s2 = time_slot(r2t1, r2t2, ct)
                    else:
                        r1t1 = str(t1)
                        r1t2 = str(l1)
                        r2t1 = str(l2)
                        r2t2 = str(t2)
                        s1 = time_slot(r1t1, r1t2, ct)
                        s2 = time_slot(r2t1, r2t2, ct)

                    if l3 is None and l4 is None:
                        r3t1 = str(t3)
                        r3t2 = str(t4)
                        r4t1 = str(t4)
                        r4t2 = str(t4)
                        s3 = time_slot(r3t1, r3t2, ct)
                        s4 = time_slot(r4t1, r4t2, ct)
                    else:
                        r3t1 = str(t3)
                        r3t2 = str(l3)
                        r4t1 = str(l4)
                        r4t2 = str(t4)
                        s3 = time_slot(r3t1, r3t2, ct)
                        s4 = time_slot(r4t1, r4t2, ct)

                    array = s1 + s2 + s3 + s4

                    for i in array:
                        time1 = datetime.strptime(i, '%H:%M').time()
                        lab_count = LabAppointment.objects.filter(doctor=id4, date=dt, appointment_time=time1).count()

                        if lab_count == 0:
                            lget = LabAppointment(patient=p_data, doctor=d_data, date=dt, appointment_time=time1, status=st)
                            lget.save()
                            messages.success(request, "Your appointment is booked successfully", extra_tags='book-success')
                            break

            else:
                bcount = LabAppointment.objects.filter(patient=pid, doctor=id4, date=dt, status=st).count()
                if bcount > 0:
                    messages.error(request, 'Your appointment on this date is already pending', extra_tags='error')
                else:
                    r1t1 = str(t1)
                    r1t2 = str(t2)
                    r2t1 = str(t3)
                    r2t2 = str(t4)

                    s1 = time_slot(r1t1, r1t2, ct)
                    s2 = time_slot(r2t1, r2t2, ct)

                    array = s1 + s2
                    for i in array:
                        time1 = datetime.strptime(i, '%H:%M').time()
                        lab_count = LabAppointment.objects.filter(doctor=id4, date=dt, appointment_time=time1).count()

                        if lab_count == 0:
                            lget = LabAppointment(patient=p_data, doctor=d_data, date=dt, appointment_time=time1, status=st)
                            lget.save()
                            messages.success(request, "Your appointment is booked successfully", extra_tags='book-success')
                            break

        context = {'p_data': p_data, 'd_data': d_data}
        return render(request, "lab-booking.html", context)
    else:
        return redirect(home)


def pat_logout(request):
    if "id" in request.session:
        del request.session['id']
        del request.session['name']
        del request.session['user_type']
        return redirect(login_patient)
    else:
        return redirect(home)


def forgot_password(request):
    return render(request, "forgot-password.html")


def doctor_register(request):
    form = DoctorRegisterForm()
    if request.method == "POST":
        form = DoctorRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Register successfully", extra_tags='doc_log_success')
            return redirect(login_doctor)

    return render(request, "doctor-register.html", {'form': form})


def login_doctor(request):
    if request.method == 'POST':
        login_mobile = request.POST['mobile']
        login_password = request.POST['password']

        dcount = Doctor.objects.filter(mobile_no=login_mobile, password=login_password).count()

        if dcount > 0:
            dget = Doctor.objects.get(mobile_no=login_mobile, password=login_password)
            request.session['id'] = dget.id
            request.session['name'] = dget.name
            request.session['user_type'] = 'Doctor'

            return redirect(doc_dashboard)
        else:
            messages.error(request, "Invalid username or password.", extra_tags='doc_log_fail')
            return redirect(login_doctor)

    return render(request, "login-doctor.html")


def doc_dashboard(request):
    if "id" in request.session:
        id = request.session['id']
        d_data = Doctor.objects.get(pk=id)
        h_appoint = HosAppointment.objects.filter(doctor=id)
        l_appoint = LabAppointment.objects.filter(doctor=id)
        context = {'d_data': d_data, 'h_appoint': h_appoint, 'l_appoint': l_appoint}
        a = d_data.doc_type
        if a == 'hospital':
            return render(request, "doctor-dashboard.html", context)
        else:
            return render(request, "lab-doctor-dashboard.html", context)
    else:
        return redirect(home)


def status_edit(request, id8):
    if "id" in request.session:
        did = request.session['id']
        d_data = Doctor.objects.get(pk=did)
        h_appoint = HosAppointment.objects.get(id=id8)

        if request.method == 'POST':
            newstatus = request.POST['status']
            fm = HosAppointment.objects.get(id=id8)
            fm.status = newstatus
            fm.save(force_update=True)
            messages.success(request, "Status changed successfully...", extra_tags='success')
            return redirect(doc_dashboard)

        context = {'d_data': d_data, 'h_appoint': h_appoint}
        return render(request, "edit-prescription.html", context)
    else:
        return redirect(home)


def lab_status_edit(request, id9):
    if "id" in request.session:
        did = request.session['id']
        d_data = Doctor.objects.get(pk=did)
        l_appoint = LabAppointment.objects.get(id=id9)

        if request.method == 'POST':
            newstatus = request.POST['status']
            fm = LabAppointment.objects.get(id=id9)
            fm.status = newstatus
            fm.save(force_update=True)
            messages.success(request, "Status changed successfully...", extra_tags='success')
            return redirect(lab_doc_dashboard)

        context = {'d_data': d_data, 'l_appoint': l_appoint}
        return render(request, "lab-edit-prescription.html", context)
    else:
        return redirect(home)


def doc_delete_hos_appointment(request, id10):
    if "id" in request.session:
        d_data = HosAppointment.objects.get(id=id10)
        d_data.delete()
        return redirect(doc_dashboard)
    else:
        return redirect(home)


def doc_delete_lab_appointment(request, id11):
    if "id" in request.session:
        d_data = LabAppointment.objects.get(id=id11)
        d_data.delete()
        return redirect(lab_doc_dashboard)
    else:
        return redirect(home)


def doc_prof_settings(request):
    if "id" in request.session:
        did = request.session['id']
        d_data = Doctor.objects.get(id=did)
        form = DoctorEditForm(instance=d_data)

        if request.method == 'POST':
            form = DoctorEditForm(request.POST, instance=d_data)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated successfully...")
                return redirect(doc_prof_settings)
        context = {'form': form, 'd_data': d_data}
        return render(request, "doctor-profile-settings.html", context)
    else:
        return redirect(home)


def doc_change_password(request):
    if "id" in request.session:
        did = request.session['id']
        d_data = Doctor.objects.get(id=did)

        if request.method == 'POST':
            oldpass = request.POST['oldpass']
            newpass1 = request.POST['newpass1']
            newpass2 = request.POST['newpass2']

            dcount = Doctor.objects.filter(id=did, password=oldpass).count()

            if dcount > 0:
                if newpass1 == newpass2:
                    fm = Doctor.objects.get(id=did)
                    fm.password = newpass1
                    fm.save(force_update=True)
                    messages.success(request, "Password changed successfully...", extra_tags='success')
                else:
                    messages.error(request, "Invalid old password or Password does not match", extra_tags='error')
            else:
                messages.error(request, "You have entered wrong old password", extra_tags='error')
        context = {'d_data': d_data}
        return render(request, "doctor-change-password.html", context)
    else:
        return redirect(home)


def my_patients(request):
    if "id" in request.session:
        did = request.session['id']
        d_data = Doctor.objects.get(id=did)
        h_appoint_id = HosAppointment.objects.values('patient').filter(doctor=did).distinct()
        h_appoint = Patient.objects.filter(id__in=h_appoint_id)

        l_appoint_id = LabAppointment.objects.values('patient').filter(doctor=did).distinct()
        l_appoint = Patient.objects.filter(id__in=l_appoint_id)
        context = {'d_data': d_data, 'h_appoint': h_appoint, 'l_appoint': l_appoint}
        a = d_data.doc_type
        if a == 'hospital':
            return render(request, "my-patients.html", context)
        else:
            return render(request, "lab-my-patients.html", context)
    else:
        return redirect(home)


def schedule_timings(request):
    if "id" in request.session:
        did = request.session['id']
        d_data = Doctor.objects.get(id=did)

        t1 = d_data.slot1_start_time
        t2 = d_data.slot1_end_time
        t3 = d_data.slot2_start_time
        t4 = d_data.slot2_end_time

        if request.method == 'POST':
            dt = request.POST.get('date')
            s1s = request.POST.get('start_time1')
            s1e = request.POST.get('end_time1')
            s2s = request.POST.get('start_time2')
            s2e = request.POST.get('end_time2')

            leave_date = DoctorLeave.objects.filter(doctor=d_data, date=dt).count()
            if leave_date == 0:
                if s1s == '' and s1e == '' and s2s == '' and s2e == '':
                    messages.error(request, "Fill at least one slot", extra_tags='error')

                elif (s1s == '' and s1e != '') or (s1s != '' and s1e == '') or (s2s == '' and s2e != '') or (
                        s2s != '' and s2e == ''):
                    messages.error(request, "Fill start time and end time both ", extra_tags='error')

                elif s2s == '' or s2e == '':
                    s2s = None
                    s2e = None

                    ts1s = datetime.strptime(s1s, "%H:%M").time()
                    ts1e = datetime.strptime(s1e, "%H:%M").time()

                    if t1 <= ts1s <= ts1e <= t2:
                        leave_data = DoctorLeave(doctor=d_data, date=dt, slot1_start_time=s1s, slot1_end_time=s1e,
                                                 slot2_start_time=s2s, slot2_end_time=s2e)
                        leave_data.save()
                        messages.success(request, "Leave added successfully...", extra_tags='success')
                    else:
                        messages.error(request, "Entered leave time is not in slot-1/slot-2 ", extra_tags='error')

                elif s1s == '' or s1e == '':
                    s1s = None
                    s1e = None

                    ts2s = datetime.strptime(s2s, "%H:%M").time()
                    ts2e = datetime.strptime(s2e, "%H:%M").time()

                    if t3 <= ts2s <= ts2e <= t4:
                        leave_data = DoctorLeave(doctor=d_data, date=dt, slot1_start_time=s1s, slot1_end_time=s1e,
                                                 slot2_start_time=s2s, slot2_end_time=s2e)
                        leave_data.save()
                        messages.success(request, "Leave added successfully...", extra_tags='success')
                    else:
                        messages.error(request, "Entered leave time is not in slot-1/slot-2 ", extra_tags='error')

                else:
                    leave_data = DoctorLeave(doctor=d_data, date=dt, slot1_start_time=s1s, slot1_end_time=s1e,
                                             slot2_start_time=s2s, slot2_end_time=s2e)
                    leave_data.save()
                    messages.success(request, "Leave added successfully...", extra_tags='success')
            else:
                messages.error(request, "This date has already in your leave", extra_tags='error')

            return redirect(schedule_timings)
        context = {'d_data': d_data}
        return render(request, "schedule-timings.html", context)
    else:
        return redirect(home)


def leave_list(request):
    if "id" in request.session:
        did = request.session['id']
        d_data = Doctor.objects.get(id=did)
        dl_data = DoctorLeave.objects.filter(doctor=did)
        context = {'d_data': d_data, 'dl_data': dl_data}
        return render(request, "leave-list.html", context)
    else:
        return redirect(home)


def leave_delete(request, id1):
    if "id" in request.session:
        d_data = DoctorLeave.objects.get(id=id1)
        d_data.delete()
        return redirect(leave_list)
    else:
        return redirect(home)


def patient_profile(request, id7):
    if "id" in request.session:
        did = request.session['id']
        d_data = Doctor.objects.get(pk=did)
        p_data = Patient.objects.get(pk=id7)
        h_appoint = HosAppointment.objects.filter(patient=id7, doctor=did)
        l_appoint = LabAppointment.objects.filter(patient=id7)
        context = {'p_data': p_data, 'd_data': d_data, 'h_appoint': h_appoint, 'l_appoint': l_appoint}
        a = d_data.doc_type
        if a == 'hospital':
            return render(request, "patient-profile.html", context)
        else:
            return render(request, "lab-patient-profile.html", context)
    else:
        return redirect(home)


def doc_book_lab_appointment(request, id13):
    if "id" in request.session:
        did = request.session['id']
        p_data = Patient.objects.get(pk=id13)
        d_data = Doctor.objects.get(id=did)
        ld_data = Doctor.objects.filter(doc_type='laboratory')
        context = {'d_data': d_data, 'ld_data': ld_data, 'p_data': p_data}
        return render(request, "doc-lab-search.html", context)
    else:
        return redirect(home)


def doc_side_lab_booking(request, id12, id13):
    if "id" in request.session:
        did = request.session['id']
        p_data = Patient.objects.get(id=id13)
        d_data = Doctor.objects.get(id=did)
        ld_data = Doctor.objects.get(id=id12)

        if request.method == 'POST':
            dt = request.POST.get('date')
            st = 'pending'

            t1 = d_data.slot1_start_time
            t2 = d_data.slot1_end_time
            t3 = d_data.slot2_start_time
            t4 = d_data.slot2_end_time
            ct = int(d_data.consult_time)

            lcount = DoctorLeave.objects.filter(doctor=id12, date=dt).count()
            if lcount > 0:
                bcount = LabAppointment.objects.filter(patient=id13, doctor=id12, date=dt, status=st).count()
                if bcount > 0:
                    messages.error(request, 'Your appointment on this date is already pending', extra_tags='error')
                else:
                    leave_data = DoctorLeave.objects.get(doctor=id12, date=dt)

                    l1 = leave_data.slot1_start_time
                    l2 = leave_data.slot1_end_time
                    l3 = leave_data.slot2_start_time
                    l4 = leave_data.slot2_end_time

                    if l1 is None and l2 is None:
                        r1t1 = str(t1)
                        r1t2 = str(t2)
                        r2t1 = str(t2)
                        r2t2 = str(t2)
                        s1 = time_slot(r1t1, r1t2, ct)
                        s2 = time_slot(r2t1, r2t2, ct)
                    else:
                        r1t1 = str(t1)
                        r1t2 = str(l1)
                        r2t1 = str(l2)
                        r2t2 = str(t2)
                        s1 = time_slot(r1t1, r1t2, ct)
                        s2 = time_slot(r2t1, r2t2, ct)

                    if l3 is None and l4 is None:
                        r3t1 = str(t3)
                        r3t2 = str(t4)
                        r4t1 = str(t4)
                        r4t2 = str(t4)
                        s3 = time_slot(r3t1, r3t2, ct)
                        s4 = time_slot(r4t1, r4t2, ct)
                    else:
                        r3t1 = str(t3)
                        r3t2 = str(l3)
                        r4t1 = str(l4)
                        r4t2 = str(t4)
                        s3 = time_slot(r3t1, r3t2, ct)
                        s4 = time_slot(r4t1, r4t2, ct)

                    array = s1 + s2 + s3 + s4

                    for i in array:
                        time1 = datetime.strptime(i, '%H:%M').time()
                        lab_count = LabAppointment.objects.filter(doctor=id12, date=dt, appointment_time=time1).count()

                        if lab_count == 0:
                            lget = LabAppointment(patient=p_data, doctor=ld_data, date=dt, appointment_time=time1, status=st)
                            lget.save()
                            messages.success(request, "Your appointment is booked successfully", extra_tags='book-success')
                            break

            else:
                bcount = LabAppointment.objects.filter(patient=id13, doctor=id12, date=dt, status=st).count()
                if bcount > 0:
                    messages.error(request, 'Your appointment on this date is already pending', extra_tags='error')
                else:
                    r1t1 = str(t1)
                    r1t2 = str(t2)
                    r2t1 = str(t3)
                    r2t2 = str(t4)

                    s1 = time_slot(r1t1, r1t2, ct)
                    s2 = time_slot(r2t1, r2t2, ct)

                    array = s1 + s2
                    for i in array:
                        time1 = datetime.strptime(i, '%H:%M').time()
                        lab_count = LabAppointment.objects.filter(doctor=id12, date=dt, appointment_time=time1).count()

                        if lab_count == 0:
                            lget = LabAppointment(patient=p_data, doctor=ld_data, date=dt, appointment_time=time1, status=st)
                            lget.save()
                            messages.success(request, "Your appointment is booked successfully", extra_tags='book-success')
                            break

        context = {'d_data': d_data, 'ld_data': ld_data, 'p_data': p_data}
        return render(request, "doc-side-lab-booking.html", context)
    else:
        return redirect(home)


def doc_logout(request):
    if "id" in request.session:
        del request.session['id']
        del request.session['name']
        del request.session['user_type']
        return redirect(login_doctor)
    else:
        return redirect(home)