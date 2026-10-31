from catalog.models import (
    Course, Lesson, Enrollment,
    Assignment, Submission
)

# 1. Semua Course beserta kode dan judul
print("\n=== 1. SEMUA COURSE ===")

courses = Course.objects.all()

print("Total Course:", courses.count())

for course in courses:
    print(course.code, "-", course.title)

# Ambil satu Course yang memiliki relasi simulasi
course = Course.objects.get(code="PERF00001")

# 2. Course yang diampu seorang dosen
print("\n=== 2. COURSE DOSEN ===")
for item in Course.objects.filter(
    lecturer=course.lecturer
)[:10]:
    print(item.code, item.title)

# 3. Semua Lesson milik satu Course
print("\n=== 3. LESSON COURSE ===")
for lesson in Lesson.objects.filter(course=course):
    print(lesson.title)

# 4. Jumlah mahasiswa dalam Course
print("\n=== 4. JUMLAH MAHASISWA ===")
print(
    Enrollment.objects.filter(course=course).count()
)

# 5. Assignment milik Course
print("\n=== 5. ASSIGNMENT COURSE ===")
for assignment in Assignment.objects.filter(course=course):
    print(assignment.title)

# 6. Submission milik suatu Assignment
print("\n=== 6. SUBMISSION ASSIGNMENT ===")
assignment = Assignment.objects.filter(course=course).first()

if assignment:
    for submission in Submission.objects.filter(
        assignment=assignment
    ):
        print(
            submission.student.username,
            submission.assignment.title
        )
