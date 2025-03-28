import reflex as rx

def assignment_item(name: str, due_date: str, status: str) -> rx.Component:
    # Dynamically create an assignment item with status-based background color
    status_colors = {
        "new": "#EFFAFF",  # Light blue for new
        "viewed": "#D3F8E2",  # Light green for viewed
        "done": "#D1E7F8",  # Light blue for done
    }
    return rx.box(
        rx.vstack(
            rx.text(f"{name}", size="3", weight="bold"),
            rx.text(f"Due: {due_date}", size="2"),
            rx.text(f"Status: {status.capitalize()}", size="2", color="gray"),
            spacing="1",  # Space between text lines
        ),
        bg=status_colors.get(status, "#EFFAFF"),  # Default to light blue for new
        color="black",  # Text color
        padding="1em",
        border_radius="8px",  # Round corners
        width="100%",  # Full width of the box
        margin_bottom="1em",  # Space between items
        shadow="md",  # Optional shadow for the box
    )

def assignments() -> rx.Component:
    # Sample list of assignments to display
    assignments_list = [
        {"name": "Math Homework 1", "due_date": "2025-03-29", "status": "new"},
        {"name": "Science Project", "due_date": "2025-04-02", "status": "viewed"},
        {"name": "History Essay", "due_date": "2025-03-25", "status": "done"},
        # Add more assignments here as needed
    ]
    
    return rx.container(
        rx.hstack(  # Create a horizontal stack (two columns)
            rx.box(  # Unfinished assignments (scrollable)
                rx.vstack(
                    rx.text("Unfinished Assignments", size="4", weight="bold"),
                    *[assignment_item(assignment["name"], assignment["due_date"], assignment["status"]) for assignment in assignments_list if assignment["status"] != "done"],
                    spacing="2",  # Space between items
                    width="100%",  # Ensure it takes full width of the box
                ),
                width="45%",  # Slightly smaller width for the boxes
                height="500px",  # Controlled height for the box
                bg="#D0E2EB",  # Background color
                color="black",  # Text color
                padding="1em",
                overflow="auto",  # Enable scrolling if content exceeds box height
                border_radius="25px",  # Round corners
                margin_right="2rem",  # Space between the two boxes
            ),
            rx.box(  # Done assignments (scrollable)
                rx.vstack(
                    rx.text("Done Assignments", size="4", weight="bold"),
                    *[assignment_item(assignment["name"], assignment["due_date"], assignment["status"]) for assignment in assignments_list if assignment["status"] == "done"],
                    spacing="2",  # Space between items
                    width="100%",  # Ensure it takes full width of the box
                ),
                width="45%",  # Slightly smaller width for the boxes
                height="500px",  # Controlled height for the box
                bg="#D0E2EB",  # Background color
                color="black",  # Text color
                padding="1em",
                overflow="auto",  # Enable scrolling if content exceeds box height
                border_radius="25px",  # Round corners
            ),
            spacing="4",  # Increase space between columns
            justify="center",  # Center both boxes horizontally
            width="100%",  # Ensure the container takes up full width
        ),
        
        width="100%",  # Ensure the container takes up full width
        padding="2em",  # Add padding around the container
        position="relative",  # Position parent relative to allow "top" positioning
        top="7rem",  # Adds space from the top of the screen/container
        overflow="hidden",  # Prevent scrolling for the whole page
        margin_left="7rem",
        min_height="100vh"
    )
