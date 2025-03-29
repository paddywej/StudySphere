from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Student Schema
class StudentBase(BaseModel):
    name: str
    email: str
    year_level: str

class StudentCreate(StudentBase):
    pass

class StudentResponse(StudentBase):
    student_id: int
    class Config:
        from_attributes = True

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

# Subject Schema
class SubjectBase(BaseModel):
    subject_name: str
    year: int
    semester: int
    credits: int  

class SubjectCreate(SubjectBase):
    pass

class SubjectResponse(SubjectBase):
    subject_id: int

    class Config:
        from_attributes = True