import reflex as rx
import uuid
import datetime
import asyncio
import requests
from typing import List, Dict, Set
from io import BytesIO
from datetime import datetime
from project.pages.assignments_page import State


class AssignmentDetailsState(rx.State):
    """Manages assignment-related state."""
    user_file: str = ""  # Stores uploaded file
    score: str = "Not Graded"  # Stores the student's score
    file_sub:str =""
    is_unsubmit: bool = None
    # file_sub="66011217_Shisa.pdf"

    # submit_file_path:str = ""
    # submit_file_name:str = ""
    
    # def upload_file(self, file_name: str):
    #     """Handles file upload."""
    #     self.user_file = file_name

    # def submit(self):
    #     """Handles submission."""
    #     if self.user_file:
    #         rx.window_alert(f"Successfully submitted: {self.user_file}")

    # def unsubmit(self):
    #     """Handles unsubmission."""
    #     if self.user_file:
    #         rx.window_alert(f"Unsubmitted: {self.user_file}")
    #         self.user_file = ""  # Reset file after unsubmission

    # def grade_assignment(self, new_score: str):
    #     """Handles grading an assignment."""
    #     self.score = new_score
    #     rx.window_alert(f"Assignment graded: {self.score}")

    # async def handle_upload(self, files: list[rx.UploadFile]):
    #     """Handle the upload of file(s)."""
    #     for file in files:
    #         upload_data = await file.read()
    #         outfile = rx.get_upload_dir() / file.filename
    #         # Save the file
    #         with outfile.open("wb") as file_object:
    #             file_object.write(upload_data)
    #         self.user_file = file.filename

    def change(self):
        self.file_sub="Resume.pdf"
        self.is_unsubmit = True
        yield

    def handle_unsubmit(self):
        self.is_unsubmit = False
        yield

def create_container(title: str, item: str, extra_content: rx.Component = None) -> rx.Component:
    """Creates a scrollable container for assignment-related content."""
    return rx.box(
        rx.box(
            rx.text(title, font_size="18px", font_weight="bold", color="#1d2023"),
            position="relative",
            width="100%",
        ),
        # Add extra content like the score at the top-right if provided
        extra_content if extra_content else rx.box(),
        rx.vstack(
            item, padding="8px", background_color="#f8f8f8", border_radius="5px",margin_right="1rem",
            height="2rem"
        ),
        height="450px",
        width="450px",
        background_color="#d0e2eb",
        border_radius="25px",
        padding="10px",
        overflow_y="scroll",
        position="relative",  # Required for absolute positioning inside
        cursor="pointer",
        on_click=rx.download(url=rx.get_upload_url(item)),
    )


