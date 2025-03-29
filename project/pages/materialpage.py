import reflex as rx

def create_container(title: str, items: list) -> rx.Component:
    """Creates a scrollable container with space for textbooks or notes."""
    return rx.box(
        # Title for the section (Textbooks or Notes)
        rx.text(title, font_size="18px", font_weight="bold", color="white"),
        # Content that will exceed the container to make it scrollable
        rx.vstack(
            *[rx.box(item, padding="8px", background_color="#f8f8f8", border_radius="5px") for item in items],
            spacing="9"
        ),
        height="450px",  # Container height
        width="450px",  # Reduced width for better centering
        background_color="#598da2",  # Container background color
        border_radius="25px",  # Increased border radius for more rounded corners
        padding="10px",  # Reduced padding inside the container
        overflow_y="scroll",  # Enable vertical scrolling when content overflows
    )

def materials() -> rx.Component:
    """Creates the main page layout with two scrollable containers: one for textbooks and one for notes."""
    textbooks = ["Textbook 1", "Textbook 2", "Textbook 3", "Textbook 4", "Textbook 5"]  # Example list of textbooks
    notes = ["Lecture 1 Notes", "Lecture 2 Notes", "Lecture 3 Notes", "Lecture 4 Notes", "Lecture 5 Notes"]  # Example list of notes
    
    return rx.box(
        rx.vstack(
            rx.text("Materials", font_size="24px", font_weight="bold", color="#598da2"),
            rx.vstack(  # Vertical stack for materials and buttons
                rx.hstack(  # Horizontal stack for the containers (Textbooks and Notes)
                    create_container("Textbooks", textbooks),  # Container for textbooks
                    create_container("Notes", notes),  # Container for notes
                    spacing="9",  # Space between containers
                    justify="center",  # Center the containers horizontally
                ),
                # Action buttons below the containers
                rx.hstack(
                    rx.button(
                        "Upload Material", 
                        padding="15px", 
                        background_color="#6EA9C5", 
                        color="white", 
                        width="200px", 
                        height="50px", 
                        border_radius="10px", 
                        weight="bold"
                    ),
                    rx.button(
                        "Edit Material", 
                        padding="15px", 
                        background_color="#6EA9C5", 
                        color="white", 
                        width="200px", 
                        height="50px", 
                        border_radius="10px", 
                        weight="bold"
                    ),
                    rx.button(
                        "Delete Material", 
                        padding="15px", 
                        background_color="#6EA9C5", 
                        color="white", 
                        width="200px", 
                        height="50px", 
                        border_radius="10px", 
                        weight="bold"
                    ),
                    spacing="9",  # Space between buttons
                    justify="center",  # Center the buttons horizontally
                    align_items="center",  # Vertically center the buttons
                    margin_top="40px",  # Space between containers and buttons
                    margin_left="13%",  # Added left margin to shift buttons away from the left
                ),
            ),
            spacing="9",  # Space between the title and materials content
            align_items="center",  # Align everything in the center
        ),
        width="100%",
        min_height="100vh",
        display="flex",
        justify_content="center",  # Center everything horizontally
        align_items="center",  # Center everything vertically
        margin_top="50px",
        margin_left="50px", 
    )
