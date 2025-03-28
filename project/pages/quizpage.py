import reflex as rx

def quiz_item(name: str, due_date: str, status: str, quiz_time: str) -> rx.Component:
    # Dynamically create a quiz item with status-based background color
    status_colors = {
        "new": "#EFFAFF",  # Light blue for new
        "done": "#D3F8E2",  # Light blue for done
    }
    return rx.box(
        rx.vstack(
            rx.text(f"{name}", size="3", weight="bold"),
            rx.text(f"Due: {due_date}", size="2"),
            rx.text(f"Time: {quiz_time}"),  # Display quiz time here
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

def quiz() -> rx.Component:
    # Sample list of quizzes to display, with quiz time fetched from the database later
    quizzes_list = [
        {"name": "Math Quiz", "due_date": "2025-03-29", "status": "new", "quiz_time": "15:00 PM - 16:00 PM"},
        {"name": "Science Quiz", "due_date": "2025-04-02", "status": "done", "quiz_time": "10:00 AM - 11:00 AM"},
        {"name": "History Quiz", "due_date": "2025-03-25", "status": "new", "quiz_time": "12:00 PM - 1:00 PM"},
        # Add more quizzes here with times when fetched from the database
    ]
    
    return rx.container(
        rx.hstack(  # Create a horizontal stack (two columns)
            rx.box(  # Quizzes (including both new and done)
                rx.vstack(
                    rx.text("All Quizzes", size="4", weight="bold"),
                    *[quiz_item(quiz["name"], quiz["due_date"], quiz["status"], quiz["quiz_time"]) for quiz in quizzes_list],
                    spacing="1",  # Space between items
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
            spacing="2",  # Increase space between columns
            justify="center",  # Center both boxes horizontally
            width="100%",  # Ensure the container takes up full width
        ),
        width="100%",  # Ensure the container takes up full width
        padding="2em",  # Add padding around the container
        position="relative",  # Position parent relative to allow "top" positioning
        top="7rem",  # Adds space from the top of the screen/container
        overflow="hidden",  # Prevent scrolling for the whole page
        margin_left="7rem",
    )