def assignment_details() -> rx.Component:
    """Dynamic assignment page with containers side by side and buttons below."""
    return rx.box(
        rx.vstack(
            rx.text("Assignment Details", font_size="24px", font_weight="bold", color="#598da2"),

            rx.hstack(
                rx.text(State.assignment_name, font_size="24px", color="#598da2",font_weight="bold"),

            ),
            

            # HStack for side-by-side containers
            rx.hstack(
                # Assignment File Container
                rx.vstack(
                    rx.box(
                        "Assignment File",
                        rx.vstack(
                            rx.button(
                            State.file_name,
                            margin_top="5px",
                            padding="12px", 
                            color="black",
                            background_color="#f8f8f8", 
                            border_radius="5px",
                            cursor="pointer",
                            on_click=rx.download(url=rx.get_upload_url(State.file_name)), 
                            ),
                        ),
                        padding_top="1rem",
                        height="450px",
                        width="450px",
                        background_color="#d0e2eb",
                        border_radius="25px",
                        padding="10px",
                        overflow_y="scroll",
                        font_weight="bold",
                        position="relative",
                    ),
                ),
    
                # Your Work Container with Score at the Top Right
                rx.vstack(
                    rx.flex(
                        rx.flex(
                            rx.text.strong("Your Work"),
                            rx.text.strong("Score", margin_right="3rem"),
                            justify="between"
                        ),
                        rx.flex(
                            rx.cond(
                                AssignmentDetailsState.is_unsubmit,
                                rx.fragment(
                                    rx.box(rx.icon("x", color="red"), on_click=AssignmentDetailsState.handle_unsubmit),
                                    rx.box(rx.text(AssignmentDetailsState.file_sub), background_color="#f8f8f8", width="65%"),
                                    rx.box(rx.text(AssignmentDetailsState.score), margin_left="1.5rem"),
                                ),
                                rx.box()
                            ),
                            margin_top="1rem",
                            width="100%",
                        ),
                        width="400px",
                        height="400px",
                        margin_top="8rem",
                        border_radius="20px",
                        padding="10px",
                        background_color="#d0e2eb",
                        direction="column"
                    ),
                    # create_container(
                    #     "Your Work", 
                    #     # State.sub_file,
                    #     (AssignmentDetailsState.file_sub),
                    #     extra_content=rx.box(
                    #         rx.text("Score:", font_size="16px", font_weight="bold", color="#1d2023"),
                    #         rx.text(
                    #             AssignmentDetailsState.score,  # Score updates dynamically
                    #             font_size="16px",
                    #             padding="5px 10px",
                    #             background_color="#d0e2eb",
                    #             border_radius="5px",
                    #             text_align="center",
                    #         ),
                            
                    #         position="absolute",
                    #         top="10px", 
                    #         right="10px",
                    #         background_color="#d0e2eb",
                    #         border_radius="8px",
                    #         padding="5px",
                    #         color="#1d2023"
                    #     )
                    # ),
                    rx.vstack(
                        rx.dialog.root(
                            rx.dialog.trigger(
                                rx.button(
                                    "Upload your file", 
                                    padding="10px", 
                                    background_color="#6EA9C5",
                                    color="white", 
                                    width="180px", 
                                    height="45px", 
                                    border_radius="10px",
                                    weight="bold",
                                ),
                            ),
                            rx.dialog.content(
                                rx.dialog.title("Upload Assignment"),
                                rx.dialog.description("Select your assignment file"),
                                rx.upload(
                                    rx.vstack(
                                        rx.button(
                                            "Select File",
                                        ),
                                        rx.text(
                                            "Drag and drop files here or click to select files"
                                        ),
                                        align="center",  # Center align the vstack contents
                                        spacing="4",
                                    ),
                                    id="upload_add",
                                    accept={
                                        "application/pdf": [".pdf"],
                                        "image/png": [".png"],
                                        "image/jpeg": [".jpg", ".jpeg"]
                                    },
                                    max_files=1,
                                    border="1px dotted rgb(107,99,246)",
                                    padding="5em",
                                ),
                                rx.text(rx.selected_files("upload_add"), color="black"),   
                                
                                rx.flex(
                                    rx.dialog.close(
                                        rx.button(
                                            "Cancel",
                                            variant="soft",
                                            color_scheme="gray",
                                        ),
                                    ),
                                    rx.dialog.close(
                                        rx.button("Submit",
                                        # on_click=State.handle_upload_submit(rx.upload_files(upload_id="upload_add"))),
                                        on_click=AssignmentDetailsState.change
                                    ),
                                    spacing="3",
                                    justify="end",
                                ),
                                max_width="450px",
                                align="center",  # Center align the dialog content
                            ),
                        ),
                        # rx.button(
                        #     "Submit", padding="10px", background_color="#6EA9C5",
                        #     color="white", width="180px", height="45px", border_radius="10px",
                        #     weight="bold", on_click=lambda: AssignmentDetailsState.submit()
                        # ),
                        # rx.button(
                        #     "Unsubmit", padding="10px", background_color="#6EA9C5",
                        #     color="white", width="180px", height="45px", border_radius="10px",
                        #     weight="bold", on_click=lambda: AssignmentDetailsState.unsubmit()
                        # ),
                        spacing="5",
                        align="center",
                        margin_top="10px"
                    ),
                    align="center",
                    spacing="3"
                ),
                spacing="9",
                justify="center",
            ),

            spacing="6",
            align_items="center",
        ),
        width="100%",
        min_height="100vh",
        display="flex",
        justify_content="center",
        align_items="center",
        padding_top="7rem",
        margin_left="7rem",
    ),
    )
