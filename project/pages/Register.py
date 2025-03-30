import reflex as rx
from project.components.NavBar import navbar_link
from project.state.formstate import FormState

def register() -> rx.Component:
    return rx.box(
        # Desktop version
        rx.hstack(
            rx.image(src="/hat_icon.png", width="130px", height="auto"),
            align_items="center",
            justify="center",
            margin_top="12px",
        ),
        rx.hstack(
            rx.heading(
                "StudySphere", size="7"
            ),
            align_items="center",
            justify="center",
        ),
        rx.vstack(
            rx.form(
                rx.vstack(
                    rx.text("First Name", font_size="16px", color="white"),
                    rx.input(
                        name="first_name",
                        border_radius="20px",
                        border="none",
                        color="black",
                        background_color="#EFFAFF",
                        width="20rem",
                        height="2.4rem",
                        # padding="0.5rem",
                    ),
                    rx.text("Last Name", font_size="16px", color="white"),
                    rx.input(
                        name="last_name",
                        border_radius="20px",
                        border="none",
                        color="black",
                        background_color="#EFFAFF",
                        width="20rem",
                        height="2.4rem",
                        # padding="0.5rem",
                    ),
                    rx.text("Gmail", font_size="16px", color="white"),
                    rx.input(
                        name="gmail",
                        border_radius="20px",
                        border="none",
                        color="black",
                        background_color="#EFFAFF",
                        width="20rem",
                        height="2.4rem",
                        # padding="0.5rem",
                    ),
                    rx.text("Password", font_size="16px", color="white"),
                    rx.input(
                        name="password",
                        type="password",
                        border_radius="20px",
                        border="none",
                        color="black",
                        background_color="#EFFAFF",
                        width="20rem",
                        height="2.4rem",
                        # padding="0.5rem",
                    ),
                    rx.button(
                        "Sign Up",
                        type="submit",
                        bg="#346579",
                        size="3",
                        color="white",
                        border_radius="20px",
                        padding="0.5em 1em",
                        align_items="center",
                        margin_left="7.2rem",
                    ),
                    justify="center",
                ),
                on_submit=FormState.handle_submit,
                reset_on_submit=True,   
                width="320px"
            ),
            align_items="center",
            justify="center",
            margin_top="12px",
        ),
        # Link for users who already have an account
        rx.vstack(
            rx.text("Already have an account?", font_size="16px", color="white"),
            rx.link("Log in", href="/login", color="white", text_decoration = "underline", font_size="16px"),  # Redirect to login page
            align_items="center",
            justify="center",
            margin_top="12px",
        ),
        bg="#598DA2",
        color="white", 
        padding="1em",
        min_height="100vh",
        width="100%",
        position="fixed",  
        top="0", 
        left="0",  
    )
