import reflex as rx
import requests

# def get_subjects(year: int, semester: int):
#     url = f"http://localhost:8000/subjects/{year}/{semester}" 
#     response = requests.get(url)
#     if response.status_code == 200:
#         return response.json()  
#     else:
#         return []

def create_container(title: str, subjects: list) -> rx.Component:
    """Creates a scrollable container with subject buttons."""
    return rx.box(
        rx.text(title, font_size="24px", font_weight="bold", color="white", text_align="center", margin_bottom="1rem"),  # Centered title text
        rx.vstack(
            *[rx.button(
                name, 
                padding="15px",  
                background_color="#F4F3F2", 
                color="black", 
                border_radius="0",
                width="100%",
                height="65px",
                _hover={"bg": "#FFEFD0"} 
            ) for name in subjects],
            spacing="2", 
            align_items="center" 
        ),
        height="450px",
        width="550px",
        background_color="#598da2",
        border_radius="25px",
        padding="20px",
        overflow_y="scroll",
    )


def Year1() -> rx.Component:
    """Creates the main page layout with scrollable containers for Semester 1 and 2."""
    # semester_1_subjects = get_subjects(1, 1) 
    # semester_2_subjects = get_subjects(1, 2)  

    return rx.box(
        rx.vstack(
            rx.text("Year 1", font_size="35px", font_weight="bold", color="#598da2", text_align="center"),  # Centered title text
            rx.hstack(
                create_container("semester 1", "subject"),
                create_container("semester 2", "subject"),
                # create_container("Semester 1", semester_1_subjects),
                # create_container("Semester 2", semester_2_subjects),
                spacing="9",
                align="center"
            ),
            spacing="9",
            align_items="center"
        ),
        width="100%",
        min_height="100vh",
        display="flex",
        justify_content="center",
        align_items="center",
        padding_top="50px",
    )
