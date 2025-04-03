import reflex as rx

# Application State
class State(rx.State):
    students: list[str] = ["66011217 Josh", "66011213 David", "66011217 Olivia"] 

    @rx.event
    def add_students(self, form_data: dict):
        new_students = [id.strip() for id in form_data.get("student_ids", "").split(",") if id.strip()]
        
        added = []
        already_exists = []
        for student in new_students:
            if student not in self.students:
                self.students.append(student)
                added.append(student)
            else:
                already_exists.append(student)

        if added:
            return rx.toast.info(f"Added students: {', '.join(added)}", position="bottom-right")
        if already_exists:
            return rx.toast.warning(f"Already exists: {', '.join(already_exists)}", position="bottom-right")


    @rx.event
    def remove_students(self, form_data: dict):
        students_to_remove = [id.strip() for id in form_data.get("student_ids", "").split(",") if id.strip()]
        
        removed = []
        not_found = []
        for student in students_to_remove:
            if student in self.students:
                self.students.remove(student)
                removed.append(student)
            else:
                not_found.append(student)

        if removed:
            return rx.toast.info(f"Removed students: {', '.join(removed)}", position="bottom-right")
        if not_found:
            return rx.toast.warning(f"Not found: {', '.join(not_found)}", position="bottom-right")

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
                rx.foreach(State.students, student_item),
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
                        on_submit=State.add_students,
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
                        background_color="#598da2",
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
                        on_submit=State.remove_students,
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
    )
