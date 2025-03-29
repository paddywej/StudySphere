import reflex as rx

def exam_item(exam_id: str, name: str, exam_date: str, status: str, exam_time: str) -> rx.Component:
    # Status-based background colors
    status_colors = {
        "upcoming": "#EFFAFF",  # Light blue for upcoming exams
        "completed": "#D3F8E2",  # Light green for completed exams
    }
    
    return rx.link(
        rx.box(
            rx.vstack(
                rx.text(f"{name}", size="3", weight="bold"),
                rx.text(f"Date: {exam_date}", size="2"),
                rx.text(f"Time: {exam_time}"),
                rx.text(f"Status: {status.capitalize()}", size="2", color="gray"),
                spacing="1",
            ),
            bg=status_colors.get(status, "#EFFAFF"),
            color="black",
            padding="1em",
            border_radius="8px",
            width="100%",
            margin_bottom="1em",
            shadow="md",
            _hover={"bg": "#BFD9E5"},
        ),
        href=f"/exam_details/{exam_id}",  # Dynamic link to exam detail page
        width="100%",
        text_decoration="none",
    )

# Exam data
exams_list = [
    {"id": "math_final_1", "name": "Mathematics Final 1", "exam_date": "2025-05-10", "status": "upcoming", "exam_time": "09:00 AM - 11:00 AM"},
    {"id": "math_midterm", "name": "Mathematics Midterm", "exam_date": "2025-04-15", "status": "completed", "exam_time": "02:00 PM - 04:00 PM"},
    {"id": "math_final_2", "name": "Mathematics Final 2", "exam_date": "2025-06-01", "status": "upcoming", "exam_time": "10:00 AM - 12:00 PM"},
]

def exam() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.box(
                rx.vstack(
                    rx.text("Upcoming Exams", size="4", weight="bold"),
                    *[exam_item(exam["id"], exam["name"], exam["exam_date"], exam["status"], exam["exam_time"]) for exam in exams_list if exam["status"] == "upcoming"],
                    spacing="1",
                    width="100%",
                ),
                width="45%",
                height="500px",
                bg="#D0E2EB",
                color="black",
                padding="1em",
                overflow="auto",
                border_radius="25px",
                margin_right="2rem",
            ),
            rx.box(
                rx.vstack(
                    rx.text("Completed Exams", size="4", weight="bold"),
                    *[exam_item(exam["id"], exam["name"], exam["exam_date"], exam["status"], exam["exam_time"]) for exam in exams_list if exam["status"] == "completed"],
                    spacing="1",
                    width="100%",
                ),
                width="45%",
                height="500px",
                bg="#D0E2EB",
                color="black",
                padding="1em",
                overflow="auto",
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
