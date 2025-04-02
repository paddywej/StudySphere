import reflex as rx
import requests
from project.state.formstate import FormState

#=============================================================================================================================================
#with backend
# class FormState(rx.State):
#     user_id: str = ""
#     role: str = ""
#     message: str = ""

#     # Student-specific attributes
#     student_year: str = ""
#     student_track: str | None = None
#     student_subjects_sem1: list = []
#     student_subjects_sem2: list = []

#     # Professor-specific attributes
#     subjects_taught: list = []

#     def handle_submit(self, form_data: dict):
#         """Handles user login and fetches additional details based on role."""
#         response = requests.post("http://127.0.0.1:8000/login", json=form_data)

#         if response.status_code == 200:
#             data = response.json()
#             self.user_id = data["user_id"]
#             self.role = data["role"]
#             print(self.user_id)

#             yield rx.toast.info("Log In Successful!", position="top-center")

#             # Redirect first, then fetch data separately
            

#             # Fetch additional data in background (doesn't block UI)
#             if self.role == "Student":
#                 self.fetch_student_details()
#                 print(f"Student Year: {self.student_year}, Track: {self.student_track}")  # Debugging print
#                 print(f"Subjects Semester 1: {self.student_subjects_sem1}")  # Debugging print
#                 print(f"Subjects Semester 2: {self.student_subjects_sem2}")  # Debugging print
            
#             elif self.role == "Professor":
#                 self.fetch_professor_subjects()

#             yield rx.redirect("/subject")  
        
#         else:
#             self.message = response.json().get("detail", "Invalid username or password.")


#     def fetch_student_details(self):
#         """Fetches student year and track, then fetches subjects for both semesters."""
#         url = f"http://localhost:8000/students/{self.user_id}/year"
#         response = requests.get(url)

#         if response.status_code == 200:
#             student_data = response.json()
#             self.student_year = student_data.get("year", 0)
#             self.student_track = student_data.get("track") if self.student_year in [3, 4] else None

#             # Now fetch subjects for both semesters
#             self.student_subjects_sem1 = self.get_subjects(self.student_year, 1, self.student_track)
#             self.student_subjects_sem2 = self.get_subjects(self.student_year, 2, self.student_track)

#     def fetch_professor_subjects(self):
#         """Fetches subjects taught by a professor."""
#         url = f"http://localhost:8000/professors/{self.user_id}/subjects"
#         response = requests.get(url)

#         if response.status_code == 200:
#             self.subjects_taught = response.json()
    
#     def get_subjects(self, year: int, semester: int, track: str | None = None) -> list:
#         """Fetch subjects based on student year, semester, and track."""
#         url = f"http://localhost:8000/subjects/{year}/{semester}"
#         response = requests.get(url)
        
#         return response.json() if response.status_code == 200 else []

#=============================================================================================================================================
#without backend

def login() -> rx.Component:
    return rx.box(
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
                    rx.text("Register as", font_size="16px", color="white"),
                    rx.select(["Student", "Professor"], name="role", placeholder="Select Role",
                              border_radius="20px", border="none", color="black",
                              background_color="#EFFAFF", width="20rem", height="2.4rem"),

                    # Display error messages
                    rx.text("", color="#A60A1B", font_size="16px", text_decoration="underline"), 
                        
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
                    rx.hstack(
                        rx.link("Forgot password?", href="/#", color="white", text_decoration="underline"),
                        margin_left="6rem"
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
