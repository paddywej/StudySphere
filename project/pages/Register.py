import reflex as rx

class FormState(rx.State):
    form_data: dict = {}

    @rx.event
    def handle_submit(self, form_data: dict):
        """Handle the form submit."""
        self.form_data = form_data


def register() -> rx.Component:
    return rx.box(
        # Desktop version
        # rx.desktop_only(
            rx.hstack(
                rx.icon("menu", size=30), 
                rx.heading(
                    "StudySphere", size="7", weight="bold"
                ),
                align_items="center",
            ),
            rx.hstack(
                rx.text("Welcome to StudySphere!",size="5"),
                align_items="center",
                justify="center",
                margin_top="12px"
            ),
            rx.vstack(
                rx.form(
                    rx.vstack(
                        rx.text("Name",
                        align_items="left",),
                        rx.input(
                            name="first_name",
                            border_radius="20px",  
                            border="none", 
                            color="black",  
                            background_color="#EFFAFF", 
                            width="20rem",
                            height="2.4rem",
                        ),
                        rx.text("Surname"),
                        rx.input(
                            name="last_name",
                            border_radius="20px", 
                            border="none",  
                            color="black",  
                            background_color="#EFFAFF", 
                            width="20rem",
                            height="2.4rem",
                        ),
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
                            border_radius="20px", 
                            border="none", 
                            color="black", 
                            background_color="#EFFAFF",  
                            width="20rem",
                            height="2.4rem",
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
                            margin_left="6.8rem",
                        ),
                        
                        justify="center",
                        
                    ),
                    on_submit=FormState.handle_submit,
                    reset_on_submit=True,   
                    width="320px"
                ),
                rx.text("Already have an account? Log in"),
                # rx.divider(),
                # rx.heading("Results"),
                # rx.text(FormState.form_data.to_string()),
                align_items="center",
                justify="center",
                margin_top="12px",
            ),
                # ),
        # Mobile and Tablet version
        # rx.mobile_and_tablet(
        #     rx.hstack(
        #         rx.icon("menu", size=30),  # Menu icon
        #         rx.heading(
        #             "StudySphere", size="7", weight="bold"
        #         ),
        #         align_items="center",
        #     ),
        # ),
        bg="#598DA2",  
        color="white", 
        padding="1em",
        min_height="100vh",
        width="100%",
        position="fixed",  
        top="0", 
        left="0",  
    )