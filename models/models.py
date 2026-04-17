from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime

from conf.db import Base


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    students = relationship("Student", back_populates="group")

    def __repr__(self):
        return f"Group(id={self.id}, name='{self.name}')"


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"))

    group = relationship("Group", back_populates="students")
    grades = relationship("Grade", back_populates="student")

    def __repr__(self):
        return f"Student(id={self.id}, name='{self.name}', group_id={self.group_id})"


class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    subjects = relationship("Subject", back_populates="teacher")

    def __repr__(self):
        return f"Teacher(id={self.id}, name='{self.name}')"


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))

    teacher = relationship("Teacher", back_populates="subjects")
    grades = relationship("Grade", back_populates="subject")

    def __repr__(self):
        return f"Subject(id={self.id}, name='{self.name}', teacher_id={self.teacher_id})"


class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    grade = Column(Integer, nullable=False)
    date_received = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student", back_populates="grades")
    subject = relationship("Subject", back_populates="grades")

    def __repr__(self):
        return (
            f"Grade(id={self.id}, student_id={self.student_id}, "
            f"subject_id={self.subject_id}, grade={self.grade}, "
            f"date={self.date_received})"
        )
