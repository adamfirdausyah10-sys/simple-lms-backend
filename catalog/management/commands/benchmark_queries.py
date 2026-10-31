import time
from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from django.test.utils import CaptureQueriesContext
from catalog.models import Course, Enrollment

class Command(BaseCommand):
    help = "Ukur BEFORE/AFTER N+1 pada Course+Lecturer dan Course+Lesson"

    def measure(self, name, queryset, relation):
        start = time.perf_counter()
        with CaptureQueriesContext(connection) as ctx:
            rows = []
            for course in queryset:
                if relation == "lecturer":
                    rows.append((course.title, course.lecturer.username))
                else:
                    rows.append([lesson.title for lesson in course.lessons.all()])
        elapsed = (time.perf_counter() - start) * 1000
        self.stdout.write(
            f"{name}: course={len(rows)}, query={len(ctx.captured_queries)}, "
            f"time_ms={elapsed:.3f}"
        )

    def handle(self, *args, **options):
        if Course.objects.filter(code__startswith="PERF").count() < 100:
            raise CommandError("Generate dataset performa terlebih dahulu")
        basic = Course.objects.filter(code__startswith="PERF").order_by("code")
        self.measure("Lecturer BEFORE", basic[:100], "lecturer")
        self.measure("Lecturer AFTER", basic.select_related("lecturer")[:100], "lecturer")
        self.measure("Lesson BEFORE", basic[:50], "lessons")
        self.measure("Lesson AFTER", basic.prefetch_related("lessons")[:50], "lessons")
