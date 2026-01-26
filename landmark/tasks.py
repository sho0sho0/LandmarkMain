from celery import shared_task
from datetime import datetime
from .models import SelectedDiploma

@shared_task
def remove_expired_diplomas():
    now = datetime.now()
    expired_diplomas = SelectedDiploma.objects.filter(diploma__end_course__lt=now)
    for entry in expired_diplomas:
        entry.delete()
