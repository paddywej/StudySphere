import reflex as rx

def Year2() -> rx.Component:
    return rx.container(
        # Header with title "Year 1"
        rx.hstack(
            rx.heading("Year 1", size="4", weight="bold"),
            justify="center",
            align_items="center",
            width="100%",
            margin_top="30px",
        ),
        
        # Content Section
        rx.vstack(
            # You can add your content here (e.g., subjects, lessons, etc.)
            rx.text("Welcome to Year 1!"),
            rx.text("Here, you can find the materials and resources for Year 1."),
            rx.text("Explore the lessons and assignments below."),
            
            # Example Button to go back to the homepage
            rx.link(
                rx.button(
                    "Back to Home",
                    padding="10px",
                    background_color="#42798F",
                    size="2",
                    weight="bold",
                    color="white",
                    width="180px",
                    height="50px",
                    border_radius="10px",
                ),
                href="/",  # Navigates back to the homepage
            ),
            margin_top="30px",
            justify="center",
            align_items="center",
        ),
        width="100%",
        padding="1em",
        min_height="100vh",
        bg="#E6F7FB",  # Background color for the page
    )
