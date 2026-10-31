from datetime import timedelta
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone
from users.models import User
from catalog.models import Course, Enrollment, Lesson, Assignment, Submission

class Command(BaseCommand):
    help = "Membuat relasi LMS (55 user, 100 course, 1000 enrollment, 500 lesson, 200 assignment, 1000 submission)"

    def handle(self, *args, **options):
        courses = list(Course.objects.filter(
            code__startswith="PERF"
        ).order_by("code")[:100])
        if len(courses) < 100:
            raise CommandError("Jalankan generate_performance_data dahulu.")

        with transaction.atomic():
            lecturers, students = [], []
            for i in range(1, 6):
                user, created = User.objects.get_or_create(
                    username=f"perf_lecturer_{i:02d}",
                    defaults={"role": "LECTURER", "is_active": True},
                )
                if user.role != "LECTURER":
                    raise CommandError(f"Role {user.username} bukan LECTURER")
                if created:
                    user.set_unusable_password()
                    user.save(update_fields=["password"])
                lecturers.append(user)

            for i in range(1, 51):
                user, created = User.objects.get_or_create(
                    username=f"perf_student_{i:03d}",
                    defaults={"role": "STUDENT", "is_active": True},
                )
                if user.role != "STUDENT":
                    raise CommandError(f"Role {user.username} bukan STUDENT")
                if created:
                    user.set_unusable_password()
                    user.save(update_fields=["password"])
                students.append(user)

            enrollment_existing = set(Enrollment.objects.filter(
                course__in=courses
            ).values_list("course_id", "student_id"))
            enrollments = []
            for index, course in enumerate(courses):
                for offset in range(10):
                    student = students[(index * 10 + offset) % len(students)]
                    if (course.pk, student.pk) not in enrollment_existing:
                        enrollments.append(Enrollment(course=course, student=student))
            Enrollment.objects.bulk_create(enrollments, batch_size=500)

            lesson_existing = set(Lesson.objects.filter(
                course__in=courses
            ).values_list("course_id", "order"))
            lessons = [
                Lesson(course=course, title=f"Materi {order}",
                       content=f"Materi simulasi {order} untuk {course.code}", order=order)
                for course in courses for order in range(1, 6)
                if (course.pk, order) not in lesson_existing
            ]
            Lesson.objects.bulk_create(lessons, batch_size=500)

            assignment_existing = set(Assignment.objects.filter(
                course__in=courses
            ).values_list("course_id", "title"))
            assignments_to_create = [
                Assignment(
                    course=course,
                    title=f"PERF Tugas {number}",
                    description=f"Tugas simulasi untuk {course.code}",
                    deadline=timezone.now() + timedelta(days=14),
                )
                for course in courses for number in range(1, 3)
                if (course.pk, f"PERF Tugas {number}") not in assignment_existing
            ]
            Assignment.objects.bulk_create(assignments_to_create, batch_size=500)

            assignments = list(Assignment.objects.filter(
                course__in=courses, title__in=["PERF Tugas 1", "PERF Tugas 2"]
            ))
            enrollment_map = {}
            for course_id, student_id in Enrollment.objects.filter(
                course__in=courses, student__in=students
            ).values_list("course_id", "student_id"):
                enrollment_map.setdefault(course_id, []).append(student_id)
            submissions_existing = set(Submission.objects.filter(
                assignment__in=assignments
            ).values_list("assignment_id", "student_id"))
            submissions = []
            for assignment in assignments:
                for student_id in sorted(enrollment_map.get(assignment.course_id, []))[:5]:
                    if (assignment.pk, student_id) not in submissions_existing:
                        submissions.append(Submission(
                            assignment=assignment,
                            student_id=student_id,
                            content="Jawaban simulasi untuk pengujian performa LMS.",
                        ))
            Submission.objects.bulk_create(submissions, batch_size=500)

        for label, count in (
            ("Lecturer simulasi", len(lecturers)),
            ("Student simulasi", len(students)),
            ("Course digunakan", len(courses)),
            ("Enrollment baru", len(enrollments)),
            ("Lesson baru", len(lessons)),
            ("Assignment baru", len(assignments_to_create)),
            ("Submission baru", len(submissions)),
        ):
            self.stdout.write(f"{label}: {count}")
