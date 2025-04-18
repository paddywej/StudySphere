import reflex as rx
import uuid
import datetime
import asyncio
import requests
from typing import List, Dict, Set
from io import BytesIO
from datetime import datetime


class State(rx.State):

    assignment_list: Dict[str, List[str]] = {}
    assignment_name:str = ""
    subject_id:str = ""
    file_name:str = ""
    due_date:str = ""
    
    student_id:str = ""
    assessment_id:str = ""
    sub_file:str =""
    submission_id:str =""

    up_status=""

    @rx.event
    async def get_submission_file(self, submission_id: str):
        """Get the file path for the given submission ID."""
        url = f"http://127.0.0.1:8000/get_submission_file/{self.submission_id}"
        
        try:
            response = await asyncio.to_thread(requests.get, url)

            if response.status_code == 200:
                data = response.json()
                self.sub_file = data["file_path"]  # Store file path in sub_file
                print(f"File Path: {self.sub_file}")
            else:
                return rx.toast.error(f"Failed to fetch file path: {response.text}", position="bottom-right")
        
        except Exception as e:
            return rx.toast.error(f"Error: {str(e)}", position="bottom-right")

    
    async def get_subject_id(self):
        url = f"http://localhost:8000/user_session/subject"
        response = await asyncio.to_thread(requests.get, url) 

        if response.status_code == 200:
            self.subject_id = response.json()
            print(self.subject_id)
            yield State.get_assignments()
            yield State.get_student_id()
            yield State.fetch_assessment_id()

        else:
            print("error get subject_id by usersession")

    async def get_student_id(self):
        url = f"http://localhost:8000/user_session/student"
        response = await asyncio.to_thread(requests.get, url) 

        if response.status_code == 200:
            self.student_id = response.json()
            print(self.student_id)
            yield State.get_assignments()

        else:
            print("error get srudent_id by usersession")

    @rx.event
    async def get_assignments(self):
        try:
            url = f"http://localhost:8000/get_assignments/{self.subject_id}"
            response = await asyncio.to_thread(requests.get, url)

            if response.status_code == 200:
                raw_assignments = response.json().get("assignments", [])
                print(f"Assignments retrieved: {raw_assignments}")

                # Properly ordered: due_date first, then file_path
                formatted_assignments: Dict[str, List[str]] = {
                    assignment["name"]: [
                        datetime.strptime(assignment["due_date"], "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d"),
                        assignment["file_path"]
                    ]
                    for assignment in raw_assignments
                }

                self.assignment_list = formatted_assignments
                print(f"Formatted assignments: {self.assignment_list}")

            else:
                error_message = response.json().get("detail", "Failed to retrieve assignments")
                print(f"Assignments retrieval error: {error_message}")

        except Exception as e:
            yield rx.toast.error(f"Error occurred: {str(e)}", position="top-center")

    @rx.event
    async def fetch_assessment_id(self):
        """Fetch the assessment_id based on subject_id and assessment_name."""
        url = f"http://localhost:8000/get_assessment_id/{self.subject_id}/{self.assignment_name}"
        try:
            response = await asyncio.to_thread(requests.get, url)

            if response.status_code == 200:
                data = response.json()
                self.assessment_id = data["assessment_id"]
                print(f"Fetched assessment_id: {self.assessment_id}")
            else:
                print(f"Failed to fetch assessment_id: {response.text}")
        except Exception as e:
            yield rx.toast.error(f"Error: {str(e)}", position="top-center")


    @rx.event
    async def get_detail(self, name: str):
        self.assignment_name = name
        print(f"subject_id: {self.subject_id}, assignment_name: {self.assignment_name}")
        yield State.get_file()

    def calculate_status(self):
        try:
            # Try parsing with the full datetime format (including time)
            try:
                due_date = datetime.strptime(self.due_date, "%Y-%m-%dT%H:%M:%S")
            except ValueError:
                # If parsing fails, try parsing just the date (no time component)
                due_date = datetime.strptime(self.due_date, "%Y-%m-%d")
            
            current_date = datetime.utcnow()

            # Compare dates to determine the status
            if due_date < current_date:
                status = "Late"
            else:
                status = "Submitted"
            
            return status

        except Exception as e:
            # Handle any other errors
            return f"Error calculating status: {str(e)}"

    @rx.event
    async def get_file(self):
        url = f"http://localhost:8000/get_file_ass/{self.subject_id}/{self.assignment_name}"
        try:
            response = await asyncio.to_thread(requests.get, url)

            if response.status_code == 200:
                data = response.json()
                self.file_name = data["file_path"]
                self.due_date = data["due_date"]
                print(f"Fetched file path: {self.file_name}")
                print(f"Fetched due date: {self.due_date}")

                yield rx.redirect("/assignment_details")
            else:
                print(f"Failed to get assignment info: {response.text}")
        except Exception as e:
            yield rx.toast.error(f"Error: {str(e)}", position="top-center")


    @rx.event
    async def handle_upload_submit(self, files: list[rx.UploadFile]):
        if not files:
            yield rx.toast.error("No file selected!", position="bottom-right")
            print("No file selected!")
            return

        # Get only the file name
        current_file = files[0]
        file_name = current_file.name
        print("file path:", file_name)

        status = self.calculate_status()

        formatted_submittion_date = datetime.today().strftime("%Y-%m-%dT%H:%M:%S.%f")

        # Prepare form data for API request
        form_data = {
            "submission_id": str(uuid.uuid4()),
            "assessment_id": self.assessment_id,  # Ensure this is set dynamically
            "student_id": self.student_id,
            "submitted_time": formatted_submittion_date,
            "last_modified": formatted_submittion_date,
            "status": status, 
            "file_path": file_name  # Status based on due date comparison
        }

        # API URL
        url = "http://127.0.0.1:8000/submit_assignment/"

        try:
            # Send only form data, no files
            response = requests.post(url, data=form_data)

            if response.status_code == 200:
                yield rx.toast.success("Upload Successful!", position="bottom-right")
                print("Upload successful!")
                self.up_status=""
                # yield State.get_submission_file()
                
            else:
                yield rx.toast.error(f"Upload Failed! {response.text}", position="bottom-right")
                print("Upload failed:", response.text)

        except Exception as e:
            yield rx.toast.error(f"Error: {str(e)}", position="bottom-right")
            print("Error during upload:", str(e))

