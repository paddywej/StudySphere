import reflex as rx
from typing import Optional

def grade_input_row(id: str, subject: str, column_widths: dict) -> rx.Component:
    return rx.hstack(
        rx.box(id, padding="12px", border="1px solid #ddd", bg="#f9f9f9", 
               border_radius="8px", text_align="center", width=column_widths["id"], height="40px"),
        rx.box(subject, padding="12px", border="1px solid #ddd", bg="#f9f9f9", 
               border_radius="8px", text_align="center", width=column_widths["subject"], height="40px"),
        rx.input(placeholder="Enter score", width=column_widths["score"], padding="10px", border_radius="8px", height="40px", font_size="16px"),
        rx.input(placeholder="Enter grade", width=column_widths["grade"], padding="10px", border_radius="8px", height="40px", font_size="16px"),
    )

def professor_grades() -> rx.Component:
    subject_id = ["10000", "10001", "10002", "10003"]
    subjects = {"10000": "Mathematics", "10001": "Science", "10002": "English", "10003": "History"}
    
    column_widths = {
        "id": "120px",
        "subject": "180px",
        "score": "120px",
        "grade": "120px",
    }

    return rx.center(
        rx.vstack(
            rx.text("Enter Student Grades", size="6", weight="bold", color="#598da2"),
            rx.box(
                rx.hstack(
                    rx.box("Subject ID", padding="12px", border="1px solid #ddd", bg="#598da2", 
                           color="white", font_weight="bold", text_align="center", border_radius="8px", 
                           width=column_widths["id"], height="40px"),
                    rx.box("Subject", padding="12px", border="1px solid #ddd", bg="#598da2", 
                           color="white", font_weight="bold", text_align="center", border_radius="8px", 
                           width=column_widths["subject"], height="40px"),
                    rx.box("Score", padding="12px", border="1px solid #ddd", bg="#598da2", 
                           color="white", font_weight="bold", text_align="center", border_radius="8px", 
                           width=column_widths["score"], height="40px"),
                    rx.box("Grade", padding="12px", border="1px solid #ddd", bg="#598da2", 
                           color="white", font_weight="bold", text_align="center", border_radius="8px", 
                           width=column_widths["grade"], height="40px"),
                ),
                *[grade_input_row(id, subjects.get(id), column_widths) for id in subject_id],
                border="1px solid #ddd",
                width="100%",
                border_radius="10px",
                overflow="hidden",
                shadow="lg",
                padding="10px",
                bg="white"
            ),
            rx.button("Submit Grades", bg="#598da2", color="white", padding="12px 24px", border_radius="8px"),
            spacing="6",
            align="center",
            justify="center",
        ),
        width="100%",
        padding="2em",
        margin_left="7rem",
        min_height="90vh",
        bg="white",
    )
