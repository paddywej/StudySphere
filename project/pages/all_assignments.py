import reflex as rx
import uuid
import datetime
import asyncio
import requests
from typing import List, Dict, Set
from io import BytesIO
from datetime import datetime
from .assignment_details import AssignmentDetailsState

def fetch_assignments_data() -> List[Dict[str, List[Dict[str, str]]]]:
    """Simulate fetching multiple assignments data from a backend."""
    assignments_data = [
        {
            "assignment_name": "Math Assignment 1",
            "due_date": "2025-09-03",
            "students": [
                {"name": "66011211", "file": "Resume.pdf"},
                {"name": "66011217", "file": "Resume.pdf"},
            ]
        },
#         # {
#         #     "assignment_name": "Science Project 1",
#         #     "due_date": "2025-11-03",
#         #     "students": [
#         #         {"name": "Student A", "file": "Project1.pdf"},
#         #         {"name": "Student B", "file": "Project1.pdf"},
#         #     ]
#         # }
    ]
    return assignments_data

class AssignmentState(rx.State):
    assignment_to_delete: str = ""
    assignments: List[Dict[str, List[Dict[str, str]]]] = fetch_assignments_data()
    edited_assignment_name: str = ""
    edited_due_date: str = ""
    subject_id :str = ""

    delete_name:str =""
    message:str=""
    assignment_name:str = ""
    due_date:str = ""
    assignment_list: Dict[str, List[str]] = {}  
    
    async def get_subject_id(self):
        url = f"http://localhost:8000/user_session/subject"
        response = await asyncio.to_thread(requests.get, url) 

        if response.status_code == 200:
            self.subject_id = response.json()
            print(self.subject_id)
            yield AssignmentState.get_assignments()

        else:
            print("error get subject_id by usersession")

    @rx.event
    async def set_assignment(self, form_data: dict):
        try:
            if not form_data.get("assignment_name") or not form_data.get("due_date"):
                self.message = "Please fill all form fields."
                
            else:
                self.assignment_name = form_data["assignment_name"]
                self.due_date = form_data["due_date"]
                self.message = ""
                print(self.assignment_name,self.due_date)

        except Exception as e:
            print(f"Error: {str(e)}")

            
    @rx.event
    async def delete_assignment(self, form_data: dict):
        try:
            if not form_data.get("delete_name"):
                print("No delete assignment name enter")
                
            else:
                self.delete_name = form_data["delete_name"]
                print(self.delete_name)

        except Exception as e:
            print(f"Error: {str(e)}")
        
        url = f"http://localhost:8000/delete_assignment/{self.subject_id}/{self.delete_name}"

        try:
            response = await asyncio.to_thread(requests.delete, url)

            # Check the response from the server
            if response.status_code == 200:

                self.message = response.json().get("message", "Assignment deleted successfully")
                yield rx.toast.success(self.message, position="top-center")
            else:

                error_message = response.json().get("detail", "Failed to delete the assignment")
                self.message = error_message
                yield rx.toast.error(self.message, position="top-center")

        except Exception as e:
            self.message = f"Error occurred: {str(e)}"
            
    @rx.event
    async def add_assignment(self, files: list[rx.UploadFile]):
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
            "name": self.assignment_name,
            "due_date": formatted_due_date,
            "published_date": formatted_published_date,
            "status": "Open",
            "assessment_type": "Assignment",
            "file_name": file_name  # only storing the file name
        }

        # API URL
        url = "http://localhost:8000/add_assignment"

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

    # def set_edited_assignment_name(self, value: str):
    #     self.edited_assignment_name = value

    # def set_edited_due_date(self, value: str):
    #     self.edited_due_date = value

    # @rx.event
    # def edit_assignment(self,form_data: dict):
    #     print("edit submit form")
    #     yield rx.toast.info("handle on submit!!", position="top-center")
        # print(form_data)
        # """Update the assignment details in the state"""
        # for assignment in self.assignments:
        #     if assignment["assignment_name"] == self.edited_assignment_name:
        #         assignment["assignment_name"] = self.edited_assignment_name
        #         assignment["due_date"] = self.edited_due_date
        #         break
        
        # return rx.toast.success(
        #     f"Assignment updated to {self.edited_assignment_name}.",
        #     position="bottom-right",
        # )

    @rx.event
    async def submit_grades(self,form_data: dict):
        yield rx.toast.info("handle on submit!!", position="top-center")

        assignment_details_state = await self.get_state(AssignmentDetailsState)
        assignment_details_state.score = "56"
        
        # print(form_data)
        # """Handle grade submission."""
        # return rx.toast.success(
        #     "Grades submitted successfully.",
        #     position="bottom-right",
        # )

