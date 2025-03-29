import reflex as rx

def grade_row(subject: str, score: int | None, grade: str | None) -> rx.Component:
    return rx.hstack(
        rx.box(subject, width="33%", padding="12px", border="1px solid #ddd", bg="#f9f9f9", border_radius="8px", text_align="center"),
        rx.box(str(score) if score is not None else "-", width="33%", padding="12px", border="1px solid #ddd", bg="#f4f4f4", border_radius="8px", text_align="center"),
        rx.box(grade if grade is not None else "-", width="33%", padding="12px", border="1px solid #ddd", bg="#f9f9f9", border_radius="8px", text_align="center"),
    )

def grades() -> rx.Component:
    subjects = ["Software Engineering Principles", "Computer Networks", "Linear Algebra", "ADA"]
    scores = {"Software Engineering Principles": 85, "Computer Networks": 90, "Linear Algebra": None, "ADA": None}
    grades = {"Software Engineering Principles": "B", "Computer Networks": "A", "Linear Algebra": None, "ADA": None}
    
    return rx.container(
        rx.vstack(
            rx.text("Grades", size="6", weight="bold", color="#2C3E50"),
            rx.box(
                rx.hstack(
                    rx.box("Subject", width="33%", padding="12px", border="1px solid #ddd", bg="#3498db", color="white", font_weight="bold", text_align="center", border_radius="8px"),
                    rx.box("Score", width="33%", padding="12px", border="1px solid #ddd", bg="#3498db", color="white", font_weight="bold", text_align="center", border_radius="8px"),
                    rx.box("Grade", width="33%", padding="12px", border="1px solid #ddd", bg="#3498db", color="white", font_weight="bold", text_align="center", border_radius="8px"),
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
        ),
        width="80%",
        padding="2em",
        bg="#E8F0FE",
        border_radius="12px",
        min_height="60vh",
        shadow="xl",
        align_items="center"
    )
