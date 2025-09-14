from logs.models import Log 
from pytz import timezone as pytzTimezone
from django.utils import timezone

def logError(reference, exception):
    Log.objects.create(
        reference=reference,
        exception=exception,
        created_at=timezone.now().astimezone(pytzTimezone("America/Sao_Paulo"))
    )
