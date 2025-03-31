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

def subject_item(name: str, year: int, term: int) -> rx.Component:
    """Creates a styled button for each subject."""
    return rx.box(
        rx.vstack(
            rx.text(name, size="3", weight="bold"),
            rx.text(f"Year {year} - Term {term}", size="2", color="gray"),
            spacing="1",
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
    """Creates a scrollable container with subject buttons."""
    return rx.box(
        rx.text(title, font_size="24px", font_weight="bold", color="white", text_align="center", margin_bottom="1rem"),
        rx.vstack(
            *[subject_item(subject["name"], subject["year"], subject["term"]) for subject in subjects],
            spacing="3", 
            align_items="center" 
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
    professor_name = "Dr. Visit"  # This would come from the get_professor_name function when uncommented
    professor_subjects = [
        {"name": "Computer Science 101", "year": 1, "term": 1},
        {"name": "Data Structures", "year": 2, "term": 1},
        {"name": "Algorithms", "year": 2, "term": 2},
        {"name": "Machine Learning", "year": 3, "term": 1},
        {"name": "Artificial Intelligence", "year": 3, "term": 2},
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