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
        rx.text(title, font_size="20px", font_weight="bold", color="white", text_align="center", margin_bottom="1rem"),  # Centered title text
        rx.vstack(
            *[rx.button(
                name, 
                padding="12px",  
                background_color="#F4F3F2", 
                color="black", 
                border_radius="8px",  # Rounded corners for a smoother look
                width="100%",
                height="50px",  # Slightly smaller button height
                _hover={"bg": "#FFEFD0"} 
            ) for name in subjects],
            spacing="2", 
            align_items="center" 
        ),
        height="400px",  # Adjusted height for consistency
        width="400px",  # Reduced width to make the page more compact
        background_color="#598da2",
        border_radius="25px",
        padding="15px",  # Slightly reduced padding
        overflow_y="auto",  # Scrollable content
    )


def Year4() -> rx.Component:
    """Creates the main page layout with scrollable containers for Semester 1 and 2."""
    # semester_1_subjects = get_subjects(1, 1) 
    # semester_2_subjects = get_subjects(1, 2)  

    return rx.box(
        rx.vstack(
            rx.text("Year 4", font_size="30px", font_weight="bold", color="#598da2", text_align="center", margin_bottom="1rem"),  # Adjusted title size
            rx.hstack(
                create_container("Semester 1", ["Math", "Science", "English"]),  # Added mock subject names for now
                create_container("Semester 2", ["History", "Geography", "Art"]),  # Added mock subject names for now
                # create_container("Semester 1", semester_1_subjects),
                # create_container("Semester 2", semester_2_subjects),
                spacing="5",  # Reduced spacing between the two containers
                align="center"
            ),
            spacing="5",  # Adjusted overall spacing between elements
            align_items="center"
        ),
        width="100%",
        min_height="100vh",
        display="flex",
        justify_content="center",
        align_items="center",
        padding_top="25px",
        padding_left="250px",
    )
