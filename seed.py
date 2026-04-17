from faker import Faker
import random
from datetime import datetime, timedelta

from conf.db import SessionLocal
from models.models import Student, Group, Teacher, Subject, Grade

fake = Faker()
session = SessionLocal()

GROUP_COUNT = 5
TEACHER_COUNT = 5
SUBJECT_COUNT = 7
STUDENT_COUNT = 35

def seed():
    # Groups
    groups = [Group(name=f"Group-{i}") for i in range(1, GROUP_COUNT + 1)]
    session.add_all(groups)

    # Teachers
    teachers = [Teacher(name=fake.name()) for _ in range(TEACHER_COUNT)]
    session.add_all(teachers)

    # Subjects
    subjects = []
    for i in range(SUBJECT_COUNT):
        subject = Subject(
            name=f"Subject-{i}",
            teacher=random.choice(teachers)
        )
        subjects.append(subject)
    session.add_all(subjects)

    # Students
    students = []
    for _ in range(SUBJECT_COUNT):
        student = Student(
            name=fake.name(),
            group=random.choice(groups)
        )
        students.append(student)
    session.add_all(students)

    session.commit()

    # Grades
    for student in students:
        for _ in range(random.randint(10, 20)):
            grade = Grade(
                student=student,
                subject=random.choice(subjects),
                grade=random.uniform(60, 100),
                date_received=datetime.now() - timedelta(days=random.randint(1, 365))
            )
            session.add(grade)

    session.commit()


if __name__ == "__main__":
    seed()
