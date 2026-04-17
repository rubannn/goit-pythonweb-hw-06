import random

from sqlalchemy import func, desc
from conf.db import SessionLocal
from models.models import Student, Grade, Subject, Group, Teacher


session = SessionLocal()

# 1
def select_1():
    result = session.query(
        Student.name,
        func.avg(Grade.grade).label("avg_grade")
    ).join(Grade).group_by(Student.id).order_by(desc("avg_grade")).limit(5).all()

    for student in result:
        print(f"  {student.name}: {student.avg_grade:.3f}")
    print()


# 2
def select_2(subject_id):
    result = (
        session.query(
            Student,
            func.avg(Grade.grade).label("avg_grade")
        )
        .join(Grade)
        .filter(Grade.subject_id == subject_id)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .first()
    )

    if result:
        student, avg_grade = result
        print(f"Top student: {student.name}, Avg grade: {avg_grade:.3f}\n")
    else:
        print("No grades found for this subject.")


# 3
def select_3(subject_id):
    result = (
        session.query(
            Group.name,
            func.avg(Grade.grade).label("avg_grade")
        )
        .join(Group.students)        # Group -> Student
        .join(Student.grades)        # Student -> Grade
        .filter(Grade.subject_id == subject_id)
        .group_by(Group.id)
        .order_by(Group.name)
        .all()
    )
    if result:
        for group in result:
            print(f"  Група {group.name}: {group.avg_grade:.3f}")
        print()
    else:
        print("No grades found for this subject.")


# 4
def select_4():
    result = session.query(func.avg(Grade.grade)).scalar()
    print(f"\t{result:.3f}\n")


# 5
def select_5(teacher_id):
    result = session.query(Subject.name).filter(Subject.teacher_id == teacher_id).all()
    if result:
        for t in result:
            print(f"  {t.name}")
        print()


# 6
def select_6(group_id):
    result = session.query(Student.name).filter(Student.group_id == group_id).all()
    for i, student in enumerate(result, start=1):
        print(f"  {i:02d}. {student.name}")
    print()


# 7
def select_7(group_id, subject_id):
    result = (
        session.query(
            Student.name,
            func.array_agg(Grade.grade).label("grades")
        )
        .join(Student.grades)
        .filter(
            Student.group_id == group_id,
            Grade.subject_id == subject_id
        )
        .group_by(Student.id, Student.name)
        .order_by(Student.name)
        .all()
    )

    for i, row in enumerate(result, start=1):
        print(f" {i:02d}. {row.name}: {row.grades}")
    print()

# 8
def select_8(teacher_id):
    result = session.query(func.avg(Grade.grade))\
        .join(Subject)\
        .filter(Subject.teacher_id == teacher_id).scalar()
    if not result:
        result = 0.0
    print(f"  {result:.3f}\n")

# 9
def select_9(student_id):
    if student_id:
        result = (
            session.query(Subject.name)
            .join(Student.grades)
            .join(Grade.subject)
            .filter(Student.id == student_id)
            .distinct()
            .all()
        )
        print(f"\t{', '.join([row.name for row in result])}")
        print()
    else:
        print('Список студентів порожній...\n')

# 10
def select_10(student_id, teacher_id):
    result = session.query(Subject.name)\
        .join(Grade)\
        .join(Teacher)\
        .filter(
            Grade.student_id == student_id,
            Teacher.id == teacher_id
        ).distinct().all()
    if result:
        print(f"\t{', '.join([row.name for row in result])}")
    else:
        print("\tНе знайдено курси...")

#11
def select_11(teacher_id: int, student_id: int):
    avg_grade = (
        session.query(func.avg(Grade.grade))
        .join(Subject, Grade.subject_id == Subject.id)
        .join(Teacher, Subject.teacher_id == Teacher.id)
        .filter(
            Teacher.id == teacher_id,
            Grade.student_id == student_id
        )
        .scalar()
    )
    if not avg_grade:
        avg_grade = 0.0
    print(f"\t{avg_grade:.3f}\n")

def select_12(group_id: int, subject_id: int):
    subquery = (
        session.query(func.max(Grade.date_received))
        .join(Student, Grade.student_id == Student.id)
        .filter(
            Student.group_id == group_id,
            Grade.subject_id == subject_id
        )
        .scalar_subquery()
    )

    results = (
        session.query(Student.name, Grade.grade, Grade.date_received.label("date"))
        .join(Grade, Student.id == Grade.student_id)
        .filter(
            Student.group_id == group_id,
            Grade.subject_id == subject_id,
            Grade.date_received == subquery
        )
        .all()
    )
    if results:
        for row in results:
            formatted_date = row.date.strftime("%d/%m/%Y %H:%M")
            print(f"\t{row.name} - {row.grade} [{formatted_date}]")
    else:
        print("\tОцінки не знадено...")


# Функція для тестування всіх запитів
def test_all_selects():

    students = session.query(Student).all()
    subjects = session.query(Subject).all()
    teachers = session.query(Teacher).all()
    groups = session.query(Group).all()

    """
    Тестування всіх функцій select
    """
    print("=== Тестування всіх запитів ===\n")

    print("1. 5 студентів із найбільшим середнім балом:")
    select_1()


    random_subject = random.choice(subjects)
    print(f"2. Студент із найвищим середнім балом з [{random_subject.name}]:")
    select_2(random_subject.id)


    random_subject = random.choice(subjects)
    print(f"3. Середній бал у групах з [{random_subject.name}]:")
    select_3(random_subject.id)


    print("4. Середній бал на потоці:")
    select_4()

    random_teacher = random.choice(teachers)
    print(f"5. Курси викладача [{random_teacher.name}]:")
    select_5(random_teacher.id)

    random_group = random.choice(groups)
    print(f"6. Студенти групи [{random_group.name}]:")
    select_6(random_group.id)

    print(f"7. Оцінки групи [{random_group.name}] з [{random_subject.name}]:")
    select_7(random_group.id, random_subject.id)

    print(f"8. Середній бал, який ставить [{random_teacher.name}]:")
    select_8(random_teacher.id)

    random_student = random.choice(students)
    print(f"9. Курси студента [{random_student.name}]:")
    select_9(random_student.id)

    print(f"10. Курси студента [{random_student.name}] від викладача [{random_teacher.name}]:")
    select_10(random_student.id, random_teacher.id)

    print(f"\nДОДАТКОВІ ЗАПИТИ")
    print(f"Середній бал, який викладач [{random_teacher.name}] ставить студенту [{random_student.name}]")
    select_11(random_teacher.id, random_student.id)

    print(f"Оцінки студентів у групі [{random_group.name}] з предмета [{random_subject.name}] на останньому занятті.")
    select_12(random_group.id, random_subject.id)

if __name__ == "__main__":
    test_all_selects()
