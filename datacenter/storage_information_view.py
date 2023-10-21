from datacenter.models import Visit, format_duration
from django.shortcuts import render
from django.utils.timezone import localtime, now


def storage_information_view(request):
    non_closed_visits_details = []
    non_closed_visits = Visit.objects.filter(leaved_at__isnull=True)
    for visit in non_closed_visits:
        non_closed_visits_details.append({
            'who_entered': visit.passcard.owner_name,
            'entered_at': localtime(visit.entered_at),
            'duration': format_duration(visit.get_duration()),
            'is_strange': visit.is_long()
        })
    context = {
        'non_closed_visits': non_closed_visits_details,
    }
    return render(request, 'storage_information.html', context)
