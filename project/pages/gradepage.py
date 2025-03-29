import reflex as rx

def grade_row(subject: str, score: int | None, grade: str | None) -> rx.Component:
    return rx.hstack(
        rx.box(subject, flex="1", padding="12px", border="1px solid #ddd", bg="#f9f9f9", 
               border_radius="8px", text_align="center", white_space="nowrap", overflow="hidden", text_overflow="ellipsis"),
        rx.box(str(score) if score is not None else "-", width="100px", padding="12px", border="1px solid #ddd", 
               bg="#f4f4f4", border_radius="8px", text_align="center"),
        rx.box(grade if grade is not None else "-", width="100px", padding="12px", border="1px solid #ddd", 
               bg="#f9f9f9", border_radius="8px", text_align="center"),
    )

def grades() -> rx.Component:
    subjects = ["Mathematics", "Science", "English", "History"]
    scores = {"Mathematics": 85, "Science": 90, "English": None, "History": None}
    grades = {"Mathematics": "B", "Science": "A", "English": None, "History": None}
    
    return rx.center(
        rx.vstack(
            rx.text("Grades", size="6", weight="bold", color="#2C3E50"),
            rx.box(
                rx.hstack(
                    rx.box("Subject", flex="1", padding="12px", border="1px solid #ddd", bg="#3498db", 
                           color="white", font_weight="bold", text_align="center", border_radius="8px"),
                    rx.box("Score", width="100px", padding="12px", border="1px solid #ddd", bg="#3498db", 
                           color="white", font_weight="bold", text_align="center", border_radius="8px"),
                    rx.box("Grade", width="100px", padding="12px", border="1px solid #ddd", bg="#3498db", 
                           color="white", font_weight="bold", text_align="center", border_radius="8px"),
                ),
                *[grade_row(sub, scores.get(sub), grades.get(sub)) for sub in subjects],
                border="1px solid #ddd",
                width="100%",
                border_radius="10px",
                overflow="hidden",
                shadow="lg",
                padding="10px",
                bg="white"
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
