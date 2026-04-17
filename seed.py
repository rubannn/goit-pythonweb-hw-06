from faker import Faker
import random
from datetime import datetime, timedelta

from conf.db import SessionLocal
from models.models import Student, Group, Teacher, Subject, Grade

fake = Faker("uk_UA")
session = SessionLocal()

GROUP_COUNT = 3
TEACHER_COUNT = 5
SUBJECT_COUNT = 6
STUDENT_COUNT = 50


def seed():
    # Groups
    groups = [Group(name=f"Група-{i}") for i in range(1, GROUP_COUNT + 1)]
    session.add_all(groups)

    # Teachers
    teachers = [Teacher(name=fake.name()) for _ in range(TEACHER_COUNT)]
    session.add_all(teachers)

    # Subjects
    subjects_list = [
        "Математика",
        "Фізика",
        "Хімія",
        "Біологія",
        "Історія",
        "Географія",
        "Програмування",
    ]
    subjects = []
    for i in range(SUBJECT_COUNT):
        subject = Subject(
            name=random.choice(subjects_list), teacher=random.choice(teachers)
        )
        subjects.append(subject)
    session.add_all(subjects)

    # Students
    students = []
    for _ in range(STUDENT_COUNT):
        student = Student(name=fake.name(), group=random.choice(groups))
        students.append(student)
    session.add_all(students)

    session.commit()

    # Grades
    for student in students:
        for _ in range(random.randint(10, 20)):
            grade = Grade(
                student=student,
                subject=random.choice(subjects),
                grade=int(random.uniform(60, 100)),
                date_received=datetime.now() - timedelta(days=random.randint(1, 365)),
            )
            session.add(grade)

    session.commit()


if __name__ == "__main__":
    seed()
