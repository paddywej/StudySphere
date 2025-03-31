from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, Base 
from fastapi.middleware.cors import CORSMiddleware
from .database import SessionLocal, get_db
from .models import *
from passlib.context import CryptContext
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins, change to specific domains if needed
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

Base.metadata.create_all(bind=engine)

# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Utility to hash passwords
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Request Model
class RegisterRequest(BaseModel):
    user_id: str
    password: str
    role: str

@app.post("/register")
def register_user(request: RegisterRequest, db: Session = Depends(get_db)):
    # Check role and find user
    if request.role == "Student":
        user = db.query(Student).filter(Student.student_id == request.user_id).first()
    elif request.role == "Professor":
        user = db.query(Professor).filter(Professor.professor_id == request.user_id).first()
    else:
        raise HTTPException(status_code=400, detail="Invalid role selected.")

    # Check if user exists
    if not user:
        raise HTTPException(status_code=404, detail="ID does not exist")

    # Ensure user doesn't already have a password
    if user.password is not None:
        raise HTTPException(status_code=400, detail="User already has a password.")

    # Hash the password and store it
    user.password = get_password_hash(request.password)
    db.commit()

    return {"message": "Registration successful"}


@app.websocket("/_event/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message received: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")

# Create Student
@app.post("/students/", response_model=schemas.StudentResponse)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    new_student = models.Student(**student.dict())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

# Get Students
@app.get("/students/", response_model=list[schemas.StudentResponse])
def get_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()

# Create Grade
@app.post("/grades/", response_model=schemas.GradeResponse)
def create_grade(grade: schemas.GradeCreate, db: Session = Depends(get_db)):
    new_grade = models.Grade(**grade.dict())
    db.add(new_grade)
    db.commit()
    db.refresh(new_grade)
    return new_grade

@app.post("/subjects/", response_model=schemas.SubjectResponse)
def create_subject(subject: schemas.SubjectCreate, db: Session = Depends(get_db)):
    db_subject = models.Subject(**subject.dict())
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject

@app.get("/subjects/{subject_id}", response_model=schemas.SubjectResponse)
def get_subject(subject_id: int, db: Session = Depends(get_db)):
    subject = db.query(models.Subject).filter(models.Subject.subject_id == subject_id).first()
    if subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subject

@app.get("/subjects/{year}/{semester}")
def get_subjects(year: int, semester: int, db: Session = Depends(get_db)):
    """Fetch subjects based on year and semester."""
    subjects = db.query(Subject).filter(Subject.year == year, Subject.semester == semester).all()
    return [subject.subject_name for subject in subjects] 

