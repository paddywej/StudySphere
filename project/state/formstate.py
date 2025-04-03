import reflex as rx

class FormState(rx.State):
    form_data: dict = {}

    @rx.event
    def handle_submit(self, form_data: dict):
        """Handle form submission and redirect user."""
        self.form_data = form_data
        return rx.redirect("/lecture_menu")