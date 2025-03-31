import reflex as rx

# Example students who submitted work
students = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Thomas", "Kate"]

def grading_item(student: str) -> rx.Component:
    """Creates a grading row for each student."""
    return rx.hstack(
        rx.box(
            rx.text(student, size="3"),
            bg="#EFFAFF",
            color="black",
            padding="1em",
            border_radius="8px",
            width="40%",
            shadow="md",
        ),
        rx.input(
            placeholder="Enter score",
            width="40%",
            border_radius="8px",
            padding="0.5em",
            shadow="sm",
        ),
        width="100%",
        justify="between",
        margin_bottom="1em",
    )

def grading() -> rx.Component:
    """Displays a grading page for professors."""
    return rx.vstack(
        rx.text("Grade Student Works", size="4", weight="bold"),
        *[grading_item(student) for student in students],
        
        rx.button(
            "Submit Grades",
            padding="15px",
            background_color="#598da2",
            color="white",
            width="200px",
            height="50px",
            border_radius="10px",
            weight="bold",
            on_click=rx.redirect("/grading")
        ),
        
        spacing="4",
        justify="center",
        align="center",
        width="80%",
        padding="2em",
        bg="#D0E2EB",
        border_radius="25px",
        padding_top="7rem",
        margin_left="14rem",
    )
