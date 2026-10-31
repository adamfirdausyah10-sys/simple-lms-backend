
import time
from django.db import connection
from django.test.utils import CaptureQueriesContext
from catalog.models import Course


def benchmark(queryset):
    start = time.perf_counter()

    with CaptureQueriesContext(connection) as ctx:
        result = [
            (course.title, course.lecturer.username)
            for course in queryset
        ]

    elapsed = time.perf_counter() - start

    return len(result), len(ctx.captured_queries), elapsed


courses = Course.objects.filter(
    code__startswith="PERF"
).order_by("code")

before = benchmark(courses[:100])
after = benchmark(courses.select_related("lecturer")[:100])

print("BEFORE:", before)
print("AFTER :", after)
