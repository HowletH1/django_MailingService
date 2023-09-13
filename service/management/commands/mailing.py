from django.core.management import BaseCommand
from service.services import check_mailing_time


class Command(BaseCommand):
    def handle(self, *args, **options):
        check_mailing_time()
