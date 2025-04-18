import reflex as rx
import uuid
import datetime
import asyncio
import requests
from typing import List, Dict
from io import BytesIO
from datetime import datetime
from .quizdetailpage import QuizDetailsState

def fetch_quizzes_data() -> List[Dict[str, List[Dict[str, str]]]]:
    """Simulate fetching multiple quizzes data from a backend."""
    quizzes_data = [
        {
            "quiz_name": "Math Quiz 1", 
            "due_date": "2025-09-03",
            "students": [
                {"name": "Student 1", "file": "Quiz1.pdf"},
                {"name": "Student 2", "file": "Quiz1.pdf"},
            ]
        },
    ]
    return quizzes_data

class QuizState(rx.State):
    quiz_to_delete: str = ""
    quizzes: List[Dict[str, List[Dict[str, str]]]] = fetch_quizzes_data()
    edited_quiz_name: str = ""
    edited_due_date: str = ""
    subject_id: str = ""

    delete_name: str = ""
    message: str = ""
    quiz_name: str = ""
    due_date: str = ""
    quiz_list: Dict[str, List[str]] = {}
    submission_list: Dict[int, str] = {}
    name: str = ""
    assessment_id: str = ""

    async def get_subject_id(self):
        url = f"http://localhost:8000/user_session/subject"
        response = await asyncio.to_thread(requests.get, url)

        if response.status_code == 200:
            self.subject_id = response.json()
            print(self.subject_id)
            yield QuizState.get_quizs()
            yield QuizState.get_quiz_id()
        else:
            print("error get subject_id by usersession")

    @rx.event
    async def set_quiz(self, form_data: dict):
        try:
            if not form_data.get("quiz_name") or not form_data.get("due_date"):
                self.message = "Please fill all form fields."
            else:
                self.quiz_name = form_data["quiz_name"]
                self.due_date = form_data["due_date"]
                self.message = ""
                print(self.quiz_name, self.due_date)
        except Exception as e:
            print(f"Error: {str(e)}")

    @rx.event
    async def add_quiz(self, files: list[rx.UploadFile]):
        if not files:
            yield rx.toast.error("No file selected!", position="bottom-right")
            print("No file selected!")
            return

        current_file = files[0]
        file_name = current_file.name

        formatted_due_date = datetime.strptime(self.due_date, "%Y-%m-%d").strftime("%Y-%m-%dT%H:%M:%S.%f")
        formatted_published_date = datetime.today().strftime("%Y-%m-%dT%H:%M:%S.%f")

        form_data = {
            "assessment_id": str(uuid.uuid4()),
            "subject_id": self.subject_id,
            "name": self.quiz_name,
            "due_date": formatted_due_date,
            "published_date": formatted_published_date,
            "status": "Open",
            "assessment_type": "Quiz",
            "file_name": file_name
        }

        url = "http://localhost:8000/add_quiz"

        try:
            response = requests.post(url, data=form_data)

            if response.status_code == 200:
                yield rx.toast.success("Upload Successful!", position="bottom-right")
                print("Upload successful!")
            else:
                yield rx.toast.error(f"Upload Failed! {response.text}", position="bottom-right")
                print("Upload failed:", response.text)

        except Exception as e:
            yield rx.toast.error(f"Error: {str(e)}", position="bottom-right")
            print("Error during upload:", str(e))

    @rx.event
    async def get_quizs(self):
        try:
            url = f"http://localhost:8000/get_quizs/{self.subject_id}"
            response = await asyncio.to_thread(requests.get, url)

            if response.status_code == 200:
                raw_quizs = response.json().get("quizs", [])
                print(f"Quizzes retrieved: {raw_quizs}")

                formatted_quizs: Dict[str, List[str]] = {
                    quiz["name"]: [
                        datetime.strptime(quiz["due_date"], "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d"),
                        quiz["file_path"]
                    ]
                    for quiz in raw_quizs
                }

                self.quiz_list = formatted_quizs
                print(f"Formatted quizzes: {self.quiz_list}")

            else:
                error_message = response.json().get("detail", "Failed to retrieve quizzes")
                print(f"Quizzes retrieval error: {error_message}")

        except Exception as e:
            yield rx.toast.error(f"Error occurred: {str(e)}", position="top-center")

    @rx.event
    async def delete_quiz(self, form_data: dict):
        try:
            if not form_data.get("delete_name"):
                print("No delete quiz name enter")
            else:
                self.delete_name = form_data["delete_name"]
                print(self.delete_name)

        except Exception as e:
            print(f"Error: {str(e)}")
        
        url = f"http://localhost:8000/delete_quiz/{self.subject_id}/{self.delete_name}"

        try:
            response = await asyncio.to_thread(requests.delete, url)

            if response.status_code == 200:
                self.message = response.json().get("message", "Quiz deleted successfully")
                yield rx.toast.success(self.message, position="top-center")
            else:
                error_message = response.json().get("detail", "Failed to delete the quiz")
                self.message = error_message
                yield rx.toast.error(self.message, position="top-center")

        except Exception as e:
            self.message = f"Error occurred: {str(e)}"

    @rx.event
    async def get_submissions(self):
        try:
            url = f"http://localhost:8000/get_submissions/{self.assessment_id}"
            response = await asyncio.to_thread(requests.get, url)

            if response.status_code == 200:
                submissions = response.json().get("submissions", [])
                print(f"Retrieved submissions: {submissions}")

                formatted = {
                    sub["student_id"]: sub["file_path"] for sub in submissions
                }

                self.submission_list = formatted
                print(f"Formatted submission list: {self.submission_list}")

            else:
                error_message = response.json().get("detail", "Failed to retrieve submissions")
                print(f"Error: {error_message}")

        except Exception as e:
            yield rx.toast.error(f"Error occurred: {str(e)}", position="top-center")

    @rx.event
    async def get_quiz_id(self):
        try:
            first_key = next(iter(self.quiz_list))
            self.name = first_key
            print(f"Quiz name: {self.name}")

            url = f"http://localhost:8000/get_assessment_id/{self.subject_id}/{self.name}"
            
            response = await asyncio.to_thread(requests.get, url)

            if response.status_code == 200:
                self.assessment_id = response.json()["assessment_id"]
                print(f"Quiz assessment ID: {self.assessment_id}")
                yield QuizState.get_submissions()

            else:
                error_message = response.json().get("detail", "Quiz assessment ID not found")
                print(f"Error: {error_message}")

        except Exception as e:
            yield rx.toast.error(f"Error occurred: {str(e)}", position="top-center")

    @rx.event
    async def submit_grades(self, form_data: dict):
        yield rx.toast.success("Success", position="top-center")
        state = await self.get_state(QuizDetailsState)
        state.score = "40"
        yield

