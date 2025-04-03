import reflex as rx
from typing import List, Dict

def fetch_exams_data() -> list:
    """Simulate fetching multiple exams data from a backend."""
    exams_data = [
        {
            "exam_name": "Math Exam 1",
            "due_date": "2025-09-03",
            "students": [
                {"name": "Student 1", "file": "Exam1.pdf"},
                {"name": "Student 2", "file": "Exam1.pdf"},
            ]
        },
        {
            "exam_name": "Science Project 1",
            "due_date": "2025-11-03",
            "students": [
                {"name": "Student A", "file": "Project1.pdf"},
                {"name": "Student B", "file": "Project1.pdf"},
            ]
        }
    ]
    return exams_data

class State(rx.State):
    exam_to_delete: str = ""
    exams: list[dict[str, list[dict[str, str]]]] = fetch_exams_data()
    edited_exam_name: str = ""
    edited_due_date: str = ""

    def add_exam(self, form_data: dict):
        """Add a new exam and trigger re-render"""
        self.exams = self.exams + [{
            "exam_name": form_data["exam_name"],
            "due_date": form_data["due_date"],
            "students": []  # Handle file uploads if needed
        }]
        return rx.toast.info(
            f"Exam {form_data['exam_name']} has been added.",
            position="bottom-right",
        )

    def delete_exam(self):
        """Delete an exam and trigger re-render"""
        self.exams = [
            e for e in self.exams
            if e["exam_name"] != self.exam_to_delete
        ]
        return rx.toast.info(
            f"Exam {self.exam_to_delete} has been deleted.",
            position="bottom-right",
        )

    def set_edited_exam_name(self, value: str):
        self.edited_exam_name = value

    def set_edited_due_date(self, value: str):
        self.edited_due_date = value

    def edit_exam(self):
        """Update the exam details in the state"""
        # Find the exam that needs to be edited
        for exam in self.exams:
            if exam["exam_name"] == self.edited_exam_name:
                # Update the exam details
                exam["exam_name"] = self.edited_exam_name
                exam["due_date"] = self.edited_due_date
                break
        
        # After editing, trigger a success message
        return rx.toast.success(
            f"Exam updated to {self.edited_exam_name}.",
            position="bottom-right",
        )


def create_exam_container(exam_title: str, due_date: str, student_data: List[Dict[str, str]], file_name: str = "No file uploaded") -> rx.Component:
    """Creates a container for each exam with editable options."""
    return rx.box(
        rx.vstack(
            # Exam Title and Due Date in one row
            rx.hstack(
                rx.text(f"{exam_title} - {due_date}", font_size="20px", font_weight="bold", color="black"),
                # Add spacer to push edit button to the right
                rx.spacer(),
                
                # Edit Button that triggers a pop-up dialog
                rx.alert_dialog.root(
                    rx.alert_dialog.trigger(
                        rx.button("Edit", bg="#6EA9C5", color="white", border_radius="8px", cursor="pointer"),
                    ),
                    rx.alert_dialog.content(
                        rx.alert_dialog.title("Edit Exam"),
                        rx.alert_dialog.description("Modify the exam details"),
                        rx.vstack(
                            rx.input(
                                placeholder="New Exam Name",
                                on_change=State.set_edited_exam_name,
                                value=State.edited_exam_name,
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
                                        on_click=State.edit_exam,  # Update the exam on Save
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


def all_exams() -> rx.Component:
    """Creates the main exams page layout with scrollable containers."""
    return rx.box(
        rx.vstack(
            rx.text("Exams", font_size="35px", font_weight="bold", color="#598da2", text_align="center"),
            
            # Buttons on a new line
            rx.hstack(
                # Add Exam Dialog
                rx.alert_dialog.root(
                    rx.alert_dialog.trigger(
                        rx.button("Add Exams", bg="#6EA9C5", color="white", border_radius="8px", cursor="pointer"),
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
                            on_submit=State.add_exam,
                            reset_on_submit=True,
                        ),
                        max_width="450px",
                    ),
                ),
                
                # Delete Exam Dialog
                rx.alert_dialog.root(
                    rx.alert_dialog.trigger(
                        rx.button("Delete Exams", bg="#6EA9C5", color="white", border_radius="8px", cursor="pointer"),
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

            # Exams list
            rx.vstack(
                rx.foreach(
                    State.exams,
                    lambda exam: create_exam_container(
                        exam["exam_name"],  # Pass exam_name
                        exam["due_date"],         # Pass due_date
                        exam["students"],         # Pass students list
                        exam["file_name"]  # No need for `.get()` anymore

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
