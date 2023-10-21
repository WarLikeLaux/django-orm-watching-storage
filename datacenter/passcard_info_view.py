from datacenter.models import Passcard, Visit, format_duration
from django.shortcuts import render
from django.utils.timezone import localtime
from django.shortcuts import get_object_or_404


def passcard_info_view(request, passcode):
    passcard = get_object_or_404(Passcard, passcode=passcode)
    passcard_visits_details = []
    this_passcard_visits = Visit.objects.filter(passcard=passcard)
    for visit in this_passcard_visits:
        passcard_visits_details.append({
            'entered_at': localtime(visit.entered_at).strftime('%d-%m-%Y'),
            'duration': format_duration(visit.get_duration()),
            'is_strange': visit.is_long()
        })
    context = {
        'passcard': passcard,
        'this_passcard_visits': passcard_visits_details
    }
    return render(request, 'passcard_info.html', context)
