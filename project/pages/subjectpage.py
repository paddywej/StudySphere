import reflex as rx
import requests

#=============================================================================================================================================
# from project.pages.login import FormState  

#with backend
# class SubjectState(rx.State):
#     name: str = ""

#     def set_subject(self, subject_name: str):
#         self.name = subject_name
#         print(self.name)
#         return rx.redirect("/lectures")  # Redirect to lecture page


# def create_container(title: str,subject) -> rx.Component:
#     """Creates a scrollable container with subject buttons."""
#     return rx.box(
#         rx.text(title, font_size="24px", font_weight="bold", color="white", text_align="center", margin_bottom="1rem"),  # Centered title text
#         rx.vstack(rx.foreach(subject, button_subject),),
#         height="450px",
#         width="550px",
#         background_color="#598da2",
#         border_radius="25px",
#         padding="20px",
#         overflow_y="scroll",
#     )

# def button_subject(subject):
#     return rx.button(
#         subject,  # Extract subject name
#         padding="15px",
#         background_color="#F4F3F2",
#         color="black",
#         border_radius="0",
#         width="100%",
#         height="65px",
#         _hover={"background_color": "#FFEFD0"},
#         on_click=SubjectState.set_subject(subject)
#     )

# def Subjects() -> rx.Component:
#     return rx.box(
#         rx.vstack(
#             rx.hstack(
#                 rx.text("Year", font_size="35px", font_weight="bold", color="#598da2", text_align="center"),  # Centered title text
#                 rx.text(FormState.student_year, font_size="35px", font_weight="bold", color="#598da2", text_align="center"),  # Centered title text
#             ),
            
#             rx.hstack(
#                 create_container("Semester 1",FormState.student_subjects_sem1),
#                 create_container("Semester 2",FormState.student_subjects_sem2),
#                 spacing="9",
#                 align="center"
#             ),
#             spacing="9",
#             align_items="center"
#         ),
#         width="100%",
#         min_height="100vh",
#         display="flex",
#         justify_content="center",
#         align_items="center",
#         padding_top="50px",
#     )

#=============================================================================================================================================
#without backend
def create_container(title: str, subjects: list) -> rx.Component:
    """Creates a scrollable container with subject buttons."""
    return rx.box(
        rx.text(title, font_size="24px", font_weight="bold", color="white", text_align="center", margin_bottom="1rem"),  # Centered title text
        rx.vstack(
            *[rx.button(
                name, 
                padding="15px",  
                background_color="#F4F3F2", 
                color="black", 
                border_radius="8px",
                width="100%",
                height="65px",
                _hover={"bg": "#FFEFD0"} 
            ) for name in subjects],
            spacing="2", 
            align_items="center" 
        ),
        height="450px",
        width="550px",
        background_color="#598da2",
        border_radius="25px",
        padding="20px",
        overflow_y="scroll",
    )


def Subjects() -> rx.Component:
    """Creates the main page layout with scrollable containers for Semester 1 and 2."""

    return rx.box(
        rx.vstack(
            rx.text("Year 1", font_size="35px", font_weight="bold", color="#598da2", text_align="center"),  # Centered title text
            rx.hstack(
                create_container("Semester 1", "subject"),
                create_container("Semester 2", "subject"),
                spacing="9",
                align="center"
            ),
            spacing="9",
            align_items="center"
        ),
        width="100%",
        min_height="100vh",
        display="flex",
        justify_content="center",
        align_items="center",
        padding_top="50px",
    )

