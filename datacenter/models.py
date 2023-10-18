from django.db import models
from django.utils.timezone import localtime, now


def format_duration(duration):
    days_from = f"{int(duration // 86400):03d}"
    hours_from = f"{int((duration % 86400) // 3600):02d}"
    minutes_from = f"{int((duration % 3600) // 60):02d}"
    return f"{days_from}:{hours_from}:{minutes_from}".replace("000:", "")


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )

    def get_duration(self):
        reference_time = self.leaved_at or now()
        visit_duration = localtime(reference_time) - localtime(self.entered_at)
        return visit_duration.total_seconds()

    def is_long(self, minutes=60):
        return self.get_duration() > minutes * 60
