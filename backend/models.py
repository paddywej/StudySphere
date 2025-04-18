from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import ARRAY 
from sqlalchemy.orm import relationship, validates
from .database import Base
import datetime


# Student Table 
class Student(Base):
    __tablename__ = "students"

    student_id = Column(String, primary_key=True, index=True)  # Changed to String
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)  # Email added
    year = Column(String, nullable=False)  
    track = Column(String, nullable=True) 
    password = Column(String, nullable=True)  # before sign up null
    subject_list = Column(ARRAY(String), nullable=True)  # Changed to PostgreSQL ARRAY type

    grades = relationship("Grade", back_populates="student")
    submissions = relationship("Submission", back_populates="student") 

# Professor Table
class Professor(Base):
    __tablename__ = "professors"

    professor_id = Column(String, primary_key=True, index=True)  # Changed to String
    name = Column(String, nullable=False)
    department = Column(String, nullable=False)
    subject_list = Column(ARRAY(String), nullable=False)  # Changed to PostgreSQL ARRAY type
    email = Column(String, unique=True, nullable=False)  # Email added
    password = Column(String, nullable=True)  # before sign up null

# # Lecture Table
class Lecture(Base):
    __tablename__ = 'lectures'

    lecture_id = Column(String, primary_key=True)
    subject_id = Column(String, ForeignKey("subjects.subject_id"), nullable=False)
    name = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    time = Column(String, nullable=False)
    file_path = Column(String, nullable=False)

    subject = relationship("Subject", back_populates="lectures")

    @validates('lecture_id')
    def validate_lecture_id(self, key, value):
        """Ensure the lecture_id is a valid UUID format."""
        return value

# Material Table
class Material(Base):
    __tablename__ = "materials"

    material_id = Column(String, primary_key=True, index=True)  # Changed to String
    subject_id = Column(String, ForeignKey("subjects.subject_id"), nullable=False)  # Foreign key to Subject
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    file_path = Column(String, nullable=False)  # Path to the material file
    
    # Relationship with the Subject table
    subject = relationship("Subject", back_populates="materials")

# Assessment Table
class Assessment(Base):
    __tablename__ = "assessments"

    assessment_id = Column(String, primary_key=True, index=True)  # Changed to String
    subject_id = Column(String, ForeignKey("subjects.subject_id"), nullable=False)
    name = Column(String, nullable=False)
    due_date = Column(DateTime, nullable=True)
    published_date = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, nullable=False)  # Open, Closed
    assessment_type = Column(String, nullable=False)  # Assignment, Quiz, Exam
    file_path = Column(String, nullable=False)  # Path to the submitted file

    grades = relationship("Grade", back_populates="assessment")
    submissions = relationship("Submission", back_populates="assessment") 

# Grade Table
class Grade(Base):
    __tablename__ = "grades"

    grade_id = Column(String, primary_key=True, index=True)  # Changed to String
    student_id = Column(String, ForeignKey("students.student_id", ondelete="CASCADE"), nullable=False)  # Changed to String
    assessment_id = Column(String, ForeignKey("assessments.assessment_id", ondelete="CASCADE"), nullable=False)  # Changed to String
    subject_id = Column(String, ForeignKey("subjects.subject_id", ondelete="CASCADE"), nullable=False)  # Link to subject
    score = Column(Integer, nullable=True)  # Numerical grade (could be NULL if not graded yet)
    grade = Column(String, nullable=True)  # Grade in letter form, e.g., A, B, C

    student = relationship("Student", back_populates="grades")
    assessment = relationship("Assessment", back_populates="grades")
    subject = relationship("Subject", back_populates="grades")

# Subject Table
class Subject(Base):
    __tablename__ = "subjects"

    subject_id = Column(String, primary_key=True, index=True)  # Changed to String
    subject_name = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    semester = Column(Integer, nullable=False)
    track = Column(String, nullable=True)
    credits = Column(Integer, nullable=False)
    student_list = Column(ARRAY(String), nullable=True)  # Added array of student IDs

    materials = relationship("Material", back_populates="subject", cascade="all, delete")
    lectures = relationship("Lecture", back_populates="subject", cascade="all, delete")
    grades = relationship("Grade", back_populates="subject", cascade="all, delete")

# Submission Table
class Submission(Base):
    __tablename__ = "submissions"

    submission_id = Column(String, primary_key=True, index=True)  # Changed to String
    assessment_id = Column(String, ForeignKey("assessments.assessment_id", ondelete="CASCADE"), nullable=False)  # Link to the assessment
    student_id = Column(String, ForeignKey("students.student_id", ondelete="CASCADE"), nullable=False)  # Link to the student
    file_path = Column(String, nullable=False)  # Path to the submitted file
    submitted_time = Column(DateTime, default=datetime.datetime.utcnow)  # When the file was submitted
    last_modified = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)  # When the file was last modified
    status = Column(String, nullable=False)  # "Submitted" or "Late"
    
    # Relationship
    assessment = relationship("Assessment", back_populates="submissions")  # Link to the Assessment table
    student = relationship("Student", back_populates="submissions")  # Link to the Student table

class UserSession(Base):
    __tablename__ = "user_sessions"
    
    session_id = Column(String, primary_key=True, index=True)  # Unique user ID
    user_id = Column(String, nullable=False) 
    role = Column(String, nullable=False)  # User's role (e.g., 'admin', 'student', etc.)
    subject_id = Column(String, nullable=True)  # Subject ID that the user is associated with
    