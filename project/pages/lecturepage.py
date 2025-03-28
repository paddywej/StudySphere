import reflex as rx

def create_container(lecture_number: int, lecture_date: str) -> rx.Component:
    """Creates a container with the lecture number, date, and space for a video."""
    return rx.box(
        # Lecture number and date
        rx.text(f"Lecture {lecture_number}", font_size="18px", font_weight="bold", color="white"),
        rx.text(f"Date: {lecture_date}", font_size="14px", color="white"),
        
        # Placeholder for video (can be replaced with an actual video component)
        rx.box(
            "Video Placeholder",  # Placeholder text, will be replaced with a video later
            width="100%",  # Full width of the container
            height="400px",  # Adjust the height of the video area
            background_color="#d3edf8",  # Placeholder background color for the video
            border_radius="10px",  # Rounded corners for the video area
            margin_top="15px",  # Space above the video
        ),
        
        # Styling for the container
        width="1500px",  # Container width
        background_color="#598da2",  # Container background color
        border_radius="25px",  # Rounded corners
        padding="20px",  # Padding inside the container
        margin_top="0px",  # Less space on top
    )

def lectures() -> rx.Component:
    """Creates the main page layout with a single container for a lecture."""
    return rx.box(
        create_container(1, "2025-03-28"),  # Example lecture with number and date
        width="100%",
        min_height="100vh",
        display="flex",
        justify_content="center",
        align_items="center",
        padding_top="0px",  # Less space on top
    )
