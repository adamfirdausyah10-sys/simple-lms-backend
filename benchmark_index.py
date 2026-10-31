
import time

from catalog.models import Course

queryset = Course.objects.filter(
    is_active=True,
    title="Performance Course 5001"
)

print("=== EXPLAIN ===")
print(queryset.explain())

start = time.perf_counter()

result = list(queryset)

elapsed = time.perf_counter() - start

print("Jumlah hasil:", len(result))
print("Waktu eksekusi:", round(elapsed, 6), "detik")
