from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from users.models import User
from catalog.models import Course

class Command(BaseCommand):
    help = "Buat 10.000 Course PERF tanpa duplikasi"

    def handle(self, *args, **options):
        lecturer = User.objects.filter(role="LECTURER").first()
        if lecturer is None:
            raise CommandError("Jalankan seed_demo dahulu agar ada Lecturer.")

        existing = set(Course.objects.filter(
            code__startswith="PERF"
        ).values_list("code", flat=True))
        rows = [
            Course(
                code=f"PERF{i:05d}",
                title=f"Performance Course {i}",
                lecturer=lecturer,
                is_active=(i % 5 != 0),
            )
            for i in range(10000)
            if f"PERF{i:05d}" not in existing
        ]
        with transaction.atomic():
            Course.objects.bulk_create(rows, batch_size=500)
        self.stdout.write(self.style.SUCCESS(
            f"Course baru: {len(rows)}; total Course: {Course.objects.count()}"
        ))
