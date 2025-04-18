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
from sqlalchemy import cast, Integer,func
from typing import Dict,List
import shutil
from datetime import datetime
from fastapi.staticfiles import StaticFiles

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

@app.get("/get_student_list/{subject_id}", response_model=List[str])
async def get_student_list(subject_id: str, db: Session = Depends(get_db)):
    # Fetch the subject based on subject_id
    subject = db.query(Subject).filter(Subject.subject_id == subject_id).first()

    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    # student_list is an array of student IDs in the Subject model
    student_list = subject.student_list or []  # Use empty list if no students

    return student_list

@app.post("/subjects/{subject_id}/add_students/")
async def add_students_to_subject(subject_id: str, students: list, db: Session = Depends(get_db)):
    subject = db.query(Subject).filter(Subject.subject_id == subject_id).first()

    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    
    # Add students to the subject's student list
    for student_id in students:
        if student_id not in subject.student_list:
            subject.student_list.append(student_id)

    db.commit()

    return {"message": "Students added successfully"}

@app.post("/user_session/{user_id}/{role}")
def user_session(user_id: str, role: str, db: Session = Depends(get_db)):
    user_session = db.query(UserSession).filter(UserSession.session_id == "S001").first()

    if not user_session:
        raise HTTPException(status_code=404, detail="User session not found")

    user_session.user_id=user_id,
    user_session.role=role,
    user_session.subject_id=None 

    db.commit()
    db.refresh(user_session)
    return user_session

@app.post("/subject_session/{user_id}/{subject_id}")
def subject_session(user_id: str, subject_id: str, db: Session = Depends(get_db)):
    # Retrieve the user session based on user_id
    user_session = db.query(UserSession).filter(UserSession.user_id == user_id).first()

    if not user_session:
        raise HTTPException(status_code=404, detail="User session not found")

    # Update the subject_id for the user session
    user_session.subject_id = subject_id  

    # Commit the transaction and refresh the session to get the latest state
    db.commit()
    db.refresh(user_session)  
    return user_session

@app.get("/user_session/subject")
def subject_id_session(db: Session = Depends(get_db)):
    user_session = db.query(UserSession).filter(UserSession.session_id == "S001").first()

    if not user_session:
        raise HTTPException(status_code=404, detail="User session not found")

    return user_session.subject_id

@app.get("/user_session/student")
def student_id_session(db: Session = Depends(get_db)):
    user_session = db.query(UserSession).filter(UserSession.session_id == "S001").first()

    if not user_session:
        raise HTTPException(status_code=404, detail="User session not found")

    return user_session.user_id

@app.put("/add_student/{subject_id}/{student}")
def add_student_to_subject(subject_id: str, student: str, db: Session = Depends(get_db)):
    # Query the subject by subject_id
    subject = db.query(Subject).filter(Subject.subject_id == subject_id).first()

    # Check if the subject exists
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    # Initialize student_list if it's None
    if not subject.student_list:  
        subject.student_list = []

    # Rebuild the student list and append the new student
    if student not in subject.student_list:
        subject.student_list.append(student)
        db.commit()  # Commit the changes to the database
        db.refresh(subject)  # Refresh the object to get updated data from DB
        
        return {"message": f"Student {student} added to subject {subject_id}"}
    else:
        raise HTTPException(status_code=400, detail="Student already exists in subject")


@app.put("/remove_student/{subject_id}/{student}")
def remove_student_from_subject(subject_id: str, student: str, db: Session = Depends(get_db)):
    subject = db.query(Subject).filter(Subject.subject_id == subject_id).first()

    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    # Check if the student is in the list
    if student in subject.student_list:
        # Create a new list excluding the student
        updated_student_list = [s for s in subject.student_list if s != student]
        
        # Update the subject's student list with the new list
        subject.student_list = updated_student_list
        
        # Commit the changes
        db.commit()
        db.refresh(subject)  # Refresh to get updated data from DB
        return {"message": f"Student {student} removed from subject {subject_id}"}
    else:
        raise HTTPException(status_code=400, detail="Student not found in subject")

@app.put("/add_subject/{subject_id}/{user_id}")
def add_subject(subject_id: str, user_id: str, db: Session = Depends(get_db)):
    # Query the subject by subject_id
    professor = db.query(Professor).filter(Professor.professor_id == user_id).first()

    # Check if the subject exists
    if not professor:
        raise HTTPException(status_code=404, detail="Professor not found")

    # Check if the student is already in the student_list
    if subject_id in professor.subject_list:
        raise HTTPException(status_code=400, detail="Subject already exists in subject")
    
    # Rebuild the student list and append the new student
    professor.subject_list = professor.subject_list + [subject_id]
    
    db.commit()  # Commit the changes to the database
    db.refresh(professor)  # Refresh the object to get updated data from DB
    
    return {"message": f"{student} added"}

