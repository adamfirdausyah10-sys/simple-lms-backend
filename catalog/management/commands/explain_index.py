from django.core.management.base import BaseCommand
from catalog.models import Course

class Command(BaseCommand):
    help = "EXPLAIN untuk filter (is_active, title); jalankan sebelum dan sesudah menambah index"

    def handle(self, *args, **options):
        queryset = Course.objects.filter(
            is_active=True, title="Performance Course 5001"
        )
        self.stdout.write(queryset.explain(analyze=True, buffers=True))
