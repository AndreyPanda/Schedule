from django.shortcuts import render
from main.models import Specialization, Doctor
from django.http import HttpResponse


def choice_of_specialization(request):
    specialists = Specialization.objects.filter(is_used=True, doctors_specialization__isnull=False).distinct()
    button_count = len(specialists)
    buttons_per_row = 3
    rows = []
    spec_titles = iter(specialists)

    for i in range(button_count // buttons_per_row):
        row = []
        for j in range(buttons_per_row):
            row.append(next(spec_titles))
        rows.append(row)

    row = []
    for i in range(button_count % buttons_per_row):
        row.append(next(spec_titles))
    rows.append(row)

    context = {
        'rows': rows,
    }

    return render(request, 'main/index.html', context)


def choice_of_doctor(request, spec_id):
    doctors = Doctor.objects.filter(is_active=True, specialization=spec_id)
    button_count = len(doctors)
    buttons_per_row = 3
    rows = []
    doctor_titles = iter(doctors)

    for i in range(button_count // buttons_per_row):
        row = []
        for j in range(buttons_per_row):
            row.append(next(doctor_titles))
        rows.append(row)

    row = []
    for i in range(button_count % buttons_per_row):
        row.append(next(doctor_titles))
    rows.append(row)

    context = {
        'rows': rows,
        'spec_id': spec_id,
        'specialization': Specialization.objects.get(pk=spec_id).title
    }

    return render(request, 'main/doctors.html', context)


def choice_of_time(request, doct_id):
    return HttpResponse(f"Здесь будет календарь для врача {Doctor.objects.get(pk=doct_id)}")
