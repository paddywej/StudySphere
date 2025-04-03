import reflex as rx
from project.pages.login import FormState
import asyncio
import requests

class LectureState(rx.State):
    """State to handle lecture data."""
    edit_mode: bool = False  # Initially false, so edit buttons are hidden

    def toggle_edit(self):
        """Toggles the edit mode."""
        self.edit_mode = not self.edit_mode

    async def on_load(self):
        """Runs when the page loads."""
        yield FormState.fetch_lectures() 

def button_lecture(lecture_name):
    """Creates a button for each lecture."""
    return rx.box(
        rx.hstack(
            rx.vstack(
                rx.text(lecture_name, size="3", weight="bold"),
                spacing="1",
                align_items="flex-start",
                width="80%",
            ),
            rx.spacer(),
            rx.cond(
                LectureState.edit_mode,
                rx.hstack(
                    rx.button(
                        rx.icon("trash"),
                        size="1",
                        variant="ghost",
                        on_click=FormState.delete_lecture(lecture_name),
                        color="gray",
                        _hover={"color": "red.500"},
                    ),
                    spacing="1",
                ),
            ),
            width="100%",
        ),
        bg="#EFFAFF",
        color="black",
        padding="1em",
        border_radius="8px",
        width="100%",
        shadow="md",
        height="3.5rem",
        margin_bottom="4px",
        _hover={"bg": "#FFEFD0"},
        on_click=FormState.get_lecture(lecture_name)  # Redirect to lecture page
    )

def create_container(lecture) -> rx.Component:
    """Creates a scrollable container with subject buttons."""
    return rx.box(
        rx.text("Lecture Videos", font_size="19px", font_weight="bold", color="white", margin_bottom="1rem"),  
        rx.vstack(rx.foreach(lecture, button_lecture)),  
        width="600px",
        background_color="#598da2",
        border_radius="25px",
        padding="20px",
        margin_top="10px",
        margin_left="16rem"
    )

def Lecture_menu() -> rx.Component:
    """Creates the main page layout with a container for lecture videos and an edit toggle button."""
    # lecture = ["121213", "131312", "213"]
    
    return rx.vstack(
        rx.text(
            FormState.subject_name,
            margin_bottom="4px",
            font_size="35px",
            margin_top="8rem",
            font_weight="bold",
            text_align="center",
            color="#7CAEC2",
            margin_left="7rem",
            width="100%",
        ),
        create_container(FormState.lecture_list),


        rx.cond(
            FormState.role == "Professor",  # Check if the role is "Professor"
            rx.hstack(
                rx.link(
                    rx.button(
                        "Upload Lecture",
                        padding="15px",
                        background_color="#6EA9C5",
                        color="white",
                        width="200px",
                        height="50px",
                        border_radius="10px",
                        weight="bold"
                    ),
                    href="/upload_lecture",
                ),
                rx.link(
                    rx.button(
                        "Edit Lecture",
                        on_click=LectureState.toggle_edit,  # Toggles edit mode
                        padding="15px",
                        background_color="#6EA9C5",
                        color="white",
                        width="200px",
                        height="50px",
                        border_radius="10px",
                        weight="bold"
                    ),
                ),
                spacing="6",
                justify="center",
                align_items="center",
                margin_top="20px",
                width="100%",
                margin_left="8.5rem"
            ),  # Show this if the role is Professor
            rx.box()  # Show an empty box (nothing) if not a Professor
        ),
        on_mount=LectureState.on_load
    )