def create_assignment_container(assignment_title: str, due_date: str, student_data: List[Dict[str, str]], file_name: str = "No file uploaded") -> rx.Component:
    """Creates a container for each assignment with editable options."""
    return rx.box(
        rx.vstack(
            # Assignment Title and Due Date in one row
            
            #     # Edit Button that triggers a pop-up dialog
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
            #             rx.alert_dialog.title("Edit Assignment"),
            #             rx.alert_dialog.description("Modify the assignment details"),
            #             rx.form(
            #                 rx.vstack(
            #                     rx.input(
            #                         name="New_Assignment_Name",
            #                         placeholder="New Assignment Name",
            #                         on_change=AssignmentState.set_edited_assignment_name,
            #                         value=AssignmentState.edited_assignment_name,
            #                     ),
            #                     rx.input(
            #                         name="New_Due_Date",
            #                         placeholder="New Due Date",
            #                         type="date",
            #                         on_change=AssignmentState.set_edited_due_date,
            #                         value=AssignmentState.edited_due_date,
            #                     ),
            #                     rx.upload(
            #                         rx.vstack(
            #                             rx.button("Select File", color="white", border_radius="8px", padding="10px", 
            #                                     _hover={"background_color": "#598da2"}),
            #                             rx.text("Drag and drop files here or click to select files", color="gray"),
            #                         ),
            #                         id="upload1",
            #                         max_files=1,
            #                         accept=".pdf,.doc,.docx,.png,.py,.zip",
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
            #                 # spacing="4",
                            
            #                 ),
            #                 on_submit=AssignmentState.edit_assignment,
            #                 reset_on_submit=True,
            #             ),
            #             max_width="450px",
            #         ),
            #     ),
            #     width="100%",
            #     align_items="center",
            #     justify_content="space-between",
            # ),
            
            # rx.hstack(
            #     rx.text(item[0] ,font_size="20px", font_weight="bold", color="black"),  # assignment name
            #     rx.text("-", font_size="20px", font_weight="bold", color="black"),
            #     rx.text(item[1]["due_date"], font_size="20px", font_weight="bold", color="black"),
            # ),

            rx.flex(
                rx.foreach(
                    AssignmentState.assignment_list.items(),
                    lambda item: rx.box(
                        rx.vstack(
                            rx.hstack(
                                rx.text(item[0], font_size="20px", font_weight="bold", color="black"),  # assignment name
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
                    student_data,
                    lambda student: rx.hstack(
                        rx.box(rx.text(student["name"], font_size="16px"), width="33%", padding="10px", background_color="#effaff", color="black", border_radius="4px", height="50px", display="flex", align_items="center", justify_content="center"),
                        rx.box(rx.text(student["file"], font_size="16px"), width="33%", padding="10px", background_color="#effaff", color="black", border_radius="4px", height="50px", display="flex", align_items="center", justify_content="center"),
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
                            on_submit=AssignmentState.submit_grades,
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

def all_assignments() -> rx.Component:
    """Creates the main assignments page layout with scrollable containers."""
    return rx.box(
        rx.vstack(
            rx.text("Assignments", font_size="35px", font_weight="bold", color="#598da2", text_align="center"),
            
            # Buttons on a new line
            rx.hstack(

                rx.alert_dialog.root(
                    rx.alert_dialog.trigger(
                        rx.button("Add Assignments", bg="#6EA9C5", color="white", border_radius="8px", cursor="pointer"),
                    ),
                    rx.alert_dialog.content(
                        rx.alert_dialog.title("Add Assignment"),
                        rx.alert_dialog.description("Fill in the assignment details"),
                        rx.form(
                            rx.flex(
                                rx.input(
                                    placeholder="Assignment Name",
                                    name="assignment_name", 
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
                                rx.text(AssignmentState.message, color="red"),                   
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
                                            on_click=lambda: AssignmentState.add_assignment(rx.upload_files(upload_id="upload_add"))
                                        ),
                                    ),
                                    spacing="3",
                                    justify="end",
                                ),
                                direction="column",
                                spacing="4",
                            ),
                            on_submit=AssignmentState.set_assignment,
                            reset_on_submit=True,
                        ),
                        max_width="450px",
                    ),
                ),
                
                # Delete Assignment Dialog
                rx.alert_dialog.root(
                    rx.alert_dialog.trigger(
                        rx.button(
                            "Delete Assignments", 
                            bg="#6EA9C5", 
                            color="white", 
                            border_radius="8px", 
                            cursor="pointer"
                        ),
                    ),
                    rx.alert_dialog.content(
                        rx.alert_dialog.title("Delete Assignment"),
                        rx.alert_dialog.description("Enter the name of the assignment you want to delete."),
                        rx.form(
                            rx.flex(
                                rx.input(
                                    placeholder="Assignment Name",
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
                            on_submit=AssignmentState.delete_assignment,
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

            # Assignments list
            rx.vstack(
                rx.foreach(
                    AssignmentState.assignments,
                    lambda assignment: create_assignment_container(
                        assignment["assignment_name"],
                        assignment["due_date"],
                        assignment["students"],
                        assignment["file_name"],
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
        on_mount=AssignmentState.get_subject_id
    )
