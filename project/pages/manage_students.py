import reflex as rx

def student_item(student: str) -> rx.Component:
    return rx.box(
        rx.text(student, size="3"),
        bg="#EFFAFF",  # Light blue background for student items
        color="black",
        padding="1em",
        border_radius="8px",
        width="100%",
        margin_bottom="1em",
        shadow="md",
        _hover={"bg": "#BFD9E5"},
    )

# Example student data
students_list = [
    "Alice",
    "Bob",
    "Charlie",
    "David",
    "Eve",
    "Frank",
]

def manage_students() -> rx.Component:
    return rx.vstack(
        rx.box(
            rx.vstack(
                rx.text("Students", size="4", weight="bold"),
                *[student_item(student) for student in students_list],  # Dynamically create student items
                spacing="1",
                width="100%",
            ),
            width="45%",  # Set width of the container
            height="500px",
            bg="#D0E2EB",
            color="black",
            padding="1em",
            overflow="auto",
            border_radius="25px",
            margin_bottom="2rem",  # Space between the container and the buttons
        ),
        
        # Buttons to add and remove students
        rx.hstack(
            # Add Student Button
            rx.button(
                "Add Student",
                padding="15px",
                background_color="#598da2",
                color="white",
                width="200px",
                height="50px",
                border_radius="10px",
                weight="bold",
            ),

            # Remove Student Button
            rx.button(
                "Remove Student",
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
