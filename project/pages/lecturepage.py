import reflex as rx
from project.pages.login import FormState

def create_container() -> rx.Component:
    """Creates a container with the lecture videos label, date, and space for a video."""
    return rx.box(
        # Lecture videos label and date
        rx.text("Lecture Videos", font_size="19px", font_weight="bold", color="white"),
        # rx.text(f"Date: {lecture_date}", font_size="14px", color="white"),
        
        # Placeholder for video
        rx.box(
            rx.vstack(
                rx.text(FormState.lecture_name, font_size="15px", font_weight="bold", color="#7CAEC2", text_align="center",margin_left="4px"),
                
                rx.cond(
                    FormState.lecture_name,
                    rx.video(url=rx.get_upload_url(FormState.lecture_name),
                    margin_left="10rem"
                    ),
                ),
            ),
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
        margin_top="7px",  # Space above the container
    )

def lectures(subject_title: str) -> rx.Component:
    """Creates the main page layout with a single container for lecture videos and action buttons horizontally below."""
    return rx.vstack(  # Use vstack to stack the container and buttons vertically
        
        # Dynamic Subject Title outside the container
        # rx.text(subject_title, font_size="24px", font_weight="bold", color="#598da2", text_align="center"),
        rx.text(
            FormState.subject_name,
            margin_bottom="4px",
            font_size="35px",
            margin_top="8rem",
            font_weight="bold",
            text_align="center",
            color="#7CAEC2",
            margin_left="1rem",
            width="100%",
        ),
        create_container(),  # Calls the create_container function with a date


        rx.hstack( 
        #         rx.button(
        #             "Download", 
        #             padding="15px", 
        #             background_color="#6EA9C5", 
        #             color="white", 
        #             width="200px", 
        #             height="50px", 
        #             border_radius="10px", 
        #             weight="bold",
        #             on_click=rx.download(url=FormState.url),
        #         ),
        spacing="3",  # Space between buttons
        justify="center",  # This should center the buttons horizontally
        align_items="center",  # Center the buttons vertically (if needed)  
        margin_top="20px",  # Space between the container and the buttons
        width="100%",  # Ensure the hstack takes up full width to allow centering
        ),
    )
