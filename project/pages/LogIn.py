import reflex as rx
import requests
# from project.state.formstate import FormState
import uuid
import datetime
from io import BytesIO
import asyncio
from typing import Dict,List
from project.pages.exampage import State

class FormState(rx.State):
    user_id: str = ""
    role: str = ""
    message: str = ""
    status: bool = False
    subject_name: str = ""
    subject_id: str = ""
    video: str = ""
    lecture_list: list = []
    lecture_name: str = ""
    lecture_url: str = ""
    note_list: list = []
    textbook_list: list = []

    # Student-specific attributes
    student_year: str = ""
    student_track: str | None = None
    student_subjects_sem1: list = []
    student_subjects_sem2: list = []
    

    # Professor-specific attributes
    subjects_taught_id: list = []
    subjects_taught_name: list = []
    subject_details: Dict[str, Dict[str, str]] = {}
    material_type: str = "Textbooks"
    professor_name:str = ""
    

    async def set_material_type(self, material_type: str):
        """Set the selected material type."""
        self.material_type = material_type

    def set_user_session(self):
        url = f"http://localhost:8000/user_session/{self.user_id}/{self.role}"
        response = requests.post(url)  # Change to POST, since we are creating a record
        if response.status_code == 200:
            print("set usersession:", self.user_id)
        else:
            print(f"Error usersession: {self.user_id}, Status Code: {response.status_code}")
            print(f"Response Text: {response.text}")  # Debugging: log the response text


    def set_subject_session(self):
        url = f"http://localhost:8000/subject_session/{self.user_id}/{self.subject_id}"
        response = requests.post(url)  # Change to POST, since we are creating a record
        if response.status_code == 200:
            print("set session subject:",self.subject_id)
        else:
            print("Error session subject:",self.subject_id)


    def handle_submit(self, form_data: dict):
        """Handles user login and fetches additional details based on role."""
        response = requests.post("http://127.0.0.1:8000/login", json=form_data)

        if response.status_code == 200:
            data = response.json()
            self.user_id = data["user_id"]
            self.role = data["role"]
            print(self.user_id)

            self.set_user_session()

            yield rx.toast.info("Log In Successful!", position="top-center")

            # Fetch additional data in background (doesn't block UI)
            if self.role == "Student":
                self.fetch_student_details()
                print(f"Student Year: {self.student_year}, Track: {self.student_track}")  # Debugging print
                print(f"Subjects Semester 1: {self.student_subjects_sem1}")  # Debugging print
                print(f"Subjects Semester 2: {self.student_subjects_sem2}")  # Debugging print
                self.status = True     
            
            if self.role == "Professor":
                self.get_professor_name()
                self.fetch_professor_subjects()
                print(f"{self.subjects_taught_id}")
                print(f"{self.subjects_taught_name}")
                self.status = True

            if self.role == "Student" and self.status==True:
                yield rx.redirect("/subject")

            if self.role == "Professor" and self.status==True:
                yield rx.redirect("/professor_subjects")  

        else:
            self.message = response.json().get("detail", "Invalid username or password.")


    def fetch_student_details(self):
        """Fetches student year and track, then fetches subjects for both semesters."""
        url = f"http://localhost:8000/students/{self.user_id}/year"
        response = requests.get(url)

        if response.status_code == 200:
            student_data = response.json()
            self.student_year = student_data.get("year", 0)
            self.student_track = student_data.get("track") if self.student_year in [3, 4] else None

            self.student_subjects_sem1 = self.get_subjects(self.student_year, 1, self.student_track)
            self.student_subjects_sem2 = self.get_subjects(self.student_year, 2, self.student_track)

    def fetch_professor_subjects(self):
        """Fetches subjects taught by a professor and their details."""
        url = f"http://localhost:8000/professors/{self.user_id}/subjects"
        response = requests.get(url)

        if response.status_code == 200:
            self.subjects_taught_id = response.json()  # Assuming it's a list of subject IDs
            print("Subjects taught:", self.subjects_taught_id)  # Debugging print
            self.get_subjects_name()
        else:
            print("Failed to fetch subjects:", response.status_code, response.text)

    
    def get_professor_name(self):
        url = f"http://localhost:8000/professors/{self.user_id}/name"
        response = requests.get(url)

        if response.status_code == 200:
            # Remove the surrounding quotation marks if present
            self.professor_name = response.text.strip('"')
            print(self.professor_name )
        else:
            print(f"Failed to fetch professor name: {response.status_code}")
            self.professor_name = None

        return self.professor_name

    # def fetch_subject_details(self, subject_id: str):
    #     """Fetch subject details by subject_id."""
    #     url = f"http://localhost:8000/subjects_detail/{subject_id}"
    #     response = requests.get(url)

    #     if response.status_code == 200:
    #         subject_data = response.json()
    #         subject_info = {
    #             "subject_id": subject_id,
    #             "name": subject_data.get("subject_name"),
    #             # "year": subject_data.get("year"),
    #             # "semester": subject_data.get("semester"),
    #             # "track": subject_data.get("track"),
    #             # "student_list": subject_data.get("student_list"),
    #         }
            
    #         # Store the subject_info in the subject_details dictionary using subject_id as the key
    #         self.subject_details[subject_id] = subject_info
    #         print("Fetched subject details:", subject_info)  # Debugging print
    #         print(self.subject_details)

    #     else:
    #         print(f"Failed to fetch details for subject {subject_id}:", response.status_code, response.text)


    
    def get_subjects(self, year: int, semester: int, track: str | None = None) -> list:
        """Fetch subjects based on student year, semester, and track."""
        url = f"http://localhost:8000/subjects/{year}/{semester}"
        response = requests.get(url)
        
        return response.json() if response.status_code == 200 else []

    # Make the get_subjects_id async
    async def get_subjects_id(self, subject_name: str):
        """Fetch subject_id based on subject_name."""
        url = f"http://localhost:8000/get_subject_id/{subject_name}"  
        response = await asyncio.to_thread(requests.get, url)  # Send the request in a separate thread
        if response.status_code == 200:
            self.subject_id = response.json().get("subject_id", "")
        else:
            self.subject_id = ""

    def get_subjects_name(self):
        self.subjects_taught_name=[]

        """Fetch subject name for each subject_id and store them in subjects_taught_name."""
        for subject_id in self.subjects_taught_id:
            url = f"http://localhost:8000/get_subject_name/{subject_id}"
            response = requests.get(url)

            if response.status_code == 200:
                subject_data = response.json()
                subject_name = subject_data.get("subject_name", "")

                if subject_name:
                    self.subjects_taught_name.append(subject_name)  # Store the subject name in the list
            else:
                print(f"Error fetching subject for {subject_id}, status code: {response.status_code}")

    # Ensure set_subject is also async
    async def set_subject(self, subject_name: str):
        self.subject_name = subject_name
        await self.get_subjects_id(self.subject_name)
        self.set_subject_session()
        
        # Check if user is a professor
        if self.role == "Professor":  
              # Fetch subject ID directly
            await self.fetch_lectures()
            yield rx.redirect("/lecture_menu")  # Redirect immediately
        else:
            # Check enrollment for students
            url = f"http://127.0.0.1:8000/check_enrollment/{self.user_id}/{self.subject_name}"
            response = await asyncio.to_thread(requests.get, url)  # Send the request in a separate thread
            
            if response.status_code == 200 and response.json().get("enrolled", False):
                await self.fetch_lectures()
                yield rx.redirect("/lecture_menu")
            else:
                yield rx.toast.error("You are not enrolled in this subject", position="top-center")

    async def get_lecture(self, lecture_name: str):
        """Fetch the lecture video for the given subject_id and lecture_name"""
        self.lecture_name = lecture_name
        url = f"http://127.0.0.1:8000/lecture/{self.subject_id}/{self.lecture_name}"

        response = await asyncio.to_thread(requests.get, url)  # Make async request

        if response.status_code == 200:
            try:
                data = response.json()
                # Make sure that the response contains a 'video_url' key
                self.lecture_url = data.get("video_url", "")  # Save the lecture URL
                print("Lecture URL:", self.lecture_url)
                yield rx.redirect("/lectures")

            except ValueError:
                # If the response is not valid JSON, print it instead of showing an error to the user
                print("Error parsing lecture data:", response.text)

            except AttributeError:
                # This handles the case where `data` is a list instead of a dictionary
                print(f"Expected a dictionary with 'video_url', but got a list: {data}")

        else:
            # If the request failed, print the error code and response
            print(f"Error fetching lecture: {response.status_code}, Response: {response.text}")

    async def fetch_lectures(self):
        """Fetch all lectures for the given subject_id."""
        url = f"http://localhost:8000/get_lectures/{self.subject_id}"
        response = await asyncio.to_thread(requests.get, url)

        if response.status_code == 200:
            data = response.json()
            self.lecture_list = data.get("lectures", [])  # Ensure 'lectures' key exists
            print("Fetched Lectures:", self.lecture_list)
        else:
            print(f"Failed to fetch lectures. Status Code: {response.status_code}")
            self.lecture_list = []

    async def delete_lecture(self, lecture_name: str):
        """Delete a lecture by calling the backend API."""
        url = f"http://localhost:8000/delete_lecture/{self.subject_id}/{lecture_name}"
        response = await asyncio.to_thread(requests.delete, url)  # Async call

        if response.status_code == 200:
            self.lecture_list = [lec for lec in self.lecture_list if lec != lecture_name]
            
            print(f"Deleted: {lecture_name}")
            return rx.toast.info("Deleted File!", position="bottom-right")
        else:
            print(f"Failed to delete: {lecture_name}")

        
    async def fetch_materials(self):
        """Fetch all materials for the given subject_id and separate them into notes and textbooks."""
        
        # Clear existing lists
        self.note_list = []
        self.textbook_list = []

        url = f"http://127.0.0.1:8000/get_materials/{self.subject_id}"
        response = await asyncio.to_thread(requests.get, url)

        if response.status_code == 200:
            data = response.json()
            materials = data.get("materials", [])  # Assuming API returns a list of dicts
            
            # Separate materials based on type and only store 'name' in lists
            for material in materials:
                if material.get("type") == "Notes":
                    self.note_list.append(material.get("name"))  # Store only the 'name'
                elif material.get("type") == "Textbooks":
                    self.textbook_list.append(material.get("name"))  # Store only the 'name'

            # Debugging Output
            print("Fetched Notes:", self.note_list)
            print("Fetched Textbooks:", self.textbook_list)

        else:
            print(f"Failed to fetch materials: {response.status_code}")


    async def delete_material(self, material_name: str):
        """Delete a material by calling the backend API and refresh the page if successful."""
        url = f"http://localhost:8000/delete_material/{self.subject_id}/{material_name}"
        response = await asyncio.to_thread(requests.delete, url)  # Async request

        if response.status_code == 200:
            try:
                # Check if items in textbook_list are dictionaries before filtering
                if isinstance(self.textbook_list, list) and all(isinstance(mat, dict) for mat in self.textbook_list):
                    self.textbook_list = [mat for mat in self.textbook_list if mat.get("name") != material_name]
                
                if isinstance(self.note_list, list) and all(isinstance(mat, dict) for mat in self.note_list):
                    self.note_list = [mat for mat in self.note_list if mat.get("name") != material_name]

                print(f"Deleted: {material_name}")

                # Show success message
                rx.toast.success("Deleted successfully!", position="bottom-right")

                # Refresh the page automatically
                

            except Exception as e:
                print(f"Error updating material lists: {e}")  # Print instead of showing an error in the web UI

        else:
            print(f"Failed to delete: {material_name} - {response.status_code}")

    async def add_subject(self, form_data: dict):
        new_subjects = [id.strip() for id in form_data.get("subject_ids", "").split(",") if id.strip()]
        
        for subject in new_subjects:
            if subject not in self.subjects_taught_id:
                url = f"http://localhost:8000/add_subject/{subject}/{self.user_id}"
                response = await asyncio.to_thread(requests.put, url)  # POST to the API

                if response.status_code == 200:
                    self.fetch_professor_subjects()  # Re-fetch student list to reflect changes
                    yield rx.toast.success(f"Added subject: {student}", position="top-center")
                else:
                    print(f"Error adding subject {subject}: {response.text}")
            else:
                # Assuming you want to show an error toast if student is already in list
                yield rx.toast.error(f"Subject {subject} already exists.", position="top-center")

    async def remove_subject(self, subject:str):
            await self.get_subjects_id(subject)
            if self.subject_id in self.subjects_taught_id:
                url = f"http://localhost:8000/remove_subject/{self.subject_id}/{self.user_id}"
                response = await asyncio.to_thread(requests.put, url)

                if response.status_code == 200:
                    self.fetch_professor_subjects()
                    yield rx.toast.success(f"Removed subject: {subject}", position="top-center")
                else:
                    print(f"Error removing subject {subject}: {response.text}")
            else:
                yield rx.toast.error(f"Subject {subject} does not exist in your list.", position="top-center")

