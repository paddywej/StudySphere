import reflex as rx

def search_bar() -> rx.Component:
    return rx.hstack(
            rx.input(
                rx.input.slot(rx.icon("search", color="black")),
                placeholder="Search for Courses",  # Just the text for placeholder
                type="search",
                size="3",
                border_radius="20px",  # Make the border rounded
                border="2px solid black",  # Set the border color to black
                color="black",  # Set the text color for input
                background_color="#EFFAFF",  # Set the inner background color
            ),
            margin_top="20px",
            justify="center",  # Center the input horizontally
            align_items="center",  # Center the content vertically
            width="100%"  # Ensure the container takes the full width
        ),