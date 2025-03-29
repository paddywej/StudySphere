import reflex as rx

def create_container(lecture_number: int, lecture_date: str) -> rx.Component:
    """Creates a container with the lecture number, date, and space for a video."""
    return rx.box(
        # Lecture number and date
        rx.text(f"Lecture {lecture_number}", font_size="18px", font_weight="bold", color="white"),
        rx.text(f"Date: {lecture_date}", font_size="14px", color="white"),
        
        # Placeholder for video
        rx.box(
            "Video Placeholder",  # Placeholder text
            width="100%",  # Video width (100% of the parent container's width)
            height="400px",  # Video area height
            background_color="#d3edf8",  # Background color for the video placeholder
            border_radius="10px",  # Rounded corners for the video area
            margin_top="15px",  # Space above the video placeholder
        ),
        
        # Styling for the container
        width="1000px", 
        background_color="#598da2",  # Background color of the container
        border_radius="25px",  # Rounded corners for the container
        padding="20px",  # Padding inside the container
        margin_top="90px",  # Space above the container
    )

def lectures() -> rx.Component:
    """Creates the main page layout with a single container for a lecture and action buttons horizontally below."""
    return rx.vstack(  # Use vstack to stack the container and buttons vertically
        create_container(1, "2025-03-28"),  # Calls the create_container function for lecture 1 with a date
        
        # Stack of buttons for uploading, editing, and deleting lectures
        rx.hstack(  # Use hstack for horizontal alignment of the buttons
            # Upload Lecture Button
            rx.link(
                rx.button(
                    "Upload Lecture", 
                    padding="15px", 
                    background_color="#6EA9C5", 
                    color="white", 
                    width="200px", 
                    height="50px", 
                    border_radius="10px", 
                    weight="bold"
                ),
                href="/upload_lecture",  # Redirect to upload lecture page
            ),
            # Edit Lecture Details Button
            rx.link(
                rx.button(
                    "Edit Lecture Details", 
                    padding="15px", 
                    background_color="#6EA9C5", 
                    color="white", 
                    width="200px", 
                    height="50px", 
                    border_radius="10px", 
                    weight="bold"
                ),
                href="/edit_lecture",  # Redirect to edit lecture page
            ),
            # Delete Lecture Button
            rx.link(
                rx.button(
                    "Delete Lecture", 
                    padding="15px", 
                    background_color="#6EA9C5", 
                    color="white", 
                    width="200px", 
                    height="50px", 
                    border_radius="10px", 
                    weight="bold"
                ),
                href="/delete_lecture",  # Redirect to delete lecture page
            ),
            spacing="6",  # Space between buttons
            justify="center",  # This should center the buttons horizontally
            align_items="center",  # Center the buttons vertically (if needed)
            margin_top="20px",  # Space between the container and the buttons
            width="100%",  # Ensure the hstack takes up full width to allow centering
        ),
    )

# Outer container styling (full page)
def outer_layout() -> rx.Component:
    """Outer container for full page layout"""
    return rx.box(
        lectures(),
        width="100%",
        min_height="100vh",
        display="flex",
        justify_content="center",
        align_items="center",
    )
