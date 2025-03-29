import reflex as rx

def exam_item(name: str, exam_date: str, status: str, exam_time: str) -> rx.Component:
    # Dynamically create an exam item with status-based background color
    status_colors = {
        "upcoming": "#EFFAFF",  # Light blue for upcoming exams
        "completed": "#D3F8E2",  # Light green for completed exams
    }
    return rx.box(
        rx.vstack(
            rx.text(f"{name}", size="3", weight="bold"),
            rx.text(f"Date: {exam_date}", size="2"),
            rx.text(f"Time: {exam_time}"),
            rx.text(f"Status: {status.capitalize()}", size="2", color="gray"),
            spacing="1",  # Space between text lines
        ),
        bg=status_colors.get(status, "#EFFAFF"),  # Default to light blue for upcoming exams
        color="black",  # Text color
        padding="1em",
        border_radius="8px",  # Round corners
        width="100%",  # Full width of the box
        margin_bottom="1em",  # Space between items
        shadow="md",  # Optional shadow for the box
    )

def exam() -> rx.Component:
    # Sample list of exams to display
    exams_list = [
        {"name": "SEP Final", "exam_date": "2025-05-10", "status": "upcoming", "exam_time": "09:00 AM - 11:00 AM"},
        {"name": "Computer Network Final", "exam_date": "2025-04-15", "status": "completed", "exam_time": "02:00 PM - 04:00 PM"},
        {"name": "Linear Algebra Final", "exam_date": "2025-06-01", "status": "upcoming", "exam_time": "10:00 AM - 12:00 PM"},
        {"name": "ADA Final", "exam_date": "2025-05-10", "status": "upcoming", "exam_time": "09:00 AM - 11:00 AM"},
        {"name": "??? Final", "exam_date": "2025-05-10", "status": "upcoming", "exam_time": "09:00 AM - 11:00 AM"},
    ]
    
    return rx.container(
        rx.hstack(
            rx.box(
                rx.vstack(
                    rx.text("Upcoming Exams", size="4", weight="bold"),
                    *[exam_item(exam["name"], exam["exam_date"], exam["status"], exam["exam_time"]) for exam in exams_list if exam["status"] == "upcoming"],
                    spacing="1",
                    width="100%",
                ),
                width="45%",
                height="500px",
                bg="#D0E2EB",
                color="black",
                padding="1em",
                overflow="auto",  # Ensures the scrollbar appears when content exceeds the box height
                border_radius="25px",
                margin_right="2rem",
            ),
            rx.box(
                rx.vstack(
                    rx.text("Completed Exams", size="4", weight="bold"),
                    *[exam_item(exam["name"], exam["exam_date"], exam["status"], exam["exam_time"]) for exam in exams_list if exam["status"] == "completed"],
                    spacing="1",
                    width="100%",
                ),
                width="45%",
                height="500px",
                bg="#D0E2EB",
                color="black",
                padding="1em",
                overflow="auto",  # Ensures the scrollbar appears when content exceeds the box height
                border_radius="25px",
            ),
            spacing="4",
            justify="center",
            width="100%",
        ),
        width="100%",
        padding="2em",
        padding_top="7rem",
        margin_left="7rem",
        min_height="100vh",
        bg="white",
    )
