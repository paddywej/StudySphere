import reflex as rx
import requests

def fetch_assignments_data() -> list:
    """Simulate fetching multiple assignments data from a backend."""
    # Simulate an API request to get the assignment data
    # Example of how you might get the assignment data from an API or database:
    # response = requests.get(f"http://example.com/api/assignments/")
    # return response.json()
    
    # Mock data for simulation purposes:
    assignments_data = [
        {
            "assignment_name": "Math Assignment 1",
            "subject_name": "Mathematics",
            "students": [
                {"name": "Student 1", "file": "Assignment1.pdf"},
                {"name": "Student 2", "file": "Assignment1.pdf"},
            ]
        },
        {
            "assignment_name": "Science Project 1",
            "subject_name": "Science",
            "students": [
                {"name": "Student A", "file": "Project1.pdf"},
                {"name": "Student B", "file": "Project1.pdf"},
            ]
        }
    ]
    return assignments_data

def create_assignment_container(assignment_title: str, subject_name: str, student_data: list) -> rx.Component:
    """Creates a scrollable container with student assignment data."""
    return rx.box(
        # Display the assignment title and subject name
        rx.text(f"{assignment_title} - {subject_name}", font_size="24px", font_weight="bold", color="black", text_align="center", margin_bottom="1rem"),
        rx.vstack(
            *[
                rx.hstack(
                    # Separate containers for student name, file, and grade, with consistent width and height
                    rx.box(
                        rx.text(student["name"], font_size="16px"),
                        width="33%",  # Ensure equal width for all elements
                        padding="10px",
                        background_color="#effaff",  # Background color for student name
                        color="black",
                        border_radius="4px",
                        height="50px",  # Ensure consistent height for all containers
                        display="flex",
                        align_items="center",
                        justify_content="center"
                    ),
                    rx.box(
                        rx.text(student["file"], font_size="16px"),
                        width="33%",  # Ensure equal width for all elements
                        padding="10px",
                        background_color="#effaff",  # Background color for file name
                        color="black",
                        border_radius="4px",
                        height="50px",  # Ensure consistent height for all containers
                        display="flex",
                        align_items="center",
                        justify_content="center"
                    ),
                    rx.box(
                        rx.hstack(
                            # Ensure input field is stretched and properly sized
                            rx.input(placeholder="Enter grade", width="100%", bg="white", border_radius="4px"),
                        ),
                        padding="10px",
                        background_color="#effaff",  # Background color for grade input
                        border_radius="4px",
                        height="50px",  # Ensure consistent height for all containers
                        display="flex",
                        align_items="center",
                        justify_content="center",
                        width="33%",  # Ensure the container holding the input is the same width as the others
                    ),
                    spacing="2",
                    align="center"
                ) for student in student_data
            ],
            spacing="2",
            align_items="center"
        ),
        height="450px",
        width="100%",  # Ensure the container width spans the full width
        background_color="#cfe2eb",  # Set to white for the assignment container
        border_radius="10px",  # Rounded corners for the video area
        padding="20px",
        overflow_y="scroll",
    )

def all_assignments() -> rx.Component:
    """Creates the main assignments page layout with scrollable containers."""
    # Fetching all assignments data from the backend
    assignments_data = fetch_assignments_data()
    
    return rx.box(
        rx.vstack(
            rx.text("Assignments", font_size="35px", font_weight="bold", color="#598da2", text_align="center"),
            rx.vstack(  # Use vstack for top-to-bottom layout
                *[
                    create_assignment_container(
                        assignment["assignment_name"], 
                        assignment["subject_name"], 
                        assignment["students"]
                    ) for assignment in assignments_data
                ],
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
    )