@app.put("/remove_subject/{subject_id}/{user_id}")
def remove_subject(subject_id: str, user_id: str, db: Session = Depends(get_db)):
    professor = db.query(Professor).filter(Professor.professor_id == user_id).first()

    if not professor:
        raise HTTPException(status_code=404, detail="Professor not found")

    if not professor.subject_list:
        raise HTTPException(status_code=400, detail="No subjects found for professor")

    if subject_id in professor.subject_list:
        professor.subject_list = [s for s in professor.subject_list if s != subject_id]
        db.commit()
        db.refresh(professor)
        return {"message": f"Subject {subject_id} removed from professor {user_id}"}
    else:
        raise HTTPException(status_code=400, detail="Subject not found in professor's list")


@app.post("/add_assignment")
def create_assignment(
    assessment_id: str = Form(...),
    subject_id: str = Form(...),
    name: str = Form(...),
    due_date: str = Form(...),
    published_date: str = Form(...),
    status: str = Form(...),
    assessment_type: str = Form(...),
    file_name: str = Form(...),  # <-- Accept file name only
    db: Session = Depends(get_db),
):

    # Convert string dates to datetime objects
    try:
        due_dt = datetime.strptime(due_date, "%Y-%m-%dT%H:%M:%S.%f")
        pub_dt = datetime.strptime(published_date, "%Y-%m-%dT%H:%M:%S.%f")
    except ValueError as e:
        logging.error(f"Date parsing error: {e}")
        raise HTTPException(status_code=400, detail="Invalid date format")

    # Create new assessment record
    new_assessment = Assessment(
        assessment_id=assessment_id,
        subject_id=subject_id,
        name=name,
        due_date=due_dt,
        published_date=pub_dt,
        status=status,
        assessment_type=assessment_type,
        file_path=file_name  # Save file name as a path format
    )

    try:
        db.add(new_assessment)
        db.commit()
        db.refresh(new_assessment)
        return {"message": "Assessment created successfully", "id": assessment_id}

    except Exception as e:
        logging.error(f"Database error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/add_quiz")
def create_quiz(
    assessment_id: str = Form(...),
    subject_id: str = Form(...),
    name: str = Form(...),
    due_date: str = Form(...),
    published_date: str = Form(...),
    status: str = Form(...),
    assessment_type: str = Form(...),
    file_name: str = Form(...),  # <-- Accept file name only
    db: Session = Depends(get_db),
):

    # Convert string dates to datetime objects
    try:
        due_dt = datetime.strptime(due_date, "%Y-%m-%dT%H:%M:%S.%f")
        pub_dt = datetime.strptime(published_date, "%Y-%m-%dT%H:%M:%S.%f")
    except ValueError as e:
        logging.error(f"Date parsing error: {e}")
        raise HTTPException(status_code=400, detail="Invalid date format")

    # Create new assessment record
    new_assessment = Assessment(
        assessment_id=assessment_id,
        subject_id=subject_id,
        name=name,
        due_date=due_dt,
        published_date=pub_dt,
        status=status,
        assessment_type=assessment_type,
        file_path=file_name  # Save file name as a path format
    )

    try:
        db.add(new_assessment)
        db.commit()
        db.refresh(new_assessment)
        return {"message": "Assessment created successfully", "id": assessment_id}

    except Exception as e:
        logging.error(f"Database error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/add_exam")
def create_exam(
    assessment_id: str = Form(...),
    subject_id: str = Form(...),
    name: str = Form(...),
    due_date: str = Form(...),
    published_date: str = Form(...),
    status: str = Form(...),
    assessment_type: str = Form(...),
    file_name: str = Form(...),  # <-- Accept file name only
    db: Session = Depends(get_db),
):

    # Convert string dates to datetime objects
    try:
        due_dt = datetime.strptime(due_date, "%Y-%m-%dT%H:%M:%S.%f")
        pub_dt = datetime.strptime(published_date, "%Y-%m-%dT%H:%M:%S.%f")
    except ValueError as e:
        logging.error(f"Date parsing error: {e}")
        raise HTTPException(status_code=400, detail="Invalid date format")

    # Create new assessment record
    new_assessment = Assessment(
        assessment_id=assessment_id,
        subject_id=subject_id,
        name=name,
        due_date=due_dt,
        published_date=pub_dt,
        status=status,
        assessment_type=assessment_type,
        file_path=file_name  # Save file name as a path format
    )

    try:
        db.add(new_assessment)
        db.commit()
        db.refresh(new_assessment)
        return {"message": "Assessment created successfully", "id": assessment_id}

    except Exception as e:
        logging.error(f"Database error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/delete_assignment/{subject_id}/{assignment_name}")
