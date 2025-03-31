import reflex as rx
import requests

class FormState(rx.State):
    message: str = ""

    # Simulate form handling without backend
    @rx.event
    def handle_submit(self, form_data: dict):
        # Clear the message before processing the request
        if self.message:
            self.message = ""

        # Simulate success or failure based on input (for front-end testing)
        if form_data.get("user_id") and form_data.get("password"):
            yield rx.toast.info("Registration successful!", position="top-center")
        else:
            self.message = "Registration failed. Please fill in all fields."

        # Uncomment when connecting to backend:
        # response = requests.post("http://127.0.0.1:8000/register", json=form_data)
        # if response.status_code == 200:
        #     return rx.toast.info("Registration successful!", position="top-center")
        # else:
        #     self.message = response.json().get("detail", "Registration failed.")


def register() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.image(src="/hat_icon.png", width="130px", height="auto"),
            align_items="center",
            justify="center",
            margin_top="12px",
        ),
        rx.hstack(
            rx.heading("StudySphere", size="7"),
            align_items="center",
            justify="center",
        ),
        rx.vstack(
            rx.form(
                rx.vstack(
                    rx.text("ID / Username", font_size="16px", color="white"),
                    rx.input(name="user_id", border_radius="20px", border="none",
                             color="black", background_color="#EFFAFF", width="20rem", height="2.4rem"),
                    
                    rx.text("Password", font_size="16px", color="white"),
                    rx.input(name="password", type="password", border_radius="20px", border="none",
                             color="black", background_color="#EFFAFF", width="20rem", height="2.4rem"),
                    
                    rx.text("Register as", font_size="16px", color="white"),
                    rx.select(["Student", "Professor"], name="role", placeholder="Select Role",
                              border_radius="20px", border="none", color="black",
                              background_color="#EFFAFF", width="20rem", height="2.4rem"),

                    # Display error messages
                    rx.text(FormState.message, color="#A60A1B", font_size="16px", text_decoration="underline"),

                    rx.button("Sign Up", type="submit", bg="#346579", size="3", color="white",
                              border_radius="20px", padding="0.5em 1em", align_items="center",
                              margin_left="7.2rem"),
    
                    justify="center",
                ),
                on_submit=FormState.handle_submit,  # No backend request, only front-end logic
                reset_on_submit=True,
                width="320px"
            ),
            align_items="center",
            justify="center",
            margin_top="12px",
        ),
        rx.vstack(
            rx.text("Already have an account?", font_size="16px", color="white"),
            rx.link("Log in", href="/login", color="white", text_decoration="underline", font_size="16px"),
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
