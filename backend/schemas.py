from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Student Schema
class StudentBase(BaseModel):
    name: str
    email: str
    year: str
    track: Optional[str] = None
    password: Optional[str] = None
    subject_list: Optional[list[str]] = []  # Include subject_list in the base schema

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    student_id: str

    class Config:
        from_attributes = True

class StudentResponse(StudentBase):
    student_id: str

    class Config:
        from_attributes = True

# Professor Schema
class ProfessorBase(BaseModel):
    name: str
    department: str
    subject_list: Optional[list[str]] = []  # Updated to store list of subject IDs (Array-like structure)
    email: str
    password: Optional[str] = None

class ProfessorCreate(ProfessorBase):
    pass

class Professor(ProfessorBase):
    professor_id: str

    class Config:
        from_attributes = True

class ProfessorResponse(ProfessorBase):
    professor_id: str

    class Config:
        from_attributes = True


# Lecture Schema
class LectureBase(BaseModel):
    subject_id: str
    name: str
    date: str
    time: str
    file_path: str

class LectureCreate(LectureBase):
    pass

class Lecture(LectureBase):
    lecture_id: str

    class Config:
        from_attributes = True

class LectureResponse(LectureBase):
    lecture_id: str

    class Config:
        from_attributes = True

# Material Schema
class MaterialBase(BaseModel):
    subject_id: str
    name: str
    file_path: str

class MaterialCreate(MaterialBase):
    pass

class Material(MaterialBase):
    material_id: str

    class Config:
        from_attributes = True

class MaterialResponse(MaterialBase):
    material_id: str

    class Config:
        from_attributes = True

# Assessment Schema
class AssessmentBase(BaseModel):
    subject_id: str
    name: str
    due_date: Optional[datetime] = None
    published_date: datetime = datetime.utcnow()
    status: str
    assessment_type: str
    file_path: str

class AssessmentCreate(AssessmentBase):
    pass

class Assessment(AssessmentBase):
    assessment_id: str

    class Config:
        from_attributes = True

class AssessmentResponse(AssessmentBase):
    assessment_id: str

    class Config:
        from_attributes = True

# Grade Schema
class GradeBase(BaseModel):
    student_id: str
    assessment_id: str
    subject_id: str
    score: Optional[int] = None
    grade: Optional[str] = None

class GradeCreate(GradeBase):
    pass

class Grade(GradeBase):
    grade_id: str

    class Config:
        from_attributes = True

class GradeResponse(GradeBase):
    grade_id: str

    class Config:
        from_attributes = True

# Subject Schema
class SubjectBase(BaseModel):
    subject_name: str
    year: int
    semester: int
    track: Optional[str] = None
    credits: int
    student_list: Optional[list[str]] = []  # Optional list of student IDs for each subject

class SubjectCreate(SubjectBase):
    pass

class Subject(SubjectBase):
    subject_id: str

    class Config:
        from_attributes = True

class SubjectResponse(SubjectBase):
    subject_id: str
    student_list: List[int]

    class Config:
        from_attributes = True

# Submission Schema
class SubmissionBase(BaseModel):
    assessment_id: str
    student_id: str
    file_path: str
    submitted_time: datetime = datetime.utcnow()
    last_modified: datetime = datetime.utcnow()
    status: str

class SubmissionCreate(SubmissionBase):
    pass

class Submission(SubmissionBase):
    submission_id: str

    class Config:
        from_attributes = True

class SubmissionResponse(SubmissionBase):
    submission_id: str

    class Config:
        from_attributes = True

class UserSessionBase(BaseModel):
    session_id:str
    user_id: str
    role: str
    subject_id: str

class UserSessionCreate(SubmissionBase):
    pass

class UserSession(SubmissionBase):
    session_id:str

    class Config:
        from_attributes = True

class UserSessionCreateResponse(SubmissionBase):
    session_id:str

    class Config:
        from_attributes = True