def create_quiz_container(quiz_title: str, due_date: str, student_data: List[Dict[str, str]], file_name: str = "No file uploaded") -> rx.Component:
    """Creates a container for each quiz with editable options."""
    return rx.box(
        rx.vstack(
            rx.flex(
                rx.foreach(
                    QuizState.quiz_list.items(),
                    lambda item: rx.box(
                        rx.vstack(
                            rx.hstack(
                                rx.text(item[0], font_size="20px", font_weight="bold", color="black"),
                                rx.text("-", font_size="20px", font_weight="bold", color="black"),
                                rx.text(item[1][0], font_size="20px", font_weight="bold", color="black"),
                            ),
                            rx.box(
                                rx.text(f"Professor's File: {item[0]}", font_size="16px", font_style="italic", color="gray"),
                                padding="10px",
                                background_color="#f0f0f0",
                                border_radius="6px",
                                margin_bottom="1rem",
                                margin_top="0.5rem",
                                width="20rem",
                                text_align="left",
                                cursor="pointer",
                                on_click=rx.download(url=rx.get_upload_url(item[1][1])),
                            ),
                        )
                    ),
                ),
                direction="column",
                spacing="4",
            ),
            
            rx.vstack(
                rx.foreach(
                    QuizState.submission_list.items(),
                    lambda student: rx.hstack(
                        rx.box(rx.text(student[0], font_size="16px"), width="33%", padding="10px", background_color="#effaff", color="black", border_radius="4px", height="50px", display="flex", align_items="center", justify_content="center"),
                        rx.box(rx.text(student[1], font_size="16px"), width="33%", padding="10px", background_color="#effaff", color="black", border_radius="4px", height="50px", display="flex", align_items="center", justify_content="center",on_click=rx.download(url=rx.get_upload_url(student[1][1]))),
                        rx.box(rx.input(name="score",placeholder="Enter score", width="100%", bg="white", border_radius="4px", color="black"), width="33%", padding="10px", background_color="#effaff", border_radius="4px", height="50px", display="flex", align_items="center", justify_content="center"),
                        spacing="2", align="center"
                    )
                ),
                spacing="2",
                align_items="center"
            ),
            
            rx.hstack(
                rx.spacer(),
                rx.alert_dialog.root(
                    rx.alert_dialog.trigger(
                        rx.button(
                            "Submit Grades",
                            bg="#6EA9C5",
                            color="white",
                            border_radius="8px",
                            cursor="pointer"
                        ),
                    ),
                    rx.alert_dialog.content(
                        rx.alert_dialog.title("Submit Grades"),
                        rx.alert_dialog.description("Are you sure you want to submit the grades?"),
                        rx.form(
                            rx.flex(
                                rx.alert_dialog.cancel(
                                    rx.button(
                                        "Cancel",
                                        variant="soft",
                                        color_scheme="gray",
                                    ),
                                ),
                                rx.alert_dialog.action(
                                    rx.button(
                                        "Submit",
                                        color_scheme="blue",
                                        type="submit"
                                    ),
                                ),
                            ),
                            margin_right="3rem",
                            spacing="3",
                            justify="end",
                            on_submit=QuizState.submit_grades,
                            reset_on_submit=True,
                        ),
                    ),
                ),
                width="100%",
                padding="10px",
                margin_top="1rem",
            ),
        ),
        height="450px",
        width="100%",
        background_color="#cfe2eb",
        border_radius="10px",
        padding="20px",
        overflow_y="scroll",
    )

