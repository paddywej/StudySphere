import reflex as rx
import uuid
import datetime
import requests
from io import BytesIO
from project.pages.login import FormState  

color = "#6EA9C5"  # Matching button color

def Upload_material():
    return rx.box(
        rx.vstack(
            rx.text("Upload Material", font_size="22px", font_weight="bold", color="white", margin_bottom="1rem"),
            
            # Dropdown to select material type
            rx.select(
                ["Textbooks", "Notes"],
                value=FormState.material_type,  # Bind to state
                on_change=FormState.set_material_type,  # Update state when changed
                width="100%",
                padding="0.5em",
                border_radius="8px",
                bg="white",
                color="black",
                margin_bottom="1rem",
            ),

            # File Upload Section
            rx.upload(
                rx.vstack(
                    rx.button("Select File", color="white", background_color=color, border_radius="8px", padding="10px", 
                              _hover={"background_color": "#598da2"}),
                    rx.text("Drag and drop files here or click to select files", color="gray"),
                ),
                id="upload1",
                max_files=1,
                border=f"2px dashed {color}",
                border_radius="10px",
                padding="3em",
                width="100%",
                background_color="#EFFAFF",
            ),

            rx.text(rx.selected_files("upload1"), color="black"),
            
            # Upload & Clear Buttons
            rx.hstack(
                rx.button(
                    "Upload", 
                    on_click=FormState.handle_upload_material(rx.upload_files(upload_id="upload1")), 
                    background_color=color, 
                    color="white", 
                    width="150px", 
                    height="45px", 
                    border_radius="8px",
                    _hover={"background_color": "#598da2"}
                ),
                rx.button(
                    "Clear",
                    on_click=rx.clear_selected_files("upload1"),
                    background_color="#F4F3F2",
                    color="black",
                    width="150px",
                    height="45px",
                    border_radius="8px",
                    _hover={"background_color": "#FFEFD0"}
                ),
                rx.button(
                    "Back",
                    on_click=lambda: rx.redirect("/materials"),
                    background_color="gray",
                    color="white",
                    width="150px",
                    height="45px",
                    border_radius="8px",
                    _hover={"background_color": "black"}
                ),
                spacing="4",
                justify="center"
            ),
        ),
        width="600px",
        background_color="#598da2",
        border_radius="25px",
        padding="20px",
        margin_top="10px",
        margin_left="9rem",
        min_height="95vh"
    )
