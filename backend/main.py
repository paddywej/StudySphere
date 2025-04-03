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
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
import os
import logging
import uuid
from sqlalchemy import cast, Integer

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


@app.get("/subjects/{subject_id}", response_model=schemas.Subject)
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

@app.get("/professors/{professor_id}/subjects", response_model=list[str])
def get_professor_subjects(professor_id: str, db: Session = Depends(get_db)):
    professor = db.query(Professor).filter(Professor.professor_id == professor_id).first()
    if not professor:
        raise HTTPException(status_code=404, detail="Professor not found")

    # professor.subject_list is a list of subject_ids (strings)
    subject_ids = professor.subject_list  # This should already be a list of subject_ids

    return subject_ids  # Return the list of subject IDs directly

@app.get("/get_subject_name/{subject_id}")
async def get_subject_name(subject_id: str, db: Session = Depends(get_db)):
    subject = db.query(Subject).filter(Subject.subject_id == subject_id).first()

    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    return {"subject_name": subject.subject_name}

@app.get("/subjects_detail/{subject_id}")
def get_subject_details(subject_id: str, db: Session = Depends(get_db)):
    subject = db.query(Subject).filter(Subject.subject_id == subject_id).first()

    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    # Ensure student_list is either an empty list or valid
    student_list = subject.student_list if isinstance(subject.student_list, list) else []

    return {
        "subject_id": subject.subject_id,
        "subject_name": subject.subject_name,
        # "year": subject.year,
        # "semester": subject.semester,
        # "track": subject.track,
        # "credits": subject.credits,
        # "student_list": student_list,  # Return an empty list if not valid
    }

@app.get("/professors/{user_id}/name")
def get_professor_name(user_id: str, db: Session = Depends(get_db)):
    # Query the database for the professor by their user_id
    professor = db.query(Professor).filter(Professor.professor_id == user_id).first()

    if not professor:
        raise HTTPException(status_code=404, detail="Professor not found")

    return professor.name

@app.get("/check_enrollment/{user_id}/{subject_name}")
def check_enrollment(user_id: str, subject_name: str, db: Session = Depends(get_db)):
    subject = db.query(Subject).filter(Subject.subject_name == subject_name).first()

    if not subject:
        return {"enrolled": False, "message": "Subject not found"}

    if not subject.student_list:
        print("No students enrolled in this subjec")
        return {"enrolled": False, "message": "No students enrolled in this subject"}

    if user_id in subject.student_list:
        return {"enrolled": True}

    return {"enrolled": False, "message": "User is not enrolled in this subject"}

@app.get("/get_subject_id/{subject_name}") 
def get_subject_id(subject_name: str, db: Session = Depends(get_db)):
    """Fetch the subject_id from the Subject table using subject_name."""
    subject = db.query(Subject).filter(Subject.subject_name == subject_name).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return {"subject_id": subject.subject_id}  

@app.get("/get_lectures/{subject_id}")
async def get_lectures(subject_id: str, db: Session = Depends(get_db)) -> dict[str, list[str]]:
    """Fetch lectures for a given subject_id."""
    
    # Query the Lecture table where subject_id matches
    lectures = db.query(Lecture).filter(Lecture.subject_id == subject_id).all()

    # Extract only lecture names (assuming Lecture has a `name` field)
    lecture_names = [lecture.name for lecture in lectures]
    
    return {"lectures": lecture_names}  # Return as JSON

@app.get("/get_materials/{subject_id}")
async def get_materials(subject_id: str, db: Session = Depends(get_db)) -> dict[str, list[dict]]:
    """Fetch materials for a given subject_id including names and types."""
    
    materials = db.query(Material).filter(Material.subject_id == subject_id).all()

    # Return a list of dictionaries with name and type
    material_list = [{"name": material.name, "type": material.type} for material in materials]
    
    return {"materials": material_list}  



@app.get("/lecture/{subject_id}/{lecture_name}")
async def get_lecture_url(subject_id: str, lecture_name: str, db: Session = Depends(get_db)):
    """
    Fetch the video URL of a lecture by subject_id and lecture_name.
    """
    # 🔹 Query the database properly instead of using `db.get()`
    lecture = db.query(Lecture).filter(
        Lecture.subject_id == subject_id, Lecture.name == lecture_name
    ).first()

    if lecture:
        return {"video_url": lecture.file_path}
    else:
        return {"error": "Lecture not found"}, 404

