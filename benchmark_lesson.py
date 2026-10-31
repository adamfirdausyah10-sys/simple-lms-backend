
import time

from django.db import connection
from django.test.utils import CaptureQueriesContext
from catalog.models import Course


def benchmark(queryset):
    start = time.perf_counter()

    with CaptureQueriesContext(connection) as ctx:
        result = [
            (course.code, [lesson.title for lesson in course.lessons.all()])
            for course in queryset
        ]

    elapsed = time.perf_counter() - start

    return len(result), len(ctx.captured_queries), elapsed


courses = Course.objects.filter(
    code__startswith="PERF"
).order_by("code")

before = benchmark(courses[:50])
after = benchmark(courses.prefetch_related("lessons")[:50])

print("BEFORE:", before)
print("AFTER :", after)
