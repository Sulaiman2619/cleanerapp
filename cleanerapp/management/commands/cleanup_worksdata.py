from django.core.management.base import BaseCommand
from django.utils import timezone
from cleanerapp.models import WorksData

class Command(BaseCommand):
    help = 'Deletes WorksData older than 2 months'

    def handle(self, *args, **kwargs):
        two_months_ago = timezone.now() - timezone.timedelta(days=60)
        WorksData.objects.filter(date__lt=two_months_ago).delete()
        self.stdout.write(self.style.SUCCESS('WorksData older than 2 months have been deleted.'))