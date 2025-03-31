import reflex as rx

def file_submission_item(student: str, file: str) -> rx.Component:
    """Creates a box for each student's file submission."""
    return rx.hstack(
        rx.box(
            rx.text(student, size="3"),
            bg="#EFFAFF",  # Light blue background for student items
            color="black",
            padding="1em",
            border_radius="8px",
            width="30%",
            shadow="md",
            _hover={"bg": "#BFD9E5"},
        ),
        rx.box(
            rx.text(file, size="3"),
            bg="#EFFAFF",  # Light blue background for file items
            color="black",
            padding="1em",
            border_radius="8px",
            width="60%",
            shadow="md",
            _hover={"bg": "#BFD9E5"},
        ),
        width="100%",
        justify="between",  # Corrected justify to 'between'
        margin_bottom="1em",
    )

# Example student and their submitted files
students_files = [
    ("Alice", "homework4.pdf"),
    ("Bob", "homework4.docx"),
    ("Charlie", "project_report.pdf"),
    ("David", "assignment3.pdf"),
    ("Eve", "homework4.pdf"),
    ("Frank", "final_exam_submission.pdf"),
]

def manage_submitted_works() -> rx.Component:
    """Displays the list of students and their submitted files."""
    return rx.vstack(
        rx.box(
            rx.vstack(
                rx.text("Submitted Works", size="4", weight="bold"),
                *[file_submission_item(student, file) for student, file in students_files],  # Dynamically create file submission items
                spacing="1",
                width="100%",
            ),
            width="80%",  # Wider table
            height="500px",
            bg="#D0E2EB",
            color="black",
            padding="1em",
            overflow="auto",
            border_radius="25px",
            margin_bottom="2rem",  # Space between the container and the buttons
        ),
        
        # Buttons to perform actions on the submissions (e.g., download or view)
        rx.hstack(
            # View Files Button
            rx.button(
                "Grade Works",
                padding="15px",
                background_color="#598da2",
                color="white",
                width="200px",
                height="50px",
                border_radius="10px",
                weight="bold",
            ),
            spacing="2",  # Space between the buttons
            justify="center",  # Center the buttons horizontally
            margin_top="5px",  # Space above the buttons
        ),
        spacing="4",
        justify="center",
        align="center",
        width="100%",
        padding="2em",
        padding_top="7rem",
        margin_left="7rem",
        min_height="100vh",
        bg="white",
    )
