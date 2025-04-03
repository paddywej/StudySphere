import reflex as rx
import requests
from typing import List, Dict  # Add this import statement

def fetch_assignments_data() -> list:
    """Simulate fetching multiple assignments data from a backend."""
    # Simulate an API request to get the assignment data
    # Example of how you might get the assignment data from an API or database:
    # response = requests.get(f"http://example.com/api/assignments/")
    # return response.json()
    
    # Mock data for simulation purposes:
    assignments_data = [
        {
            "assignment_name": "Math Assignment 1",
            "due_date": "2025-09-03",
            "students": [
                {"name": "Student 1", "file": "Assignment1.pdf"},
                {"name": "Student 2", "file": "Assignment1.pdf"},
            ]
        },
        {
            "assignment_name": "Science Project 1",
            "due_date": "2025-11-03",
            "students": [
                {"name": "Student A", "file": "Project1.pdf"},
                {"name": "Student B", "file": "Project1.pdf"},
            ]
        }
    ]
    return assignments_data

# In your State class:
class State(rx.State):
    assignment_to_delete: str = ""
    assignments: list[dict[str, list[dict[str, str]]]] = fetch_assignments_data()   
    edited_assignment_name: str = ""
    edited_due_date: str = ""

    def add_assignment(self, form_data: dict):
    # Ensure the assignments list is updated properly to trigger UI refresh
        self.assignments = self.assignments + [{
            "assignment_name": form_data["assignment_name"],
            "due_date": form_data["due_date"],
            "students": []  # You may need to handle file uploads properly here
        }]
        return rx.toast.info(
            f"Assignment {form_data['assignment_name']} has been added.",
            position="bottom-right",
        )


    def delete_assignment(self):
        # Filter out the assignment with matching name and update state
        self.assignments = [
            a for a in self.assignments 
            if a["assignment_name"] != self.assignment_to_delete
        ]
        return rx.toast.info(
            f"Assignment {self.assignment_to_delete} has been deleted.",
            position="bottom-right",
        )
    
    def set_edited_assignment_name(self, value: str):
        self.edited_assignment_name = value

    def set_edited_due_date(self, value: str):
        self.edited_due_date = value

    def edit_assignment(self):
        """Update the assignment details."""
        for assignment in self.assignments:
            if assignment["assignment_name"] == self.edited_assignment_name:  # Match by name
                assignment["assignment_name"] = self.edited_assignment_name
                assignment["due_date"] = self.edited_due_date
                break
        return rx.toast.success(
            f"Assignment {self.edited_assignment_name} updated.",
            position="bottom-right",
        )



def create_assignment_container(assignment_title: str, due_date: str, student_data: List[Dict[str, str]]) -> rx.Component:
    return rx.box(
        rx.vstack(
            # Assignment Title and Due Date
            rx.hstack(
                rx.text(f"{assignment_title} - {due_date}", font_size="20px", font_weight="bold", color="black"),
                
                # Edit Button that triggers a pop-up dialog
                rx.alert_dialog.root(
                    rx.alert_dialog.trigger(
                        rx.button("Edit", bg="#6EA9C5", color="white", border_radius="8px", cursor="pointer"),
                    ),
                    rx.alert_dialog.content(
                        rx.alert_dialog.title("Edit Assignment"),
                        rx.alert_dialog.description("Modify the assignment details"),
                        rx.vstack(
                            rx.input(
                                placeholder="New Assignment Name",
                                on_change=State.set_edited_assignment_name,
                                value=State.edited_assignment_name,
                            ),
                            rx.input(
                                placeholder="New Due Date",
                                type="date",
                                on_change=State.set_edited_due_date,
                                value=State.edited_due_date,
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
                                        on_click=State.edit_assignment,  # Update the assignment on Save
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




def all_assignments() -> rx.Component:
    """Creates the main assignments page layout with scrollable containers."""
    return rx.box(
        rx.vstack(
            rx.text("Assignments", font_size="35px", font_weight="bold", color="#598da2", text_align="center"),
            
            # Buttons on a new line
            rx.hstack(
                # Add Assignment Dialog
                rx.alert_dialog.root(
                    rx.alert_dialog.trigger(
                        rx.button("Add Assignments", bg="#6EA9C5", color="white", border_radius="8px", cursor="pointer"),
                    ),
                    rx.alert_dialog.content(
                        rx.alert_dialog.title("Add Assignment"),
                        rx.alert_dialog.description("Fill in the assignment details"),
                        rx.form(
                            rx.flex(
                                rx.input(
                                    placeholder="Assignment Name",
                                    name="assignment_name", 
                                    required=True
                                ),
                                rx.input(
                                    placeholder="Due Date",
                                    name="due_date",
                                    type="date",
                                    required=True
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
                            on_submit=State.add_assignment,
                            reset_on_submit=True,
                        ),
                        max_width="450px",
                    ),
                ),
                
                # Delete Assignment Dialog
                rx.alert_dialog.root(
                    rx.alert_dialog.trigger(
                        rx.button("Delete Assignments", bg="#6EA9C5", color="white", border_radius="8px", cursor="pointer"),
                    ),
                    rx.alert_dialog.content(
                        rx.alert_dialog.title("Delete Assignment"),
                        rx.alert_dialog.description("Enter the name of the assignment you want to delete."),
                        rx.vstack(
                            rx.input(
                                placeholder="Assignment Name",
                                on_change=State.set_assignment_to_delete,
                                value=State.assignment_to_delete,
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
                                        on_click=State.delete_assignment,
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

            # Assignments list
            rx.vstack(
                rx.foreach(
                    State.assignments,
                    lambda assignment: create_assignment_container(
                        assignment["assignment_name"],  # Pass assignment_name
                        assignment["due_date"],         # Pass due_date
                        assignment["students"],         # Pass students list
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
