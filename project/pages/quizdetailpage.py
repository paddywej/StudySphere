import reflex as rx

class QuizState(rx.State):
    """Manages quiz-related state."""
    
    quiz_title: str = "Sample Quiz"
    quiz_due_date: str = "25 March 2025"
    quiz_time: str = "12:00 PM"
    quiz_file: str = "sample_quiz.pdf"  # Simulated quiz file name
    user_file: str = ""  # Stores uploaded file
    score: str = "Not Graded"  # Stores the student's score
    
    def upload_file(self, file_name: str):
        """Handles file upload."""
        self.user_file = file_name

    def submit(self):
        """Handles submission."""
        if self.user_file:
            rx.window_alert(f"Successfully submitted: {self.user_file}")

    def unsubmit(self):
        """Handles unsubmission."""
        if self.user_file:
            rx.window_alert(f"Unsubmitted: {self.user_file}")
            self.user_file = ""  # Reset file after unsubmission

    def grade_quiz(self):
        """Handles grading a quiz."""
        rx.window_alert("Grade Quiz Clicked")  # Placeholder for grading logic
    
    def view_submitted_works(self):
        """Handles viewing submitted works."""
        rx.window_alert("View Submitted Works Clicked")  # Placeholder for viewing logic


def create_container(title: str, items: list, extra_content: rx.Component = None) -> rx.Component:
    """Creates a scrollable container for assignment-related content."""
    return rx.box(
        rx.box(
            rx.text(title, font_size="18px", font_weight="bold", color="#1d2023"),
            position="relative",
            width="100%",
        ),
        # Add extra content like the score at the top-right if provided
        extra_content if extra_content else rx.box(),
        rx.vstack(
            *[rx.box(item, padding="8px", background_color="#f8f8f8", border_radius="5px") for item in items],
            spacing="9"
        ),
        height="450px",
        width="450px",
        background_color="#d0e2eb",
        border_radius="25px",
        padding="10px",
        overflow_y="scroll",
        position="relative",  # Required for absolute positioning inside
    )


def quiz_details() -> rx.Component:
    """Dynamic quiz page with containers side by side and buttons below."""
    return rx.box(
        rx.vstack(
            rx.text("Quiz Details", font_size="24px", font_weight="bold", color="#598da2"),

            # HStack for side-by-side containers
            rx.hstack(
                # Quiz File Container
                rx.vstack(
                    create_container("Quiz File", [QuizState.quiz_file]),
                    # rx.vstack(
                    #     rx.button(
                    #         "Add Quiz", padding="10px", background_color="#6EA9C5",
                    #         color="white", width="180px", height="45px", border_radius="10px",
                    #         weight="bold", on_click=lambda: rx.window_alert("Add Quiz Clicked")
                    #     ),
                    #     rx.button(
                    #         "Edit Quiz", padding="10px", background_color="#6EA9C5",
                    #         color="white", width="180px", height="45px", border_radius="10px",
                    #         weight="bold", on_click=lambda: rx.window_alert("Edit Quiz Clicked")
                    #     ),
                    #     # rx.button(
                    #     #     "Grade Quiz", padding="10px", background_color="#6EA9C5",
                    #     #     color="white", width="180px", height="45px", border_radius="10px",
                    #     #     weight="bold", on_click=lambda: QuizState.grade_quiz()
                    #     # ),
                    #     rx.button(
                    #         "View Submitted Works", padding="10px", background_color="#6EA9C5",
                    #         color="white", width="180px", height="45px", border_radius="10px",
                    #         weight="bold", on_click=rx.redirect("/manage_submitted_works")
                    #     ),
                    #     spacing="5",
                    #     align="center",
                    #     margin_top="10px"  # Adds space between the container and buttons
                    # ),
                    # align="center",
                    # spacing="3"
                ),

                # Your Work Container
                rx.vstack(
                    create_container(
                        "Your Work", 
                        [],
                        extra_content=rx.box(
                            rx.text("Score:", font_size="16px", font_weight="bold", color="#1d2023"),
                            rx.text(
                                QuizState.score,  # Score updates dynamically
                                font_size="16px",
                                padding="5px 10px",
                                background_color="#d0e2eb",
                                border_radius="5px",
                                text_align="center",
                            ),
                            position="absolute",
                            top="10px", 
                            right="10px",
                            background_color="#d0e2eb",
                            border_radius="8px",
                            padding="5px",
                            color="#1d2023"
                        )
                    ),
                    rx.vstack(
                        rx.button(
                            "Upload your file", padding="10px", background_color="#6EA9C5",
                            color="white", width="180px", height="45px", border_radius="10px",
                            weight="bold", on_click=lambda: QuizState.upload_file("sample_quiz.pdf")
                        ),
                        rx.button(
                            "Submit", padding="10px", background_color="#6EA9C5",
                            color="white", width="180px", height="45px", border_radius="10px",
                            weight="bold", on_click=lambda: QuizState.submit()
                        ),
                        rx.button(
                            "Unsubmit", padding="10px", background_color="#6EA9C5",
                            color="white", width="180px", height="45px", border_radius="10px",
                            weight="bold", on_click=rx.redirect("/manage_submitted_works")
                        ),
                        spacing="5",
                        align="center",
                        margin_top="10px"  # Adds space between the container and buttons
                    ),
                    align="center",
                    spacing="3"
                ),
                spacing="9",  # Space between the two large containers
                justify="center",  # Aligns the containers side by side
            ),

            spacing="6",  # Space between the containers and buttons
            align_items="center",
        ),
        width="100%",
        min_height="100vh",
        display="flex",
        justify_content="center",
        align_items="center",
        padding_top="7rem",
        margin_left="7rem",
    )
