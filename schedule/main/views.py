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


def choice_of_doctor(request, spec_slug):
    doctors = Doctor.objects.filter(is_active=True, specialization__slug=spec_slug)
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
        'spec_slug': spec_slug,
        'specialization': Specialization.objects.get(slug=spec_slug).title
    }

    return render(request, 'main/doctors.html', context)


def choice_of_time(request, doct_slug):
    return HttpResponse(f"Здесь будет календарь для врача {Doctor.objects.get(slug=doct_slug)}")
