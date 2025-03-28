import reflex as rx

def create_container(title: str) -> rx.Component:
    """Creates a scrollable container with space for semester titles."""
    return rx.box(
        # Title for the semester (Semester 1 or Semester 2)
        rx.text(title, font_size="18px", font_weight="bold", color="white"),
        # Content that will exceed the container to make it scrollable
        rx.vstack(
            *[rx.box(f"Button {i}", padding="10px", background_color="#f8f8f8", border_radius="5px") for i in range(10)],  # Add more buttons to create overflow
            spacing="9"
        ),
        height="450px",  # Container height
        width="550px",  # Same width for both containers
        background_color="#598da2",  # Container background color
        border_radius="25px",  # Increased border radius for more rounded corners
        padding="20px",  # Padding inside the container
        overflow_y="scroll",  # Enable vertical scrolling when content overflows
    )

def Year4() -> rx.Component:
    """Creates the main page layout with two scrollable containers for Semester 1 and Semester 2."""
    return rx.box(
        rx.vstack(
            rx.text("Year 4", font_size="24px", font_weight="bold", color="#598da2"),
            rx.hstack(
                create_container("Semester 1"),  # First container with Semester 1
                create_container("Semester 2"),  # Second container with Semester 2
                spacing="9",  # Space between containers
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