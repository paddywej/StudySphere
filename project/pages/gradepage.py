import reflex as rx
from typing import Optional

def grade_row(id: str, subject: str, score: Optional[int], grade: Optional[str], column_widths: dict) -> rx.Component:
    return rx.hstack(
        rx.box(id, padding="12px", border="1px solid #ddd", bg="#f9f9f9", 
               border_radius="8px", text_align="center", white_space="nowrap", overflow="hidden", text_overflow="ellipsis", 
               width=column_widths["id"]),
        rx.box(subject, padding="12px", border="1px solid #ddd", bg="#f9f9f9", 
               border_radius="8px", text_align="center", white_space="nowrap", overflow="hidden", text_overflow="ellipsis", 
               width=column_widths["subject"]),
        rx.box(str(score) if score is not None else "-", width=column_widths["score"], padding="12px", border="1px solid #ddd", 
               bg="#f4f4f4", border_radius="8px", text_align="center"),
        rx.box(grade if grade is not None else "-", width=column_widths["grade"], padding="12px", border="1px solid #ddd", 
               bg="#f9f9f9", border_radius="8px", text_align="center"),
    )

def grades() -> rx.Component:
    subject_id = ["10000", "10001", "10002", "10003"]
    subjects = {"10000": "Mathematics", "10001": "Science", "10002": "English", "10003": "History"}
    scores = {"10000": 85, "10001": 90, "10002": None, "10003": None}
    grades = {"10000": "B", "10001": "A", "10002": None, "10003": None}
    
    column_widths = {
        "id": "120px",
        "subject": "180px",
        "score": "100px",
        "grade": "100px",
    }

    return rx.center(
        rx.vstack(
            rx.text("Grades", size="6", weight="bold", color="#598da2"),
            rx.box(
                rx.hstack(
                    rx.box("Subject ID", padding="12px", border="1px solid #ddd", bg="#598da2", 
                           color="white", font_weight="bold", text_align="center", border_radius="8px", 
                           width=column_widths["id"]),
                    rx.box("Subject", padding="12px", border="1px solid #ddd", bg="#598da2", 
                           color="white", font_weight="bold", text_align="center", border_radius="8px", 
                           width=column_widths["subject"]),
                    rx.box("Score", padding="12px", border="1px solid #ddd", bg="#598da2", 
                           color="white", font_weight="bold", text_align="center", border_radius="8px", 
                           width=column_widths["score"]),
                    rx.box("Grade", padding="12px", border="1px solid #ddd", bg="#598da2", 
                           color="white", font_weight="bold", text_align="center", border_radius="8px", 
                           width=column_widths["grade"]),
                ),
                *[grade_row(id, subjects.get(id), scores.get(id), grades.get(id), column_widths) for id in subject_id],
                border="1px solid #ddd",
                width="100%",
                border_radius="10px",
                overflow="hidden",
                shadow="lg",
                padding="10px",
                bg="white"
            ),
            rx.hstack(
                rx.link(
                    rx.button(
                        "Add Score", 
                        padding="15px", 
                        background_color="#6EA9C5", 
                        color="white", 
                        width="150px", 
                        height="50px", 
                        border_radius="10px", 
                        weight="bold"
                    ),
                    href="/add_score",
                ),
                rx.link(
                    rx.button(
                        "Edit Score", 
                        padding="15px", 
                        background_color="#6EA9C5", 
                        color="white", 
                        width="150px", 
                        height="50px", 
                        border_radius="10px", 
                        weight="bold"
                    ),
                    href="/edit_score",
                ),
                spacing="6",
                justify="center",
                align_items="center",
                margin_top="20px",
                width="100%",
            ),
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
