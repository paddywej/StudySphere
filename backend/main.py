from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, Base 
from fastapi.middleware.cors import CORSMiddleware
from .database import SessionLocal, get_db
from .models import *
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import Optional
import reflex as rx
from fastapi import Request

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

# Utility to verify passwords
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Request Model
class RegisterRequest(BaseModel):
    user_id: str
    password: str
    role: str

class LoginRequest(BaseModel):
    user_id: str
    password: str
    role: str

@app.websocket("/_event/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message received: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")

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

@app.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    if request.role == "Student":
        user = db.query(Student).filter(Student.student_id == request.user_id).first()
        
    elif request.role == "Professor":
        user = db.query(Professor).filter(Professor.professor_id == request.user_id).first()
        
    else:
        raise HTTPException(status_code=400, detail="Invalid role selected.")

    if not user or not verify_password(request.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password.")

    

    return {"message": "Login successful", "user_id": request.user_id, "role": request.role}

@app.post("/logout")
def logout(request):
    usersession.set("","",False)

    return {"message": "Logged out successfully."}

@app.get("/students/{user_id}/year")
def get_year(user_id: str, db: Session = Depends(get_db)):
    # Query the database to find the student by user_id
    student = db.query(Student).filter(Student.student_id == user_id).first()

    # If student does not exist, raise HTTPException
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Return as a dictionary (JSON format)
    return {"year": student.year, "track": student.track}


@app.get("/subjects/{subject_id}", response_model=schemas.SubjectResponse)
def get_subject(subject_id: int, db: Session = Depends(get_db)):
    subject = db.query(models.Subject).filter(models.Subject.subject_id == subject_id).first()
    if subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subject

@app.get("/subjects/{year}/{semester}")
def get_subjects(year: int, semester: int, track: str | None = None, db: Session = Depends(get_db)):
    subjects = db.query(Subject).filter(Subject.year == year, Subject.semester == semester).all()

    # If track is specified, filter by track as well
    if track:
        track_subjects = db.query(Subject).filter(
            Subject.year == year, Subject.semester == semester, Subject.track == track
        ).all()
        subjects.extend(track_subjects)

    if not subjects:
        raise HTTPException(status_code=404, detail="No subjects found")

    return [subject.subject_name for subject in subjects]
