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

class State(rx.State):
    quiz_to_delete: str = ""
    quizzes: list[dict[str, list[dict[str, str]]]] = fetch_quizzes_data()
    edited_quiz_name: str = ""
    edited_due_date: str = ""

    def add_quiz(self, form_data: dict):
        self.quizzes = self.quizzes + [{
            "quiz_name": form_data["quiz_name"],
            "due_date": form_data["due_date"],
            "students": []
        }]
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

    def set_quiz_to_delete(self, value: str):
        self.quiz_to_delete = value
        
    def set_edited_quiz_name(self, value: str):
        self.edited_quiz_name = value

    def set_edited_due_date(self, value: str):
        self.edited_due_date = value

    def edit_quiz(self):
        for quiz in self.quizzes:
            if quiz["quiz_name"] == self.edited_quiz_name:
                quiz["quiz_name"] = self.edited_quiz_name
                quiz["due_date"] = self.edited_due_date
                break
        return rx.toast.success(
            f"Quiz updated to {self.edited_quiz_name}.",
            position="bottom-right",
        )

    def submit_grades(self):
        return rx.toast.success(
            "Grades submitted successfully.",
            position="bottom-right",
        )

def create_quiz_container(quiz_title: str, due_date: str, student_data: list, file_name: str = "No file uploaded") -> rx.Component:
    return rx.box(
        rx.vstack(
            # Quiz Title and Due Date in one row
            rx.hstack(
                rx.text(f"{quiz_title} - {due_date}", font_size="20px", font_weight="bold", color="black"),
                rx.spacer(),
                
                # Edit Button with dialog
                rx.alert_dialog.root(
                    rx.alert_dialog.trigger(
                        rx.button("Edit", bg="#6EA9C5", color="white", border_radius="8px", cursor="pointer"),
                    ),
                    rx.alert_dialog.content(
                        rx.alert_dialog.title("Edit Quiz"),
                        rx.alert_dialog.description("Modify the quiz details"),
                        rx.vstack(
                            rx.input(
                                placeholder="New Quiz Name",
                                on_change=State.set_edited_quiz_name,
                                value=State.edited_quiz_name,
                            ),
                            rx.input(
                                placeholder="New Due Date",
                                type="date",
                                on_change=State.set_edited_due_date,
                                value=State.edited_due_date,
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
                                        "Save Changes",
                                        color_scheme="blue",
                                        on_click=State.edit_quiz,
                                    ),
                                    justify="space-between",
                                ),
                                spacing="3",
                                justify="end",
                            ),
                            spacing="4",
                        ),
                        max_width="450px",
                    ),
                ),
                width="100%",
                align_items="center",
                justify_content="space-between",
            ),

            # Professor's file section
            rx.box(
                rx.text(f"Professor's File: {file_name}", font_size="16px", font_style="italic", color="gray"),
                padding="10px",
                background_color="#f0f0f0",
                border_radius="6px",
                margin_bottom="1rem",
                margin_top="0.5rem",
                width="100%",
                text_align="left",
            ),

            # Student List
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
                spacing="2",
                align_items="center"
            ),

            # Submit Grades button at bottom right
            rx.hstack(
                rx.spacer(),
                rx.alert_dialog.root(
                    rx.alert_dialog.trigger(
                        rx.button(
                            "Submit Grades",
                            bg="#6EA9C5",
                            color="white",
                            border_radius="8px",
                            cursor="pointer"
                        ),
                    ),
                    rx.alert_dialog.content(
                        rx.alert_dialog.title("Submit Grades"),
                        rx.alert_dialog.description(
                            "Are you sure you want to submit the grades?"
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
                                    color_scheme="blue",
                                    on_click=State.submit_grades,
                                ),
                            ),
                            spacing="3",
                            justify="end",
                        ),
                    ),
                ),
                width="100%",
                padding="10px",
                margin_top="1rem",
            ),
        ),
        height="450px",
        width="100%",
        background_color="#cfe2eb",
        border_radius="10px",
        padding="20px",
        overflow_y="scroll",
    )

def all_quizzes() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text("Quizzes", font_size="35px", font_weight="bold", color="#598da2", text_align="center"),
            
            # Action buttons
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

            # Quizzes list
            rx.vstack(
                rx.foreach(
                    State.quizzes,
                    lambda quiz: create_quiz_container(
                        quiz["quiz_name"],
                        quiz["due_date"],
                        quiz["students"],
                        quiz.get("file_name", "No file uploaded")
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