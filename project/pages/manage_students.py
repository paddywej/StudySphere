import reflex as rx
import asyncio
from typing import Dict,List
import requests

# Application State
class ManageState(rx.State):
    student_list:list = []
    subject_id: str = ""
    new_students = ""
    
    @rx.event
    async def add_students(self, form_data: dict):
        new_students = [id.strip() for id in form_data.get("student_ids", "").split(",") if id.strip()]
        
        for student in new_students:
            if student not in self.student_list:
                url = f"http://localhost:8000/add_student/{self.subject_id}/{student}"
                response = await asyncio.to_thread(requests.put, url)  # POST to the API

                if response.status_code == 200:
                    await self.get_student_list()  # Re-fetch student list to reflect changes
                    print("added student:", student)
                    print("added student success")
                    print("student list", self.student_list)
                    yield rx.toast.success(f"Added students: {student}", position="bottom-right")
                else:
                    print(f"Error adding student {student}: {response.text}")
            else:
                # Assuming you want to show an error toast if student is already in list
                yield rx.toast.error(f"Student {student} already exists.", position="bottom-right")


    async def get_subject_id(self):
        url = f"http://localhost:8000/user_session/subject"
        response = await asyncio.to_thread(requests.get, url) 

        if response.status_code == 200:
            self.subject_id = response.json()
            print(self.subject_id)
            await self.get_student_list()
        else:
            print("error get subject_id by usersession")
    

    async def get_student_list(self):
        """Fetch student list for a given subject_id and store it in the student_list."""
        url = f"http://localhost:8000/get_student_list/{self.subject_id}"
        response = await asyncio.to_thread(requests.get, url)

        if response.status_code == 200:
            self.student_list = response.json()
            print("Fetch student_list:",self.student_list)
        else:
            self.student_list = []  # In case of error

    @rx.event
    async def remove_students(self, form_data: dict):
        """Remove multiple students using comma-separated IDs."""
        students_to_remove = [id.strip() for id in form_data.get("student_ids", "").split(",") if id.strip()]
        
        removed = []
        not_found = []
        for student in students_to_remove:
            if student in self.student_list:
                # Call API to remove student from the database
                url = f"http://localhost:8000/remove_student/{self.subject_id}/{student}"
                response = await asyncio.to_thread(requests.put, url)  # Use PUT to update the list

                if response.status_code == 200:
                    self.student_list.remove(student)
                    removed.append(student)
                else:
                    print(f"Error removing student {student}: {response.text}")
            else:
                not_found.append(student)

        if removed:
            yield rx.toast.success(f"Removed students: {', '.join(removed)}", position="bottom-right")
        if not_found:
            yield rx.toast.error(f"Students not found: {', '.join(not_found)}", position="bottom-right")


# Student Item Component
def student_item(student_id: str) -> rx.Component:
    return rx.box(
        rx.text(student_id, size="3"),
        bg="#EFFAFF",
        color="black",
        padding="1em",
        border_radius="8px",
        width="100%",
        margin_bottom="1em",
        shadow="md",
        _hover={"bg": "#BFD9E5"},
    )

# Manage Students Page
def manage_students() -> rx.Component:
    return rx.vstack(
        rx.box(
            rx.vstack(
                rx.text("Enrolled Students", size="4", weight="bold"),
                rx.foreach(ManageState.student_list, student_item),
                spacing="1",
                width="100%",
            ),
            width="45%",
            height="500px",
            bg="#D0E2EB",
            color="black",
            padding="1em",
            overflow="auto",
            border_radius="25px",
            margin_bottom="2rem",
        ),
        
        # Buttons for adding and removing students
        rx.hstack(
            # Add Student Dialog
            rx.alert_dialog.root(
                rx.alert_dialog.trigger(
                    rx.button(
                        "Add Students",
                        padding="15px",
                        background_color="#598da2",
                        color="white",
                        width="200px",
                        height="50px",
                        border_radius="10px",
                        weight="bold",
                    ),
                ),
                rx.alert_dialog.content(
                    rx.alert_dialog.title("Add Students"),
                    rx.alert_dialog.description("Enter student IDs separated by commas."),
                    rx.form(
                        rx.flex(
                            rx.text_area(
                                placeholder="xxxx, xxxx, xxxx",
                                name="student_ids",
                            ),
                            rx.flex(
                                rx.alert_dialog.cancel(
                                    rx.button("Cancel", variant="soft", color_scheme="gray"),
                                ),
                                rx.alert_dialog.action(
                                    rx.button("Submit", type="submit"),
                                ),
                                spacing="3",
                                justify="end",
                            ),
                            direction="column",
                            spacing="4",
                        ),
                        on_submit=ManageState.add_students,
                        reset_on_submit=True,
                    ),
                    max_width="450px",
                ),
            ),

            # Remove Student Dialog
            rx.alert_dialog.root(
                rx.alert_dialog.trigger(
                    rx.button(
                        "Remove Students",
                        padding="15px",
                        background_color="#A25B5B",
                        color="white",
                        width="200px",
                        height="50px",
                        border_radius="10px",
                        weight="bold",
                    ),
                ),
                rx.alert_dialog.content(
                    rx.alert_dialog.title("Remove Students"),
                    rx.alert_dialog.description("Enter student IDs to remove, separated by commas."),
                    rx.form(
                        rx.flex(
                            rx.text_area(
                                placeholder="xxxx, xxxx, xxxx",
                                name="student_ids",
                            ),
                            rx.flex(
                                rx.alert_dialog.cancel(
                                    rx.button("Cancel", variant="soft", color_scheme="gray"),
                                ),
                                rx.alert_dialog.action(
                                    rx.button("Submit", type="submit"),
                                    
                                ),
                                spacing="3",
                                justify="end",
                            ),
                            direction="column",
                            spacing="4",
                        ),
                        on_submit=ManageState.remove_students,
                        reset_on_submit=True,
                    ),
                    max_width="450px",
                ),
            ),

            spacing="2",
            justify="center",
            margin_top="5px",
        ),

        spacing="4",
        justify="center",
        align="center",
        width="100%",
        padding="2em",
        padding_top="7rem",
        margin_left="7rem",
        min_height="100vh",
        bg="white",
        on_mount=ManageState.get_subject_id
    )
