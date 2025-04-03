import reflex as rx
from project.pages.login import FormState
import asyncio
import requests

class MaterialState(rx.State):
    """State to handle lecture data."""
    edit_mode: bool = False  

    def toggle_edit(self):
        """Toggles the edit mode."""
        self.edit_mode = not self.edit_mode

    async def on_load(self):
        """Runs when the page loads."""
        yield FormState.fetch_materials()

def button_lecture(material):
    """Creates a button for each lecture."""
    return rx.box(
        rx.hstack(
            rx.vstack(
                rx.text(material, size="3", weight="bold"),
                spacing="1",
                align_items="flex-start",
                width="80%",
                cursor="pointer",
                on_click=rx.download(url=rx.get_upload_url(material))
            ),
            rx.spacer(),
            rx.cond(
                MaterialState.edit_mode,
                rx.hstack(
                    rx.button(
                        rx.icon("trash"),
                        size="1",
                        variant="ghost",
                        on_click=FormState.delete_material(material),
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
        # on_click=FormState.get_material(material)  
    )

def create_container(title:str,lecture) -> rx.Component:
    """Creates a scrollable container with subject buttons."""
    return rx.box(
        rx.text(title, font_size="19px", font_weight="bold", color="white", margin_bottom="1rem"),  
        rx.vstack(rx.foreach(lecture, button_lecture)),  
        width="500px",
        background_color="#598da2",
        border_radius="25px",
        padding="20px",
        margin_top="10px",
        height="27rem"
    )

def materials() -> rx.Component:
    """Creates the main page layout with two scrollable containers: one for textbooks and one for notes."""
    textbooks = ["Textbook 1", "Textbook 2", "Textbook 3", "Textbook 4", "Textbook 5"]  # Example list of textbooks
    notes = ["Lecture 1 Notes", "Lecture 2 Notes", "Lecture 3 Notes", "Lecture 4 Notes", "Lecture 5 Notes"]  # Example list of notes
    
    return rx.box(
        rx.vstack(
            rx.text("Materials", font_size="28px", font_weight="bold", color="#598da2"),
            rx.vstack(  # Vertical stack for materials and buttons
                rx.hstack(  # Horizontal stack for the containers (Textbooks and Notes)
                    create_container("Textbooks", FormState.textbook_list),  # Container for textbooks
                    create_container("Notes", FormState.note_list),  # Container for notes
                    spacing="9",  # Space between containers
                    justify="center",  # Center the containers horizontally
                ),
                # Action buttons below the containers

                rx.cond(
                    FormState.role == "Professor",
                    rx.hstack(
                        rx.button(
                            "Upload Material", 
                            padding="15px", 
                            background_color="#6EA9C5", 
                            color="white", 
                            width="200px", 
                            height="50px", 
                            border_radius="10px", 
                            weight="bold",
                            on_click=rx.redirect("/upload_material")
                        ),
                        rx.button(
                            "Edit Material", 
                            on_click=MaterialState.toggle_edit,
                            padding="15px", 
                            background_color="#6EA9C5", 
                            color="white", 
                            width="200px", 
                            height="50px", 
                            border_radius="10px", 
                            weight="bold"
                        ),
                    
                        spacing="9",  # Space between buttons
                        justify="center",  # Center the buttons horizontally
                        align_items="center",  # Vertically center the buttons
                        margin_top="40px",  # Space between containers and buttons
                        margin_left="24%",  # Added left margin to shift buttons away from the left
                    ),
                    rx.box() 
                ),
            ),
            spacing="6",  # Space between the title and materials content
            align_items="center",  # Align everything in the center
        ),
        width="100%",
        min_height="100vh",
        display="flex",
        justify_content="center",  # Center everything horizontally
        align_items="center",  # Center everything vertically
        padding_top="7rem",
        margin_left="7rem",
        on_mount=MaterialState.on_load
    )
