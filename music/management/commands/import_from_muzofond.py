from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print("Started importing from CSV file")
        # the import
        print("Successfully finished impoting")



