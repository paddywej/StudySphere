import reflex as rx
import uuid
import datetime
import asyncio
import requests
from typing import List, Dict
from io import BytesIO
from datetime import datetime

def fetch_exams_data() -> List[Dict[str, List[Dict[str, str]]]]:
    """Simulate fetching multiple exams data from a backend."""
    exams_data = [
        {
            "exam_name": "Math Exam 1",
            "due_date": "2025-09-03",
            "students": [
                {"name": "Student 1", "file": "Exam1.pdf"},
                {"name": "Student 2", "file": "Exam1.pdf"},
            ]
        },
    ]
    return exams_data

class ExamState(rx.State):
    exam_to_delete: str = ""
    exams: List[Dict[str, List[Dict[str, str]]]] = fetch_exams_data()
    edited_exam_name: str = ""
    edited_due_date: str = ""
    subject_id :str = ""

    delete_name:str =""
    message:str=""
    exam_name:str = ""
    due_date:str = ""
    exam_list: Dict[str, List[str]] = {}  
    submission_list: Dict[int, str] = {}
    name:str =""
    assessment_id:str =""

    
    async def get_subject_id(self):
        url = f"http://localhost:8000/user_session/subject"
        response = await asyncio.to_thread(requests.get, url) 

        if response.status_code == 200:
            self.subject_id = response.json()
            print(self.subject_id)
            yield ExamState.get_exam()
            yield ExamState.get_exam_id()
        else:
            print("error get subject_id by usersession")

    @rx.event
    async def set_exam(self, form_data: dict,):
        try:
            if not form_data.get("exam_name") or not form_data.get("due_date"):
                self.message = "Please fill all form fields."
                
            else:
                self.exam_name = form_data["exam_name"]
                self.due_date = form_data["due_date"]
                self.message = ""
                print(self.exam_name,self.due_date)

        except Exception as e:
            print(f"Error: {str(e)}")

    @rx.event
    async def add_exam(self, files: list[rx.UploadFile]):
        if not files:
            yield rx.toast.error("No file selected!", position="bottom-right")
            print("No file selected!")
            return

        # Get only the file name
        current_file = files[0]
        file_name = current_file.name

        # Format dates correctly
        formatted_due_date = datetime.strptime(self.due_date, "%Y-%m-%d").strftime("%Y-%m-%dT%H:%M:%S.%f")
        formatted_published_date = datetime.today().strftime("%Y-%m-%dT%H:%M:%S.%f")

        # Prepare form data (no file upload)
        form_data = {
            "assessment_id": str(uuid.uuid4()),
            "subject_id": self.subject_id,
            "name": self.exam_name,
            "due_date": formatted_due_date,
            "published_date": formatted_published_date,
            "status": "Open",
            "assessment_type": "Exam",
            "file_name": file_name  # only storing the file name
        }

        # API URL
        url = "http://localhost:8000/add_exam"

        try:
            # Send only form data, no files
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
    async def get_exam(self):
        try:
            url = f"http://localhost:8000/get_exams/{self.subject_id}"
            response = await asyncio.to_thread(requests.get, url)

            if response.status_code == 200:
                raw_exams = response.json().get("exams", [])
                print(f"Exams retrieved: {raw_exams}")

                # Properly ordered: due_date first, then file_path
                formatted_exams: Dict[str, List[str]] = {
                    exam["name"]: [
                        datetime.strptime(exam["due_date"], "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d"),
                        exam["file_path"]
                    ]
                    for exam in raw_exams
                }

                self.exam_list = formatted_exams
                print(f"Formatted exams: {self.exam_list}")

            else:
                error_message = response.json().get("detail", "Failed to retrieve exams")
                print(f"Exams retrieval error: {error_message}")

        except Exception as e:
            yield rx.toast.error(f"Error occurred: {str(e)}", position="top-center")



    @rx.event
    async def delete_exam(self, form_data: dict):

        try:
            if not form_data.get("delete_name"):
                print("No delete exam name enter")
                
            else:
                self.delete_name = form_data["delete_name"]
                print(self.delete_name)

        except Exception as e:
            print(f"Error: {str(e)}")
        
        url = f"http://localhost:8000/delete_exam/{self.subject_id}/{self.delete_name}"

        try:
            response = await asyncio.to_thread(requests.delete, url)

            # Check the response from the server
            if response.status_code == 200:

                self.message = response.json().get("message", "Exam deleted successfully")
                yield rx.toast.success(self.message, position="top-center")
            else:

                error_message = response.json().get("detail", "Failed to delete the exam")
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

                # Format as {student_id: file_path}
                formatted = {
                    sub["student_id"]: sub["file_path"] for sub in submissions
                }

                # Store the dict in state
                self.submission_list = formatted
                print(f"Formatted submission list: {self.submission_list}")

            else:
                error_message = response.json().get("detail", "Failed to retrieve submissions")
                print(f"Error: {error_message}")

        except Exception as e:
            yield rx.toast.error(f"Error occurred: {str(e)}", position="top-center")

    @rx.event
    async def get_exam_id(self):
        try:
            # Retrieve the first key from the dictionary
            first_key = next(iter(self.exam_list))
            self.name = first_key
            print(f"Exam name: {self.name}")

            # Construct the URL for the backend API
            url = f"http://localhost:8000/get_assessment_id/{self.subject_id}/{self.name}"
            
            # Make the API call using requests asynchronously
            response = await asyncio.to_thread(requests.get, url)

            if response.status_code == 200:
                # Print the assessment ID if found
                self.assessment_id = response.json()["assessment_id"]
                print(f"Exam assessment ID: {self.assessment_id}")
                yield ExamState.get_submissions()

            else:
                # Handle error if no assessment ID is found
                error_message = response.json().get("detail", "Exam assessment ID not found")
                print(f"Error: {error_message}")

        except Exception as e:
            # Handle any other exceptions during the process
            yield rx.toast.error(f"Error occurred: {str(e)}", position="top-center")

    # def set_edited_exam_name(self, value: str):
    #     self.edited_exam_name = value

    # def set_edited_due_date(self, value: str):
    #     self.edited_due_date = value

    # @rx.event
    # def edit_exam(self, form_data: dict):
    #     print("edit submit form")
    #     yield rx.toast.info("handle on submit!!", position="top-center")

    @rx.event
    def submit_grades(self, form_data: dict):
        yield rx.toast.success("Success", position="top-center")

