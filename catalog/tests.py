from django.db import IntegrityError, transaction
from django.test import TestCase
from catalog.models import Course, Lesson
from users.models import User

class CourseTestCase(TestCase):
    def setUp(self):
        self.lecturer = User.objects.create_user(
            username="testlecturer", password="test12345", role="LECTURER"
        )

    def test_course_created(self):
        course = Course.objects.create(
            code="TEST01", title="Test Course", lecturer=self.lecturer
        )
        self.assertEqual(course.code, "TEST01")

    def test_course_code_unique(self):
        Course.objects.create(code="TEST01", title="Pertama", lecturer=self.lecturer)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Course.objects.create(
                    code="TEST01", title="Kedua", lecturer=self.lecturer
                )

    def test_lesson_relationship(self):
        course = Course.objects.create(
            code="TEST02", title="Django", lecturer=self.lecturer
        )
        lesson = Lesson.objects.create(
            course=course, title="Pengenalan", content="Materi", order=1
        )
        self.assertEqual(lesson.course, course)
        self.assertEqual(course.lessons.count(), 1)
