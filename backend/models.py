from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime

# Student Table
class Student(Base):
    __tablename__ = "students"

    student_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    year_level = Column(String, nullable=False)  # e.g., Year 1, Year 2

    grades = relationship("Grade", back_populates="student")

# Professor Table
class Professor(Base):
    __tablename__ = "professors"

    professor_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    department = Column(String, nullable=False)

# Lecture Table
class Lecture(Base):
    __tablename__ = "lectures"

    lecture_id = Column(Integer, primary_key=True, index=True)
    lecture_number = Column(Integer, nullable=False)
    published_date = Column(DateTime, default=datetime.datetime.utcnow)

# Material Table
class Material(Base):
    __tablename__ = "materials"

    material_id = Column(Integer, primary_key=True, index=True)
    material_type = Column(String, nullable=False)  # PDF, Video, etc.
    material_name = Column(String, nullable=False)
    subject = Column(String, nullable=False)

# Assessment Table
class Assessment(Base):
    __tablename__ = "assessments"

    assessment_id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, nullable=False)  # No FK, assuming subjects aren't a table
    name = Column(String, nullable=False)
    due_date = Column(DateTime, nullable=True)
    published_date = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, nullable=False)  # Open, Closed
    assessment_type = Column(String, nullable=False)  # Assignment, Quiz, Exam

    grades = relationship("Grade", back_populates="assessment")

# Grade Table
class Grade(Base):
    __tablename__ = "grades"

    grade_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.student_id"))
    assessment_id = Column(Integer, ForeignKey("assessments.assessment_id"))
    grade = Column(Integer, nullable=False)

    student = relationship("Student", back_populates="grades")
    assessment = relationship("Assessment", back_populates="grades")

# Subjects Table
class Subject(Base):
    __tablename__ = "subjects"

    subject_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    subject_name = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    semester = Column(Integer, nullable=False)
    credits = Column(Integer, nullable=False) 