async def delete_assignment(subject_id: str, assignment_name: str, db: Session = Depends(get_db)):
    # Query the assignment to check if it exists
    assignment = db.query(Assessment).filter(
        Assessment.subject_id == subject_id,
        Assessment.name == assignment_name,
        Assessment.assessment_type == "Assignment"
    ).first()

    # If the assignment exists, delete it
    if assignment:
        db.delete(assignment)
        db.commit()
        return {"message": f"Assignment '{assignment_name}' deleted successfully"}
    
    # Raise an exception if the assignment is not found
    raise HTTPException(status_code=404, detail="Assignment not found")

@app.delete("/delete_exam/{subject_id}/{exam_name}")
async def delete_exam(subject_id: str, exam_name: str, db: Session = Depends(get_db)):
    exam = db.query(Assessment).filter(
        Assessment.subject_id == subject_id,
        Assessment.name == exam_name,
        Assessment.assessment_type == "Exam"
    ).first()

    if exam:
        db.delete(exam)
        db.commit()
        return {"message": f"Exam '{exam_name}' deleted successfully"}
    
    raise HTTPException(status_code=404, detail="Exam not found")

@app.delete("/delete_quiz/{subject_id}/{quiz_name}")
async def delete_quiz(subject_id: str, quiz_name: str, db: Session = Depends(get_db)):
    quiz = db.query(Assessment).filter(
        Assessment.subject_id == subject_id,
        Assessment.name == quiz_name,
        Assessment.assessment_type == "Quiz"
    ).first()

    if quiz:
        db.delete(quiz)
        db.commit()
        return {"message": f"Quiz '{quiz_name}' deleted successfully"}
    
    raise HTTPException(status_code=404, detail="Quiz not found")

@app.get("/get_assignments/{subject_id}")
async def get_assignments(subject_id: str, db: Session = Depends(get_db)):
    try:
        # Query to get assignments by subject_id where assessment_type is "Assignment"
        assignments = db.query(Assessment).filter(
            Assessment.subject_id == subject_id, 
            Assessment.assessment_type == "Assignment"
        ).all()

        # Extract only the necessary fields (name, due_date, file_path)
        assignment_list = [{"name": assignment.name, "due_date": assignment.due_date, "file_path": assignment.file_path} for assignment in assignments]

        return {"assignments": assignment_list}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving assignments: {str(e)}")

@app.get("/get_quizs/{subject_id}")
async def get_quizs(subject_id: str, db: Session = Depends(get_db)):
    try:

        quizs = db.query(Assessment).filter(
            Assessment.subject_id == subject_id, 
            Assessment.assessment_type == "Quiz"
        ).all()

        # Extract only the necessary fields (name, due_date, file_path)
        quiz_list = [{"name": quiz.name, "due_date": quiz.due_date, "file_path": quiz.file_path} for quiz in quizs]

        return {"quizs": quiz_list}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving quizs: {str(e)}")


@app.get("/get_exams/{subject_id}")
async def get_exams(subject_id: str, db: Session = Depends(get_db)):
    try:

        exams = db.query(Assessment).filter(
            Assessment.subject_id == subject_id, 
            Assessment.assessment_type == "Exam"
        ).all()

        # Extract only the necessary fields (name, due_date, file_path)
        exam_list = [{"name": exam.name, "due_date": exam.due_date, "file_path": exam.file_path} for exam in exams]

        return {"exams": exam_list}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving exams: {str(e)}")

