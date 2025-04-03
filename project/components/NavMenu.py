import reflex as rx
from project.pages.login import FormState

def navmenu_link(text: str, url: str, margin_top: str = "") -> rx.Component:
    return rx.box(
        rx.link(
            rx.text(text, size="4", color="white", weight="bold", text_align="center"),
            href=url,
            padding="1em",
            width="100%",
            display="block", 
            text_decoration="none", 
            _hover={"bg": "#2b4c59"}  
        ),
        width="100%",  
        margin_top=margin_top  
    )

class NavigationState(rx.State):
    @rx.event
    def go_back(self):
        return rx.redirect("javascript:history.back()")
    
def navmenu() -> rx.Component:
    return rx.box(
        rx.vstack(            
            navmenu_link("Lectures", "/lecture_menu"),
            rx.cond(
                FormState.role == "Professor",  # Check if the role is "Professor"
                navmenu_link("Assignments", "/all_assignments"),  # Show this if the role is Professor
                navmenu_link("Assignments", "/assignments"),
            ),
            # navmenu_link("Assignments", "/assignments"),
            navmenu_link("Materials", "/materials"),
            navmenu_link("Quiz", "/quiz"),
            navmenu_link("Exam", "/exam"),
            navmenu_link("Grades", "/grades"),
            # navmenu_link("Manage Students", "/manage_students"),
            rx.cond(
                FormState.role == "Professor",  # Check if the role is "Professor"
                navmenu_link("Manage Students", "/manage_students"),  # Show this if the role is Professor
                rx.box()  # Show an empty box (nothing) if not a Professor
            ),
            rx.button(
                "Back",
                on_click=NavigationState.go_back,
                width="100%",
                padding="1em",
                margin_top="40px",
                text_align="center",
                color="white",
                weight="bold",
                size="4",
                bg="#598DA2",
                text_decoration="none", 
                _hover={"bg": "#2b4c59"}
            ),
            
            align_items="start",
            spacing="4",
            width="100%",
            height="100%",
        ),
        bg="#598DA2",  
        color="white",  
        padding="1em",
        padding_left="0",
        padding_right="0",
        width="250px",  
        height="100vh",
        position="fixed",
        top="82px",
        left="0",
        z_index="10",
        shadow="md",
    )