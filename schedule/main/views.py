from django.shortcuts import render
from main.models import Specialization


def choice_of_specialization(request):
    specialists = Specialization.objects.filter(is_used=True)
    button_count = len(specialists)
    buttons_per_row = 3
    rows = []
    xxx = iter(specialists)

    for i in range(button_count // buttons_per_row):
        row = []
        for j in range(buttons_per_row):
            row.append(next(xxx))
        rows.append(row)

    row = []
    for i in range(button_count % buttons_per_row):
        row.append(next(xxx))
    rows.append(row)

    context = {
        'rows': rows,
    }

    return render(request, 'main/index.html', context)

def choice_of_doctor(request, spec_id):
    context = {
        'spec_id': spec_id,
        'specialization': Specialization.objects.get(pk=spec_id).title
    }

    return render(request, 'main/doctors.html', context)
