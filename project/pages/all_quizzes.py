import reflex as rx
import requests

def fetch_quizzes_data() -> list:
    """Simulate fetching multiple quizzes data from a backend."""
    quizzes_data = [
        {
            "quiz_name": "Math Quiz 1",
            "due_date": "2025-09-03",
            "students": [
                {"name": "Student 1", "file": "Quiz1.pdf"},
                {"name": "Student 2", "file": "Quiz1.pdf"},
            ]
        },
        {
            "quiz_name": "Science Quiz 1", 
            "due_date": "2025-11-03",
            "students": [
                {"name": "Student A", "file": "Quiz1.pdf"},
                {"name": "Student B", "file": "Quiz1.pdf"},
            ]
        }
    ]
    return quizzes_data

def create_quiz_container(quiz_title: str, due_date: str, student_data: list) -> rx.Component:
    """Creates a scrollable container with student quiz data."""
    return rx.box(
        rx.text(f"{quiz_title} - {due_date}", font_size="24px", font_weight="bold", color="black", text_align="center", margin_bottom="1rem"),
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
                        rx.input(placeholder="Enter score", width="100%", bg="white", border_radius="4px"),
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
    quiz_to_delete: str = ""
    quizzes: list[dict] = []

    def add_quiz(self, form_data: dict):
        self.quizzes.append(form_data)
        return rx.toast.info(
            f"Quiz {form_data['quiz_name']} has been added.",
            position="bottom-right",
        )

    def delete_quiz(self):
        self.quizzes = [
            q for q in self.quizzes 
            if q["quiz_name"] != self.quiz_to_delete
        ]
        return rx.toast.info(
            f"Quiz {self.quiz_to_delete} has been deleted.",
            position="bottom-right",
        )
        
def all_quizzes() -> rx.Component:
    """Creates the main quizzes page layout with scrollable containers."""
    quizzes_data = fetch_quizzes_data()
    
    return rx.box(
        rx.vstack(
            rx.text("Quizzes", font_size="35px", font_weight="bold", color="#598da2", text_align="center"),
            
            rx.hstack(
                rx.alert_dialog.root(
                    rx.alert_dialog.trigger(
                        rx.button("Add Quiz", bg="#6EA9C5", color="white", border_radius="8px", cursor="pointer"),
                    ),
                    rx.alert_dialog.content(
                        rx.alert_dialog.title("Add Quiz"),
                        rx.alert_dialog.description("Fill in the quiz details"),
                        rx.form(
                            rx.flex(
                                rx.input(
                                    placeholder="Quiz Name",
                                    name="quiz_name", 
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
                            on_submit=State.add_quiz,
                            reset_on_submit=True,
                        ),
                        max_width="450px",
                    ),
                ),
                
                rx.alert_dialog.root(
                    rx.alert_dialog.trigger(
                        rx.button("Delete Quiz", bg="#6EA9C5", color="white", border_radius="8px", cursor="pointer"),
                    ),
                    rx.alert_dialog.content(
                        rx.alert_dialog.title("Delete Quiz"),
                        rx.alert_dialog.description("Enter the name of the quiz you want to delete."),
                        rx.vstack(
                            rx.input(
                                placeholder="Quiz Name",
                                on_change=State.set_quiz_to_delete,
                                value=State.quiz_to_delete,
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
                                        on_click=State.delete_quiz,
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
                    create_quiz_container(
                        quiz["quiz_name"],
                        quiz["due_date"],
                        quiz["students"]
                    ) for quiz in quizzes_data
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