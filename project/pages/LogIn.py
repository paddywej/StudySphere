import reflex as rx
from project.components.NavBar import navbar_link
from project.state.formstate import FormState

def login() -> rx.Component:
    return rx.box(
        # Desktop version
        rx.hstack(
            rx.button(
                rx.icon("arrow_left", size=30),
                rx.hstack(
                    rx.text("Back", size="3", weight="bold")
                ),
                bg="transparent",
                border="none",
            ),
            margin="1.7rem",
            margin_bottom="0",
        ),
        rx.hstack(
            rx.image(src="/hat_icon.png", width="130px", height="auto"),
            align_items="center",
            justify="center",
            margin_top="12px",
        ),
        rx.hstack(
            rx.heading(
                "StudySphere", size="7", weight="bold"
            ),
            align_items="center",
            justify="center",
        ),
        rx.vstack(
            rx.form(
                rx.vstack(
                    rx.text("Gmail"),
                    rx.input(
                        name="gmail",
                        border_radius="20px",
                        border="none",
                        color="black",
                        background_color="#EFFAFF",
                        width="20rem",
                        height="2.4rem",
                    ),
                    rx.text("Password"),
                    rx.input(
                        name="password",
                        type="password",
                        border_radius="20px",
                        border="none",
                        color="black",
                        background_color="#EFFAFF",
                        width="20rem",
                        height="2.4rem",
                    ),
                    rx.hstack(
                        navbar_link("Forgot password?", "/#"),
                        margin_left="12rem"
                    ),                  
                    rx.button(
                        "Log in",
                        type="submit",
                        bg="#346579",
                        size="3",
                        color="white",
                        border_radius="20px",
                        padding="0.5em 1em",
                        align_items="center",
                        margin_left="7.5rem",
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
        # Link for users who don't have an account yet
        rx.vstack(
            rx.text("Don't have an account yet?"),
            rx.link("Sign up", href="/register", color="white", text_decoration = "underline"),  # Redirect to register page
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
