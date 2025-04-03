import reflex as rx
from typing import List, Dict

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

class State(rx.State):
    quiz_to_delete: str = ""
    quizzes: list[dict[str, list[dict[str, str]]]] = fetch_quizzes_data()
    edited_quiz_name: str = ""
    edited_due_date: str = ""

    def add_quiz(self, form_data: dict):
        """Add a new quiz and trigger re-render"""
        self.quizzes = self.quizzes + [{
            "quiz_name": form_data["quiz_name"],
            "due_date": form_data["due_date"],
            "students": []  # Handle file uploads if needed
        }]
        return rx.toast.info(
            f"Quiz {form_data['quiz_name']} has been added.",
            position="bottom-right",
        )

    def delete_quiz(self):
        """Delete a quiz and trigger re-render"""
        self.quizzes = [
            q for q in self.quizzes
            if q["quiz_name"] != self.quiz_to_delete
        ]
        return rx.toast.info(
            f"Quiz {self.quiz_to_delete} has been deleted.",
            position="bottom-right",
        )

    def set_edited_quiz_name(self, value: str):
        self.edited_quiz_name = value

    def set_edited_due_date(self, value: str):
        self.edited_due_date = value

    def edit_quiz(self):
        """Update the quiz details in the state"""
        # Find the quiz that needs to be edited
        for quiz in self.quizzes:
            if quiz["quiz_name"] == self.edited_quiz_name:
                # Update the quiz details
                quiz["quiz_name"] = self.edited_quiz_name
                quiz["due_date"] = self.edited_due_date
                break
        
        # After editing, trigger a success message
        return rx.toast.success(
            f"Quiz updated to {self.edited_quiz_name}.",
            position="bottom-right",
        )


def create_quiz_container(quiz_title: str, due_date: str, student_data: List[Dict[str, str]], file_name: str = "No file uploaded") -> rx.Component:
    """Creates a container for each quiz with editable options."""
    return rx.box(
        rx.vstack(
            # Quiz Title and Due Date in one row
            rx.hstack(
                rx.text(f"{quiz_title} - {due_date}", font_size="20px", font_weight="bold", color="black"),
                # Add spacer to push edit button to the right
                rx.spacer(),
                
                # Edit Button that triggers a pop-up dialog
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
                                        on_click=State.edit_quiz,  # Update the quiz on Save
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
                # Set width to full to ensure hstack takes entire container width
                width="100%",
                # Ensure alignment of items within hstack
                align_items="center",
                justify_content="space-between",
            ),
            
            # Professor's file section below the title
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
            
            # Student List (Student ID, File, Score)
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

            # Quizzes list
            rx.vstack(
                rx.foreach(State.quizzes, lambda quiz: create_quiz_container(quiz["quiz_name"], quiz["due_date"], quiz["students"])),
                spacing="4",
                align_items="center",
            ),
        ),
        height="100vh", 
        overflow_y="scroll", 
        padding="20px", 
        background_color="#e0f7fa", 
    )
