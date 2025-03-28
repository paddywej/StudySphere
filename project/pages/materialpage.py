import reflex as rx

def create_container(title: str, items: list) -> rx.Component:
    """Creates a scrollable container with space for textbooks or notes."""
    return rx.box(
        # Title for the section (Textbooks or Notes)
        rx.text(title, font_size="18px", font_weight="bold", color="white"),
        # Content that will exceed the container to make it scrollable
        rx.vstack(
            *[rx.box(item, padding="10px", background_color="#f8f8f8", border_radius="5px") for item in items],
            spacing="9"
        ),
        height="450px",  # Container height
        width="550px",  # Same width for both containers
        background_color="#598da2",  # Container background color
        border_radius="25px",  # Increased border radius for more rounded corners
        padding="20px",  # Padding inside the container
        overflow_y="scroll",  # Enable vertical scrolling when content overflows
    )

def materials() -> rx.Component:
    """Creates the main page layout with two scrollable containers: one for textbooks and one for notes."""
    textbooks = ["Textbook 1", "Textbook 2", "Textbook 3", "Textbook 4", "Textbook 5"]  # Example list of textbooks
    notes = ["Lecture 1 Notes", "Lecture 2 Notes", "Lecture 3 Notes", "Lecture 4 Notes", "Lecture 5 Notes"]  # Example list of notes
    
    return rx.box(
        rx.vstack(
            rx.text("Materials", font_size="24px", font_weight="bold", color="#598da2"),
            rx.hstack(
                create_container("Textbooks", textbooks),  # Container for textbooks
                create_container("Notes", notes),  # Container for notes
                spacing="4",  # Adjust spacing to your preference
                align="center"
            ),
            spacing="9",
            align_items="center"
        ),
        width="100%",
        min_height="100vh",
        display="flex",
        justify_content="left",
        align_items="center",
        padding_top="50px",  # Adjusted space on top
    )