def all_quizzes() -> rx.Component:
    """Creates the main quizzes page layout with scrollable containers."""
    return rx.box(
        rx.vstack(
            rx.text("Quizzes", font_size="35px", font_weight="bold", color="#598da2", text_align="center"),
            
            rx.hstack(
                rx.alert_dialog.root(
                    rx.alert_dialog.trigger(
                        rx.button("Add Quiz", bg="#6EA9C5", color="white", border_radius="8px", cursor="pointer"),
                    ),
                    rx.alert_dialog.content(
                        rx.alert_dialog.title("Add Quiz"),
                        rx.alert_dialog.description("Fill in the quiz details"),
                        rx.form(
                            rx.flex(
                                rx.input(
                                    placeholder="Quiz Name",
                                    name="quiz_name",
                                ),
                                rx.input(
                                    placeholder="Due Date",
                                    name="due_date",
                                    type="date",
                                ),
                                rx.upload(
                                    rx.vstack(
                                        rx.button("Select File", color="white", border_radius="8px", padding="10px",
                                                _hover={"background_color": "#598da2"}),
                                        rx.text("Drag and drop files here or click to select files", color="gray"),
                                    ),
                                    id="upload_add",
                                    max_files=1,
                                    accept=".pdf,.doc,.docx,.png,.py,.zip",
                                ),
                                rx.text(rx.selected_files("upload_add"), color="black"),
                                rx.text(QuizState.message, color="red"),
                                rx.flex(
                                    rx.alert_dialog.cancel(
                                        rx.button(
                                            "Cancel",
                                            variant="soft",
                                            color_scheme="gray",
                                        ),
                                    ),
                                    rx.alert_dialog.action(
                                        rx.button(
                                            "Submit", type="submit",
                                            on_click=lambda: QuizState.add_quiz(rx.upload_files(upload_id="upload_add"))
                                        ),
                                    ),
                                    spacing="3",
                                    justify="end",
                                ),
                                direction="column",
                                spacing="4",
                            ),
                            on_submit=QuizState.set_quiz,
                            reset_on_submit=True,
                        ),
                        max_width="450px",
                    ),
                ),
                
                rx.alert_dialog.root(
                    rx.alert_dialog.trigger(
                        rx.button(
                            "Delete Quiz",
                            bg="#6EA9C5",
                            color="white",
                            border_radius="8px",
                            cursor="pointer"
                        ),
                    ),
                    rx.alert_dialog.content(
                        rx.alert_dialog.title("Delete Quiz"),
                        rx.alert_dialog.description("Enter the name of the quiz you want to delete."),
                        rx.form(
                            rx.flex(
                                rx.input(
                                    placeholder="Quiz Name",
                                                                        name="delete_name"
                                ),
                                rx.flex(
                                    rx.alert_dialog.cancel(
                                        rx.button(
                                            "Cancel",
                                            variant="soft",
                                            color_scheme="gray",
                                        ),
                                    ),
                                    rx.alert_dialog.action(
                                        rx.button(
                                            "Delete",
                                            color_scheme="red",
                                            type="submit"
                                        ),
                                    ),
                                    spacing="3",
                                    justify="end",
                                ),
                            ),
                            spacing="4",
                            on_submit=QuizState.delete_quiz,
                            reset_on_submit=True,
                        ),
                        max_width="450px",
                    ),
                ),
                spacing="4",
                justify="center",
                width="100%",
                margin_top="1rem"
            ),

            rx.vstack(
                rx.foreach(
                    QuizState.quizzes,
                    lambda quiz: create_quiz_container(
                        quiz["quiz_name"],
                        quiz["due_date"],
                        quiz["students"],
                        quiz["file_name"],
                    ),
                ),
                spacing="6",
                align="center"
            ),
            spacing="6",
            align_items="center"
        ),
        width="100%",
        min_height="100vh",
        display="flex",
        justify_content="center",
        align_items="center",
        margin_left="4rem",
        padding_top="7rem",
        on_mount=QuizState.get_subject_id
    )
