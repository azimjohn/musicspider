from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print("Started crawling from z1.fm")
        # the crawl
        print("Successfully finished crawling")