#===================================

    @rx.event
    async def handle_upload_lecture(self, files: list[rx.UploadFile]):
        """Handle file upload and send details to FastAPI."""
        if not files:
            return rx.toast.error("No file selected!", position="bottom-right")

        current_file = files[0]
        upload_data = await current_file.read() 

        # Save the file locally
        outfile = rx.get_upload_dir() / current_file.name 
        with outfile.open("wb") as file_object:
            file_object.write(upload_data)

        # Update state to show video
        self.video = current_file.name

        # Prepare form data
        form_data = {
            "lecture_id": str(uuid.uuid4()),  # UUID for uniqueness
            "lecture_name": current_file.name,
            "lecture_date": str(datetime.date.today()),
            "lecture_time": str(datetime.datetime.now().time()),
        }

        # Convert file to correct format for FastAPI
        files_payload = {
            "file": (current_file.name, BytesIO(upload_data), "video/mp4")
        }

        # Correct API URL
        url = f"http://127.0.0.1:8000/lectures/{self.subject_id}/upload/"

        try:
            response = requests.post(url, data=form_data, files=files_payload)

            if response.status_code == 200:
                return rx.toast.success("Upload Successful!", position="bottom-right")
            else:
                return rx.toast.error(f"Upload Failed! {response.text}", position="bottom-right")

        except Exception as e:
            return rx.toast.error(f"Error: {str(e)}", position="bottom-right")


    @rx.event
    async def handle_upload_material(self, files: list[rx.UploadFile]):
        """Handle file upload and send details to FastAPI."""
        if not files:
            return rx.toast.error("No file selected!", position="bottom-right")

        current_file = files[0]
        upload_data = await current_file.read()

        # Save the file locally
        outfile = rx.get_upload_dir() / current_file.name
        with outfile.open("wb") as file_object:
            file_object.write(upload_data)

        # Update state to show video
        self.video = current_file.name

        # Prepare form data with selected material type
        form_data = {
            "material_id": str(uuid.uuid4()),
            "material_name": current_file.name,
            "material_type": self.material_type, 
        }

        files_payload = {
            "file": (current_file.name, BytesIO(upload_data), "video/mp4")
        }

        url = f"http://127.0.0.1:8000/materials/{self.subject_id}/upload/"

        try:
            response = requests.post(url, data=form_data, files=files_payload)

            if response.status_code == 200:
                return rx.toast.success("Upload Successful!", position="bottom-right")
            else:
                return rx.toast.error(f"Upload Failed! {response.text}", position="bottom-right")

        except Exception as e:
            return rx.toast.error(f"Error: {str(e)}", position="bottom-right")


