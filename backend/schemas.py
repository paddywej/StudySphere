from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Student Base Schema
class StudentBase(BaseModel):
    name: str
    email: str
    year_level: str
    track: str | None = None  # track is nullable, only applicable for years 3 and 4

# Schema for creating a student (input data)
class StudentCreate(StudentBase):
    pass

# Schema for responding with a student's data (includes student_id)
class StudentResponse(StudentBase):
    student_id: int

    class Config:
        from_attributes = True  # Tells Pydantic to support the ORM models' attributes


# Professor Schema
class ProfessorBase(BaseModel):
    name: str
    username: str
    department: str

class ProfessorCreate(ProfessorBase):
    pass

class ProfessorResponse(ProfessorBase):
    professor_id: int
    class Config:
        from_attributes = True

# Assessment Schema
class AssessmentBase(BaseModel):
    subject_id: int
    name: str
    due_date: Optional[datetime] = None
    published_date: datetime
    status: str
    assessment_type: str

class AssessmentCreate(AssessmentBase):
    pass

class AssessmentResponse(AssessmentBase):
    assessment_id: int
    class Config:
        from_attributes = True

# Grade Schema
class GradeBase(BaseModel):
    student_id: int
    assessment_id: int
    grade: int

class GradeCreate(GradeBase):
    pass

class GradeResponse(GradeBase):
    grade_id: int
    class Config:
        from_attributes = True

# Subject Base Schema
class SubjectBase(BaseModel):
    subject_name: str
    year: int
    semester: int
    credits: int
    track: Optional[str] = None  # Optional track field to accommodate subjects without track

# Schema for creating new subjects (can be used when inserting data)
class SubjectCreate(SubjectBase):
    pass

# Schema for returning a subject response (can be used in API responses)
class SubjectResponse(SubjectBase):
    subject_id: str  # Use str for subject_id (since it's a string in the database)

    class Config:
        from_attributes = True