def assignment_item(assignment_name: str, due_date: str, status: str) -> rx.Component:
    # Background color based on status
    status_colors = {
        "new": "#EFFAFF",   # Light blue for new
        "done": "#D3F8E2",   # Light blue for done
    }
    
    return rx.button(
                rx.vstack(
                    rx.text(assignment_name, size="3", weight="bold"),
                    rx.text(f"Due: {due_date}", size="2"),
                    rx.text(f"Status: {status.capitalize()}", size="2", color="gray"),
                    spacing="1",
                    margin_left="-11rem",
                    align_items="flex-start",
                ),
                bg=status_colors.get(status, "#EFFAFF"),
                color="black",
                padding="1em",
                border_radius="14px",
                width="100%",
                height="6rem",
                shadow="md",
                _hover={"bg": "#BFD9E5"},
                on_click=State.get_detail(assignment_name),  # Define the click event handler
)


def assignments() -> rx.Component:
    # Sample list of assignments with unique IDs
    # assignments_list = [
    #     {"id": "math_hw_1", "name": "Math Homework 1", "due_date": "2025-03-29", "status": ""},
    #     {"id": "science_proj", "name": "Science Project", "due_date": "2025-04-02", "status": ""},
    #     {"id": "history_essay", "name": "History Essay", "due_date": "2025-03-25", "status": "done"},
    # ]
    
    return rx.container(
        rx.hstack(
            # Unfinished Assignments
            rx.box(
                rx.vstack(
                    rx.text("Assignments", size="4", weight="bold"),
                    rx.foreach(
                        State.assignment_list.items(),
                        lambda item: assignment_item(item[0],item[1][0],"New"),
                    ),

                    spacing="2",
                    width="100%",
                ),
                width="45%",
                height="500px",
                bg="#D0E2EB",
                color="black",
                padding="1em",
                overflow="auto",
                border_radius="25px",
                margin_right="2rem",
            ),
            # # Done Assignments
            # rx.box(
            #     rx.vstack(
            #         rx.text("Done Assignments", size="4", weight="bold"),
            #         # *[assignment_item(a["id"], a["name"], a["due_date"], a["status"]) for a in assignments_list if a["status"] == "done"],
            #         spacing="2",
            #         width="100%",
            #     ),
            #     width="45%",
            #     height="500px",
            #     bg="#D0E2EB",
            #     color="black",
            #     padding="1em",
            #     overflow="auto",
            #     border_radius="25px",
            # ),
            spacing="4",
            justify="center",
            width="100%",
        ),
        width="100%",
        padding="2em",
        padding_top="7rem",
        margin_left="7rem",
        min_height="100vh",
        bg="white",
        on_mount=State.get_subject_id
    )