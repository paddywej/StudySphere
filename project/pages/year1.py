import reflex as rx

def Year1() -> rx.Component:
    return rx.box(
        # Full page layout with white background
        rx.vstack(
            # Main content section
            rx.text("Welcome to Year 1!", font_size="24px", color="black", margin_top="20px"),
            rx.text("Here, you can find the materials and resources for Year 1.", font_size="18px", color="black"),
            rx.text("Explore the lessons and assignments below.", font_size="18px", color="black"),
            
            # Button linking back to the homepage
            rx.link(
                rx.button(
                    "Back to Home",
                    padding="12px",
                    background_color="#42798F",
                    # Removed invalid 'md' size value
                    size="2",  # Using one of the valid values like '1', '2', '3', '4'
                    color="white",
                    width="200px",
                    height="50px",
                    border_radius="10px",
                ),
                href="/home"  # Link to homepage
            ),
            
            # Added missing comma and corrected alignment
            padding_top="100px",  # Correctly placed comma here
            justify="center",
            align_items="center",
            margin_top="40px",
        ),
        width="100%", 
        height="100%",
        align_items="center",  
    )