#=============================================================================================================================================
#without backend

def login() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.image(src="/hat_icon.png", width="130px", height="auto"),
            align_items="center",
            justify="center",
            margin_top="12px",
        ),
        rx.hstack(
            rx.heading("StudySphere", size="7", weight="bold"),
            align_items="center",
            justify="center",
        ),
        rx.vstack(
            rx.form(
                rx.vstack(
                    rx.text("ID / Username"),
                    rx.input(
                        name="user_id",  
                        border_radius="20px",
                        border="none",
                        color="black",
                        background_color="#EFFAFF",
                        width="20rem",
                        height="2.4rem",
                    ),
                    rx.text("Password"),
                    rx.input(
                        name="password",
                        type="password",
                        border_radius="20px",
                        border="none",
                        color="black",
                        background_color="#EFFAFF",
                        width="20rem",
                        height="2.4rem",
                    ),
                    rx.text("Register as", font_size="16px", color="white"),
                    rx.select(["Student", "Professor"], name="role", placeholder="Select Role",
                              border_radius="20px", border="none", color="black",
                              background_color="#EFFAFF", width="20rem", height="2.4rem"),

                    # Display error messages dynamically
                    rx.text(FormState.message, color="#A60A1B", font_size="16px", text_decoration="underline"), 
                        
                    rx.button(
                        "Log in",
                        type="submit",
                        bg="#346579",
                        size="3",
                        color="white",
                        border_radius="20px",
                        padding="0.5em 1em",
                        align_items="center",
                        margin_left="7.5rem",
                    ),
                    # rx.hstack(
                    #     rx.link("Forgot password?", href="/forgot-password", color="white", text_decoration="underline"),
                    #     margin_left="6rem"
                    # ), 
                    justify="center",
                ),
                on_submit=FormState.handle_submit,  # Calls backend to check credentials
                reset_on_submit=True,   
                width="320px"
            ),
            align_items="center",
            justify="center",
            margin_top="12px",
        ),
        # Link for users who don't have an account yet
        rx.vstack(
            rx.text("Don't have an account yet?"),
            rx.link("Sign up", href="/register", color="white", text_decoration="underline"),  # Redirect to register page
            align_items="center",
            justify="center",
            margin_top="12px",
        ),      
        bg="#598DA2",
        color="white", 
        padding="1em",
        min_height="100vh",
        width="100%",
        position="fixed",  
        top="0", 
        left="0",  
    )