@app.get("/get_file_ass/{subject_id}/{name}")
def get_file_assignment(subject_id: str, name: str, db: Session = Depends(get_db)):
    try:
        assessment = db.query(Assessment).filter(
            Assessment.subject_id == subject_id,
            Assessment.name == name,
            Assessment.assessment_type == "Assignment"  # Ensure it's an assignment
        ).first()

        if assessment is None:
            raise HTTPException(status_code=404, detail="Assignment not found")

        # Return both file path and due date (format date to string if needed)
        return {
            "file_path": assessment.file_path,
            "due_date": assessment.due_date.strftime("%Y-%m-%d")
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving assignment details: {str(e)}")

@app.get("/get_file_exam/{subject_id}/{name}")
def get_file_exam(subject_id: str, name: str, db: Session = Depends(get_db)):
    try:
        assessment = db.query(Assessment).filter(
            Assessment.subject_id == subject_id,
            Assessment.name == name,
            Assessment.assessment_type == "Exam"  # Ensure it's an assignment
        ).first()

        if assessment is None:
            raise HTTPException(status_code=404, detail="Assignment not found")

        # Return both file path and due date (format date to string if needed)
        return {
            "file_path": assessment.file_path,
            "due_date": assessment.due_date.strftime("%Y-%m-%d")
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving assignment details: {str(e)}")


@app.get("/get_file_quiz/{subject_id}/{name}")
def get_file_quiz(subject_id: str, name: str, db: Session = Depends(get_db)):
    try:
        assessment = db.query(Assessment).filter(
            Assessment.subject_id == subject_id,
            Assessment.name == name,
            Assessment.assessment_type == "Quiz"  # Ensure it's an assignment
        ).first()

        if assessment is None:
            raise HTTPException(status_code=404, detail="Assignment not found")

        # Return both file path and due date (format date to string if needed)
        return {
            "file_path": assessment.file_path,
            "due_date": assessment.due_date.strftime("%Y-%m-%d")
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving assignment details: {str(e)}")


@app.get("/get_assessment_id/{subject_id}/{assessment_name}")
def get_assessment_id(subject_id: str, assessment_name: str, db: Session = Depends(get_db)):
    try:
        # Query to get the assessment by subject_id and name
        assessment = db.query(Assessment).filter(
            Assessment.subject_id == subject_id,
            Assessment.name == assessment_name
        ).first()

        if not assessment:
            raise HTTPException(status_code=404, detail="Assessment not found")

        return {"assessment_id": assessment.assessment_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving assessment_id: {str(e)}")

@app.post("/submit_assignment/")
def create_assignment(
    submission_id: str = Form(...),
    assessment_id: str = Form(...),
    student_id: str = Form(...),
    file_path: str = Form(...),
    submitted_time: str = Form(...),
    last_modified: str = Form(...),
    status: str = Form(...),
    db: Session = Depends(get_db),
):

    os.makedirs

    try:
        psub_t = datetime.strptime(submitted_time, "%Y-%m-%dT%H:%M:%S.%f")
    except ValueError as e:
        logging.error(f"Date parsing error: {e}")
        raise HTTPException(status_code=400, detail="Invalid date format")

    # Create new assessment record
    new_submission = Submission(
        submission_id=submission_id,  # Correct the typo here
        assessment_id=assessment_id,
        student_id=student_id,
        file_path=file_path,  # Path to the file
        submitted_time=submitted_time,
        last_modified=last_modified,
        status=status
    )

    try:
        db.add(new_submission)
        db.commit()
        db.refresh(new_submission)
        return {"message": "Success submittion", "id": submission_id}

    except Exception as e:
        logging.error(f"Database error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/get_submission_file/{submission_id}")
def get_submission_file(submission_id: str, db: Session = Depends(get_db)):
    submission = db.query(Submission).filter(Submission.submission_id == submission_id).first()

    if submission is None:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    # Return the file path from the submission
    return {"file_path": submission.file_path}


@app.post("/submit_exam/")
def create_assignment(
    submission_id: str = Form(...),
    assessment_id: str = Form(...),
    student_id: str = Form(...),
    file_path: str = Form(...),
    submitted_time: str = Form(...),
    last_modified: str = Form(...),
    status: str = Form(...),
    db: Session = Depends(get_db),
):

    try:
        psub_t = datetime.strptime(submitted_time, "%Y-%m-%dT%H:%M:%S.%f")
    except ValueError as e:
        logging.error(f"Date parsing error: {e}")
        raise HTTPException(status_code=400, detail="Invalid date format")

    # Create new assessment record
    new_submission = Submission(
        submission_id=submission_id,  # Correct the typo here
        assessment_id=assessment_id,
        student_id=student_id,
        file_path=file_path,  # Path to the file
        submitted_time=submitted_time,
        last_modified=last_modified,
        status=status
    )

    try:
        db.add(new_submission)
        db.commit()
        db.refresh(new_submission)
        return {"message": "Success submittion", "id": submission_id}

    except Exception as e:
        logging.error(f"Database error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/get_submission_file/{submission_id}")
def get_submission_file(submission_id: str, db: Session = Depends(get_db)):
    submission = db.query(Submission).filter(Submission.submission_id == submission_id).first()

    if submission is None:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    # Return the file path from the submission
    return {"file_path": submission.file_path}

@app.get("/get_submissions/{assessment_id}")
def get_submissions_by_assessment(assessment_id: str, db: Session = Depends(get_db)):
    submissions = db.query(Submission).filter(Submission.assessment_id == assessment_id).all()

    if not submissions:
        return {"submissions": []}

    result = [
        {
            "student_id": submission.student_id,
            "file_path": submission.file_path
        }
        for submission in submissions
    ]
    return {"submissions": result}

@app.get("/get_assessment_id/{subject_id}/{name}")
def get_exam_id(subject_id: str, name: str, db: Session = Depends(get_db)):
    # Query the database for the specific exam
    exam = db.query(Assessment).filter(
        Assessment.subject_id == subject_id,
        Assessment.name == name,
        Assessment.assessment_type == "Exam"
    ).first()

    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")

    # Return the assessment ID if found
    return {"assessment_id": exam.assessment_id}