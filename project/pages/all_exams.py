import reflex as rx
import requests

def fetch_exams_data() -> list:
    """Simulate fetching multiple exams data from a backend."""
    exams_data = [
        {
            "exam_name": "Math Final Exam",
            "due_date": "2025-09-03",
            "students": [
                {"name": "Student 1", "file": "FinalExam1.pdf"},
                {"name": "Student 2", "file": "FinalExam1.pdf"},
            ]
        },
        {
            "exam_name": "Science Midterm", 
            "due_date": "2025-11-03",
            "students": [
                {"name": "Student A", "file": "Midterm1.pdf"},
                {"name": "Student B", "file": "Midterm1.pdf"},
            ]
        }
    ]
    return exams_data

def create_exam_container(exam_title: str, due_date: str, student_data: list) -> rx.Component:
    """Creates a scrollable container with student exam data."""
    return rx.box(
        rx.text(f"{exam_title} - {due_date}", font_size="24px", font_weight="bold", color="black", text_align="center", margin_bottom="1rem"),
        rx.vstack(
            *[
                rx.hstack(
                    rx.box(
                        rx.text(student["name"], font_size="16px"),
                        width="33%",
                        padding="10px",
                        background_color="#effaff",
                        color="black",
                        border_radius="4px",
                        height="50px",
                        display="flex",
                        align_items="center",
                        justify_content="center"
                    ),
                    rx.box(
                        rx.text(student["file"], font_size="16px"),
                        width="33%",
                        padding="10px",
                        background_color="#effaff",
                        color="black",
                        border_radius="4px",
                        height="50px",
                        display="flex",
                        align_items="center",
                        justify_content="center"
                    ),
                    rx.box(
                        rx.input(placeholder="Enter score", width="100%", bg="white", border_radius="4px", color="black"),
                        width="33%",
                        padding="10px",
                        background_color="#effaff",
                        border_radius="4px",
                        height="50px",
                        display="flex",
                        align_items="center",
                        justify_content="center"
                    ),
                    spacing="2",
                    align="center"
                ) for student in student_data
            ],
            spacing="2",
            align_items="center"
        ),
        height="450px",
        width="100%",
        background_color="#cfe2eb",
        border_radius="10px",
        padding="20px",
        overflow_y="scroll",
    )

class State(rx.State):
    exam_to_delete: str = ""
    exams: list[dict] = []

    def add_exam(self, form_data: dict):
        self.exams.append(form_data)
        return rx.toast.info(
            f"Exam {form_data['exam_name']} has been added.",
            position="bottom-right",
        )

    def delete_exam(self):
        self.exams = [
            e for e in self.exams 
            if e["exam_name"] != self.exam_to_delete
        ]
        return rx.toast.info(
            f"Exam {self.exam_to_delete} has been deleted.",
            position="bottom-right",
        )
        
def all_exams() -> rx.Component:
    """Creates the main exams page layout with scrollable containers."""
    exams_data = fetch_exams_data()
    
    return rx.box(
        rx.vstack(
            rx.text("Exams", font_size="35px", font_weight="bold", color="#598da2", text_align="center"),
            
            rx.hstack(
                rx.alert_dialog.root(
                    rx.alert_dialog.trigger(
                        rx.button("Add Exam", bg="#6EA9C5", color="white", border_radius="8px", cursor="pointer"),
                    ),
                    rx.alert_dialog.content(
                        rx.alert_dialog.title("Add Exam"),
                        rx.alert_dialog.description("Fill in the exam details"),
                        rx.form(
                            rx.flex(
                                rx.input(
                                    placeholder="Exam Name",
                                    name="exam_name", 
                                    required=True
                                ),
                                rx.input(
                                    placeholder="Due Date",
                                    name="due_date",
                                    type="date",
                                    required=True
                                ),
                                rx.input(
                                    type="file",
                                    name="file",
                                    accept=".pdf,.doc,.docx"
                                ),
                                rx.flex(
                                    rx.alert_dialog.cancel(
                                        rx.button(
                                            "Cancel",
                                            variant="soft",
                                            color_scheme="gray",
                                        ),
                                    ),
                                    rx.alert_dialog.action(
                                        rx.button(
                                            "Submit",
                                            type="submit"
                                        ),
                                    ),
                                    spacing="3",
                                    justify="end",
                                ),
                                direction="column",
                                spacing="4",
                            ),
                            on_submit=State.add_exam,
                            reset_on_submit=True,
                        ),
                        max_width="450px",
                    ),
                ),
                
                rx.alert_dialog.root(
                    rx.alert_dialog.trigger(
                        rx.button("Delete Exam", bg="#6EA9C5", color="white", border_radius="8px", cursor="pointer"),
                    ),
                    rx.alert_dialog.content(
                        rx.alert_dialog.title("Delete Exam"),
                        rx.alert_dialog.description("Enter the name of the exam you want to delete."),
                        rx.vstack(
                            rx.input(
                                placeholder="Exam Name",
                                on_change=State.set_exam_to_delete,
                                value=State.exam_to_delete,
                            ),
                            rx.flex(
                                rx.alert_dialog.cancel(
                                    rx.button(
                                        "Cancel",
                                        variant="soft",
                                        color_scheme="gray", 
                                    ),
                                ),
                                rx.alert_dialog.action(
                                    rx.button(
                                        "Delete",
                                        color_scheme="red",
                                        on_click=State.delete_exam,
                                    ),
                                ),
                                spacing="3",
                                justify="end",
                            ),
                            spacing="4",
                        ),
                        max_width="450px",
                    ),
                ),
                spacing="4",
                justify="center", 
                width="100%",
                margin_top="1rem"
            ),

            rx.vstack(
                *[
                    create_exam_container(
                        exam["exam_name"],
                        exam["due_date"],
                        exam["students"]
                    ) for exam in exams_data
                ],
                spacing="6",
                align="center"
            ),
            spacing="6",
            align_items="center"
        ),
        width="100%",
        min_height="100vh", 
        display="flex",
        justify_content="center",
        align_items="center",
        margin_left="4rem",
        padding_top="7rem",
    )