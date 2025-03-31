import reflex as rx
import requests

# def get_professor_subjects(professor_id: int):
#     url = f"http://localhost:8000/professors/{professor_id}/subjects"
#     response = requests.get(url)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         return []

# def get_professor_name(professor_id: int):
#     """Retrieves the professor's name from the API.
#     
#     Args:
#         professor_id (int): The ID of the professor
#         
#     Returns:
#         str: The name of the professor or "Professor" if not found
#     """
#     url = f"http://localhost:8000/professors/{professor_id}"
#     response = requests.get(url)
#     if response.status_code == 200:
#         professor_data = response.json()
#         return professor_data.get("name", "Professor")
#     else:
#         return "Professor"

def subject_item(name: str, year: int, term: int, subject_id: int = None) -> rx.Component:
    """Creates a styled button for each subject with edit and delete options."""
    return rx.box(
        rx.hstack(
            rx.vstack(
                rx.text(name, size="3", weight="bold"),
                rx.text(f"Year {year} - Term {term}", size="2", color="gray"),
                spacing="1",
                align_items="flex-start",
                width="80%",
            ),
            rx.spacer(),
            rx.hstack(
                rx.button(
                    rx.icon("pencil"),
                    size="1",
                    variant="ghost",
                    on_click=lambda: rx.window_alert(f"Edit subject: {name}"),
                    color="gray",
                    _hover={"color": "blue.500"},
                ),
                rx.button(
                    rx.icon("trash"),
                    size="1",
                    variant="ghost",
                    on_click=lambda: rx.window_alert(f"Delete subject: {name}"),
                    color="gray",
                    _hover={"color": "red.500"},
                ),
                spacing="1",
            ),
            width="100%",
        ),
        bg="#F4F3F2",
        color="black",
        padding="1em",
        border_radius="8px",
        width="100%",
        shadow="md",
        _hover={"bg": "#FFEFD0"},
    )

def create_container(title: str, subjects: list) -> rx.Component:
    """Creates a scrollable container with subject buttons and an add button."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text(title, font_size="24px", font_weight="bold", color="white"),
                rx.spacer(),
                rx.button(
                    rx.hstack(
                        rx.icon("plus"),
                        rx.text("Add Subject"),
                        spacing="1",
                    ),
                    bg="white",
                    color="#598da2",
                    size="2",
                    border_radius="md",
                    on_click=lambda: rx.window_alert("Add new subject"),
                    _hover={"bg": "#FFEFD0"},
                ),
                width="100%",
            ),
            rx.divider(border_color="white", opacity=0.3, margin_y="3"),
            rx.vstack(
                *[subject_item(subject["name"], subject["year"], subject["term"], subject.get("id")) for subject in subjects],
                spacing="3", 
                align_items="center", 
                width="100%",
            ),
            spacing="3", 
            align_items="flex-start",
            width="100%",
        ),
        height="450px",
        width="550px",
        background_color="#598da2",
        border_radius="25px",
        padding="20px",
        overflow_y="scroll",
    )

def professor_subjects() -> rx.Component:
    """Creates the main page layout displaying subjects taught by the professor."""
    # Mock data for development purposes
    professor_id = 1  # This would typically come from your app state or URL params
    
    # professor_subjects = get_professor_subjects(professor_id)
    # professor_name = get_professor_name(professor_id)
    
    # Using mock data for now
    professor_name = "Dr. Smith"  # This would come from the get_professor_name function when uncommented
    professor_subjects = [
        {"id": 1, "name": "Computer Science 101", "year": 1, "term": 1},
        {"id": 2, "name": "Data Structures", "year": 2, "term": 1},
        {"id": 3, "name": "Algorithms", "year": 2, "term": 2},
        {"id": 4, "name": "Machine Learning", "year": 3, "term": 1},
        {"id": 5, "name": "Artificial Intelligence", "year": 3, "term": 2},
    ]
    
    return rx.box(
        rx.vstack(
            rx.text(f"{professor_name}'s Subjects", font_size="35px", font_weight="bold", color="#598da2", text_align="center"),
            create_container("Subjects Taught", professor_subjects),
            spacing="6",
            align_items="center"
        ),
        width="100%",
        min_height="100vh",
        display="flex",
        justify_content="center",
        align_items="center",
        padding_top="50px",
    )