from django.core.management.base import BaseCommand
from home.models import Invitation 
from django.utils import timezone

class Command(BaseCommand):
    help = "Expire old invitations that are still pending."

    def handle(self, *args, **kwargs):
        # Filter invitations with expiration date in the past and status still pending
        expired = Invitation.objects.filter(expiration_date__lt=timezone.now(), status='Pending')
        count = expired.update(status='Expired')  # Bulk update
        self.stdout.write(self.style.SUCCESS(f"{count} invitation(s) expired."))
