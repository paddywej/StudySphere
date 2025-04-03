import reflex as rx
import requests
from project.pages.login import FormState

class ProfState(rx.State):
    students: list[str] = ["66011217 Josh", "66011213 David", "66011217 Olivia"] 

    @rx.event
    def add_subject(self, form_data: dict):
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
            return rx.toast.info(f"Added Subject: {', '.join(added)}", position="bottom-right")
        if already_exists:
            return rx.toast.warning(f"Already exists: {', '.join(already_exists)}", position="bottom-right")

def subject_item(subject) -> rx.Component:
    """Creates a styled button for each subject with edit and delete options."""
    return rx.box(
        rx.hstack(
            rx.vstack(
                rx.text(subject, size="3", weight="bold"),
                # rx.foreach(subject[1],
                #     lambda sub_item: rx.box(
                #         rx.text(sub_item[1], size="3", weight="bold"),
                #     ),
                # ),
                spacing="1",
                align_items="flex-start",
                width="80%",
            ),
            rx.spacer(),
            rx.hstack(
                rx.button(
                    rx.icon("trash"),
                    size="1",
                    variant="ghost",
                    # on_click=lambda: rx.window_alert(f"Delete subject: {subject["name"]}"),
                    color="gray",
                    _hover={"color": "red.500"},
                ),
                spacing="1",
            ),
            width="100%",
        ),
        bg="#F4F3F2",
        color="black",
        padding="1em",
        border_radius="8px",
        width="100%",
        shadow="md",
        _hover={"bg": "#FFEFD0"},
        on_click=FormState.set_subject(subject),
    )

def create_container(title: str, subjects: list) -> rx.Component:
    """Creates a scrollable container with subject buttons and an add button."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text(title, font_size="24px", font_weight="bold", color="white"),
                rx.spacer(),
                rx.box(
                    rx.alert_dialog.root(
                        rx.alert_dialog.trigger(
                            rx.button(
                                rx.hstack(
                                    rx.icon("plus"),
                                    rx.text("Add Subject"),
                                    spacing="1",
                                ),
                                bg="white",
                                color="#598da2",
                                size="2",
                                border_radius="md",
                                # on_click=lambda: rx.window_alert("Add new subject"),
                                _hover={"bg": "#FFEFD0"},
                            ),
                            width="100%",
                        ),
                        rx.alert_dialog.content(
                            rx.alert_dialog.title("Add Subject"),
                            rx.alert_dialog.description("Enter subject IDs separated by commas."),
                            rx.form(
                                rx.flex(
                                    rx.text_area(
                                        placeholder="xxxx, xxxx, xxxx",
                                        name="subject_ids",
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
                                on_submit=ProfState.add_subject,
                                reset_on_submit=True,
                            ),
                            max_width="450px",
                        ),
                    ),
                    margin_left="10rem"
                ),
            ),
            
            rx.divider(border_color="white", opacity=0.3, margin_y="3"),
            rx.vstack(
                # Directly pass the reactive variable subjects into rx.foreach
                # rx.foreach(subjects, subject_item(subject["name"], subject["year"], subject["term"])),
                rx.foreach(subjects, subject_item),
                spacing="3", 
                align_items="center", 
                width="100%",
            ),
            spacing="3", 
            align_items="flex-start",
            width="100%",
        ),
        height="450px",
        width="550px",
        background_color="#598da2",
        border_radius="25px",
        padding="20px",
        overflow_y="scroll",
    )


def professor_subjects() -> rx.Component:

    return rx.box(
        rx.vstack(
            
            rx.text(f"{FormState.professor_name}'s Subjects", font_size="35px", font_weight="bold", color="#598da2", text_align="center"),
            create_container("Subjects Taught", FormState.subjects_taught_name),
            spacing="6",
            align_items="center"
        ),
        width="100%",
        min_height="100vh",
        display="flex",
        justify_content="center",
        align_items="center",
        padding_top="50px",
    )