@app.delete("/delete_lecture/{subject_id}/{lecture_name}")
async def delete_lecture(subject_id: str, lecture_name: str, db: Session = Depends(get_db)):
    """
    Delete a lecture by subject_id and lecture_name.
    """
    # Query the lecture from the database
    lecture = db.query(Lecture).filter(
        Lecture.subject_id == subject_id, Lecture.name == lecture_name
    ).first()

    if lecture:
        db.delete(lecture)  # Delete lecture
        db.commit()  # Save changes
        return {"message": f"Lecture '{lecture_name}' deleted successfully"}
    
    raise HTTPException(status_code=404, detail="Lecture not found")

@app.delete("/delete_material/{subject_id}/{material_name}")
async def delete_material(subject_id: str, material_name: str, db: Session = Depends(get_db)):
    """
    Delete a material (either note or textbook) by subject_id and material_name.
    """
    material = db.query(Material).filter(
        Material.subject_id == subject_id, Material.name == material_name
    ).first()

    if material:
        db.delete(material)
        db.commit()
        return {"message": f"Material '{material_name}' deleted successfully"}

    raise HTTPException(status_code=404, detail="Material not found")
    
@app.post("/lectures/{subject_id}/upload/")
async def upload_lecture(
    subject_id: str,  # Ensure subject_id is captured from the URL
    lecture_id: str = Form(...),
    lecture_name: str = Form(...),
    lecture_date: str = Form(...),
    lecture_time: str = Form(...),
    file: UploadFile = File(...),  # Corrected from FastAPIFile
    db: Session = Depends(get_db),
):
    upload_dir = f"uploads/lectures/{subject_id}"
    os.makedirs(upload_dir, exist_ok=True)  # Ensure directory exists

    file_path = os.path.join(upload_dir, file.filename.replace(" ", "_"))

    try:
        with open(file_path, "wb") as f:
            for chunk in iter(lambda: file.file.read(4096), b""):
                f.write(chunk)
    except Exception as e:
        logging.error(f"Error writing file: {e}")
        raise HTTPException(status_code=500, detail="Error saving file")

    # Store file path in the database under Lecture
    new_lecture = Lecture(
        lecture_id=lecture_id,  # Generate unique ID for lecture
        subject_id=subject_id,
        name=lecture_name,
        date=lecture_date,
        time=lecture_time,
        file_path=file_path,
    )

    try:
        db.add(new_lecture)
        db.commit()
        db.refresh(new_lecture)
    except Exception as e:
        db.rollback()
        logging.error(f"Error saving lecture to database: {e}")
        raise HTTPException(status_code=500, detail="Error saving lecture to database")

    return {"message": "Lecture uploaded successfully", "file_path": file_path}


@app.post("/materials/{subject_id}/upload/")
async def upload_material(
    subject_id: str,
    file: UploadFile = File(...),
    material_id: str = Form(...),
    material_name: str = Form(...),
    material_type: str = Form(...),
    db: Session = Depends(get_db)
):

    upload_dir = f"uploads/materials/{subject_id}"
    os.makedirs(upload_dir, exist_ok=True)  # Ensure directory exists

    # Define the file path
    file_path = os.path.join(upload_dir , file.filename.replace(" ", "_"))

    try:
        with open(file_path, "wb") as f:
            for chunk in iter(lambda: file.file.read(4096), b""):
                f.write(chunk)
    except Exception as e:
        logging.error(f"Error writing file: {e}")
        raise HTTPException(status_code=500, detail="Error saving file")

    # Save the uploaded file
    # with open(file_path, "wb") as buffer:
    #     shutil.copyfileobj(file.file, buffer)

    # Save material information to the database
    new_material = Material(
        material_id=material_id,
        subject_id=subject_id,
        name=material_name,
        type=material_type,
        file_path=file_path
    )
    try:
        db.add(new_material)
        db.commit()
        db.refresh(new_material)
    except Exception as e:
        db.rollback()
        logging.error(f"Error saving material to database: {e}")
        raise HTTPException(status_code=500, detail="Error saving material to database")

    return {"message": "Material uploaded successfully", "file_path": file_path}