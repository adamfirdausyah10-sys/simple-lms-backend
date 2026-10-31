from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from users.models import User
from catalog.models import Course, Lesson, Enrollment, Assignment, Submission

class Command(BaseCommand):
    help = "Membuat sample data LMS tanpa duplikasi"

    def handle(self, *args, **options):
        lecturer, _ = User.objects.get_or_create(
            username="suprayogi",
            defaults={"email": "suprayogi@example.test", "role": "LECTURER"},
        )
        student, _ = User.objects.get_or_create(
            username="fauzan",
            defaults={"email": "fauzan@example.test", "role": "STUDENT"},
        )
        for user in (lecturer, student):
            if not user.has_usable_password():
                continue
            # Akun simulasi tidak dipakai untuk login.
            user.set_unusable_password()
            user.save(update_fields=["password"])

        course, _ = Course.objects.get_or_create(
            code="PSS01",
            defaults={
                "title": "Pemrograman Sisi Server",
                "description": "Belajar backend development dengan Django.",
                "lecturer": lecturer,
            },
        )
        for order, title in enumerate((
            "Pengenalan Backend", "Pola Arsitektur Backend", "Containerisasi dengan Docker"
        ), start=1):
            Lesson.objects.get_or_create(
                course=course,
                order=order,
                defaults={"title": title, "content": f"Materi {title}"},
            )
        Enrollment.objects.get_or_create(student=student, course=course)
        for number, title in enumerate(("Tugas Django ORM", "Tugas REST API"), start=1):
            assignment, _ = Assignment.objects.get_or_create(
                course=course,
                title=title,
                defaults={
                    "description": title,
                    "deadline": timezone.now() + timedelta(days=number * 7),
                },
            )
            Submission.objects.get_or_create(
                assignment=assignment,
                student=student,
                defaults={"content": "Jawaban simulasi"},
            )
        self.stdout.write(self.style.SUCCESS("Sample data berhasil dibuat."))
