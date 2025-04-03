import reflex as rx
import requests

def fetch_quizzes_data() -> list:
    """Simulate fetching multiple quiz data from a backend."""
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
                {"name": "Student A", "file": "Quiz2.pdf"},
                {"name": "Student B", "file": "Quiz2.pdf"},
            ]
        }
    ]
    return quizzes_data

# In your State class:
class State(rx.State):
    quiz_to_delete: str = ""
    quizzes: list[dict[str, list[dict[str, str]]]] = fetch_quizzes_data()

    def add_quiz(self, form_data: dict):
        # Add a new quiz to the list
        self.quizzes = self.quizzes + [{
            "quiz_name": form_data["quiz_name"],
            "due_date": form_data["due_date"],
            "students": [],  # You may need to handle student file uploads properly here
        }]
        return rx.toast.info(
            f"Quiz {form_data['quiz_name']} has been added.",
            position="bottom-right",
        )

    def delete_quiz(self):
        # Filter out the quiz with matching name and update state
        self.quizzes = [
            q for q in self.quizzes 
            if q["quiz_name"] != self.quiz_to_delete
        ]
        return rx.toast.info(
            f"Quiz {self.quiz_to_delete} has been deleted.",
            position="bottom-right",
        )

def create_quiz_container(quiz_title: str, due_date: str, student_data: list, file_name: str) -> rx.Component:
    return rx.box(
        rx.text(f"{quiz_title} - {due_date}", font_size="24px", font_weight="bold", color="black", text_align="center", margin_bottom="1rem"),

        # Professor's file section
        rx.box(
            rx.text(f"Professor's File: {file_name}", font_size="16px", font_style="italic", color="gray"),
            padding="10px",
            background_color="#f0f0f0",
            border_radius="6px",
            margin_bottom="1rem",
            width="100%",
            text_align="center",
        ),

        rx.vstack(
            rx.foreach(
                student_data,
                lambda student: rx.hstack(
                    rx.box(rx.text(student["name"], font_size="16px"), width="33%", padding="10px", background_color="#effaff", color="black", border_radius="4px", height="50px", display="flex", align_items="center", justify_content="center"),
                    rx.box(rx.text(student["file"], font_size="16px"), width="33%", padding="10px", background_color="#effaff", color="black", border_radius="4px", height="50px", display="flex", align_items="center", justify_content="center"),
                    rx.box(rx.input(placeholder="Enter score", width="100%", bg="white", border_radius="4px", color="black"), width="33%", padding="10px", background_color="#effaff", border_radius="4px", height="50px", display="flex", align_items="center", justify_content="center"),
                    spacing="2", align="center"
                )
            ),
            spacing="2", align_items="center"
        ),
        height="450px",
        width="100%",
        background_color="#cfe2eb",
        border_radius="10px",
        padding="20px",
        overflow_y="scroll",
    )

def all_quizzes() -> rx.Component:
    """Creates the main quizzes page layout with scrollable containers."""
    return rx.box(
        rx.vstack(
            # Title section
            rx.text("Quizzes", font_size="35px", font_weight="bold", color="#598da2", text_align="center"),
            
            # Buttons on a new line
            rx.hstack(
                # Add Quiz Dialog
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
                                    accept=".pdf,.doc,.docx,.png,.py,.zip"
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
                
                # Delete Quiz Dialog
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

            # Quizzes list - Use rx.foreach to dynamically render the quizzes
            rx.vstack(
                rx.foreach(
                    State.quizzes,
                    lambda quiz: create_quiz_container(
                        quiz["quiz_name"],
                        quiz["due_date"],
                        quiz["students"],
                        quiz["file_name"]  # No need for `.get()` anymore
                    ),
                ),
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