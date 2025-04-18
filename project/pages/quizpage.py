import reflex as rx
import uuid
import datetime
import asyncio
import requests
from typing import List, Dict, Set
from io import BytesIO
from datetime import datetime


class State(rx.State):

    quiz_list: Dict[str, List[str]] = {}
    quiz_name:str = ""
    subject_id:str = ""
    file_name:str = "test.pdf"
    due_date:str = ""
    
    student_id:str = ""
    assessment_id:str = ""
    sub_file:str =""
    submission_id:str =""

    up_status=""

    async def get_subject_id(self):
        url = f"http://localhost:8000/user_session/subject"
        response = await asyncio.to_thread(requests.get, url) 

        if response.status_code == 200:
            self.subject_id = response.json()
            print(self.subject_id)
            yield State.get_quizs()
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
            yield State.get_quizs()

        else:
            print("error get srudent_id by usersession")

    @rx.event
    async def get_quizs(self):
        try:
            url = f"http://localhost:8000/get_quizs/{self.subject_id}"
            response = await asyncio.to_thread(requests.get, url)

            if response.status_code == 200:
                raw_quizs = response.json().get("quizs", [])
                print(f"Quizs retrieved: {raw_quizs}")

                # Properly ordered: due_date first, then file_path
                formatted_quizs: Dict[str, List[str]] = {
                    quiz["name"]: [
                        datetime.strptime(quiz["due_date"], "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d"),
                        quiz["file_path"]
                    ]
                    for quiz in raw_quizs
                }

                self.quiz_list = formatted_quizs
                print(f"Formatted quizs: {self.quiz_list}")

            else:
                error_message = response.json().get("detail", "Failed to retrieve quizs")
                print(f"Quizs retrieval error: {error_message}")

        except Exception as e:
            yield rx.toast.error(f"Error occurred: {str(e)}", position="top-center")


    # @rx.event
    # async def get_quizs(self):
    #     try:
    #         url = f"http://localhost:8000/get_quizs/{self.subject_id}"
    #         response = await asyncio.to_thread(requests.get, url)

    #         if response.status_code == 200:
    #             raw_quizzes = response.json().get("quizzes", [])
    #             print(f"quizzes retrieved: {raw_quizzes}")

    #             # Properly ordered: due_date first, then file_path
    #             formatted_quizs: Dict[str, List[str]] = {
    #                 quiz["name"]: [
    #                     datetime.strptime(quiz["due_date"], "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d"),
    #                     quiz["file_path"]
    #                 ]
    #                 for quiz in raw_quizzes
    #             }

    #             self.quiz_list = formatted_quizs
    #             print(f"Formatted quizzes: {self.quiz_list}")

    #         else:
    #             error_message = response.json().get("detail", "Failed to retrieve quizzes")
    #             print(f"Quizzes retrieval error: {error_message}")

    #     except Exception as e:
    #         yield rx.toast.error(f"Error occurred: {str(e)}", position="top-center")

    @rx.event
    async def fetch_assessment_id(self):
        """Fetch the assessment_id based on subject_id and assessment_name."""
        url = f"http://localhost:8000/get_assessment_id/{self.subject_id}/{self.quiz_name}"
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
        self.quiz_name = name
        print(f"subject_id: {self.subject_id}, quiz_name: {self.quiz_name}")
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
        url = f"http://localhost:8000/get_file_ass/{self.subject_id}/{self.quiz_name}"
        try:
            response = await asyncio.to_thread(requests.get, url)

            if response.status_code == 200:
                data = response.json()
                self.file_name = data["file_path"]
                self.due_date = data["due_date"]
                print(f"Fetched file path: {self.file_name}")
                print(f"Fetched due date: {self.due_date}")

                yield rx.redirect("/quiz_details")
            else:
                print(f"Failed to get quiz info: {response.text}")
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
        url = "http://127.0.0.1:8000/submit_quiz/"

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


def quiz_item(name: str, quiz_date: str) -> rx.Component:
    # status_colors = {
    #     "upcoming": "#EFFAFF",
    #     "completed": "#D3F8E2",
    # }
   
    return rx.link(
        rx.box(
            rx.vstack(
                rx.text(f"{name}", size="3", weight="bold"),
                rx.text(f"Date: {quiz_date}", size="2"),
                spacing="1",
            ),
            bg="#EFFAFF",
            color="black",
            padding="1em",
            border_radius="8px",
            width="100%",
            margin_bottom="1em",
            shadow="md",
            _hover={"bg": "#BFD9E5"},
        ),
        href=f"/quiz_details",
        width="100%",
        text_decoration="none",
    )

def quiz() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.box(
                rx.vstack(
                    rx.text("Quiz", size="4", weight="bold"),
                    rx.foreach(
                        State.quiz_list.items(),
                        lambda item: quiz_item(item[0],item[1][0]),
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
            # rx.box(
            #     rx.vstack(
            #         rx.text("Completed Exams", size="4", weight="bold"),
            #         *[exam_item(e["id"], e["name"], e["exam_date"], e["status"], e["exam_time"]) for e in exam_data_list if e["status"] == "completed"],
            #         spacing="1",
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