def create_exam_container(exam_title: str, due_date: str, student_data: List[Dict[str, str]], file_name: str = "No file uploaded") -> rx.Component:
    """Creates a container for each exam with editable options."""
    return rx.box(
        rx.vstack(

            #     rx.alert_dialog.root(
            #         rx.alert_dialog.trigger(
            #             rx.button(
            #                 "Edit", 
            #                 bg="#6EA9C5", 
            #                 color="white", 
            #                 border_radius="8px", 
            #                 cursor="pointer"
            #             ),
            #         ),
            #         rx.alert_dialog.content(
            #             rx.alert_dialog.title("Edit Exam"),
            #             rx.alert_dialog.description("Modify the exam details"),
            #             rx.form(
            #                 rx.vstack(
            #                     rx.input(
            #                         name="New_Exam_Name",
            #                         placeholder="New Exam Name",
            #                     ),
            #                     rx.input(
            #                         name="New_Due_Date",
            #                         placeholder="New Due Date",
            #                         type="date",
            #                     ),
            #                     rx.input(
            #                         type="file",
            #                         name="edit_file",
            #                         accept=".pdf,.doc,.docx,.png,.py,.zip"
            #                     ),
            #                     rx.flex(
            #                         rx.alert_dialog.cancel(
            #                             rx.button(
            #                                 "Cancel",
            #                                 variant="soft",
            #                                 color_scheme="gray",
            #                             ),
            #                         ),
            #                         rx.alert_dialog.action(
            #                             rx.button(
            #                                 "Save Changes",
            #                                 color_scheme="blue",
            #                                 type="submit"
            #                             ),
            #                             justify="space-between",
            #                         ),
            #                         spacing="3",
            #                         justify="end",
            #                     ),
            #                 ),
            #                 on_submit=ExamState.edit_exam,
            #                 reset_on_submit=True,
            #             ),
            #             max_width="450px",
            #         ),
            #     ),
            #     width="100%",
            #     align_items="center",
            #     justify_content="space-between",
            # ),
            
            rx.flex(
                rx.foreach(
                    ExamState.exam_list.items(),
                    lambda item: rx.box(
                        rx.vstack(
                            rx.hstack(
                                rx.text(item[0], font_size="20px", font_weight="bold", color="black"),  
                                rx.text("-", font_size="20px", font_weight="bold", color="black"),
                                rx.text(item[1][0], font_size="20px", font_weight="bold", color="black"),  # due date
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
                                on_click=rx.download(url=rx.get_upload_url(item[1][1])),  # file path
                            ),
                        )
                    ),
                ),
                direction="column",
                spacing="4",
            ),
            
            # Student List
            rx.vstack(
                rx.foreach(
                    ExamState.submission_list.items(),
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
            
            # Submit Grades button at the bottom right
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
                            on_submit=ExamState.submit_grades,
                            reset_on_submit=True,
                        ),
                    ),
                ),
                width="10rem",
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

def all_exams() -> rx.Component:
    """Creates the main exams page layout with scrollable containers."""
    return rx.box(
        rx.vstack(
            rx.text("Exams", font_size="35px", font_weight="bold", color="#598da2", text_align="center"),
            
            rx.hstack(
                rx.alert_dialog.root(
                    rx.alert_dialog.trigger(
                        rx.button("Add Exam", bg="#6EA9C5", color="white", border_radius="8px", cursor="pointer"),
                    ),
                    rx.alert_dialog.content(
                        rx.alert_dialog.title("Add Exam"),
                        rx.alert_dialog.description("Fill in the exam details"),
                        rx.form(
                            rx.flex(
                                rx.input(
                                    placeholder="Exam Name",
                                    name="exam_name", 
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
                                rx.text(ExamState.message, color="red"),                   
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
                                            on_click=lambda: ExamState.add_exam(rx.upload_files(upload_id="upload_add"))
                                        ),
                                    ),
                                    spacing="3",
                                    justify="end",
                                ),
                                direction="column",
                                spacing="4",
                            ),
                            on_submit=ExamState.set_exam,
                            reset_on_submit=True,
                        ),
                        max_width="450px",
                    ),
                ),
                
                rx.alert_dialog.root(
                    rx.alert_dialog.trigger(
                        rx.button(
                            "Delete Exams", 
                            bg="#6EA9C5", 
                            color="white", 
                            border_radius="8px", 
                            cursor="pointer"
                        ),
                    ),
                    rx.alert_dialog.content(
                        rx.alert_dialog.title("Delete Exam"),
                        rx.alert_dialog.description("Enter the name of the exam you want to delete."),
                        rx.form(
                            rx.flex(
                                rx.input(
                                    placeholder="Exam Name",
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
                            on_submit=ExamState.delete_exam,
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

            # Exams list
            rx.vstack(
                rx.foreach(
                    ExamState.exams,
                    lambda exam: create_exam_container(
                        exam["exam_name"],
                        exam["due_date"],
                        exam["students"],
                        exam["file_name"],
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
        on_mount=ExamState.get_subject_id
    )