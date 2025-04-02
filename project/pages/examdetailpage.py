import reflex as rx

class ExamState(rx.State):
    """Manages exam-related state."""
    
    exam_title: str = "Final Exam"
    exam_date: str = "20 May 2024"
    exam_time: str = "10:00 AM"
    exam_file: str = "final_exam.pdf"  # Simulated exam file name
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

    def grade_exam(self):
        """Handles grading an exam."""
        rx.window_alert("Grade Exam Clicked")  # Placeholder for grading logic

    def view_submitted_works(self):
        """View the submitted works."""
        rx.window_alert("Viewing Submitted Works")

    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle the upload of file(s)."""
        for file in files:
            upload_data = await file.read()
            outfile = rx.get_upload_dir() / file.filename
            # Save the file
            with outfile.open("wb") as file_object:
                file_object.write(upload_data)
            self.user_file = file.filename

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

def exam_details() -> rx.Component:
    """Dynamic exam page with containers side by side and buttons below."""
    return rx.box(
        rx.vstack(
            rx.text("Exam Details", font_size="24px", font_weight="bold", color="#598da2"),

            # HStack for side-by-side containers
            rx.hstack(
                # Exam File Container
                rx.vstack(
                    create_container("Exam File", [ExamState.exam_file]),
                    # rx.vstack(
                    #     rx.button(
                    #         "Add Exam", padding="10px", background_color="#6EA9C5",
                    #         color="white", width="180px", height="45px", border_radius="10px",
                    #         weight="bold", on_click=lambda: rx.window_alert("Add Exam Clicked")
                    #     ),
                    #     rx.button(
                    #         "Edit Exam", padding="10px", background_color="#6EA9C5",
                    #         color="white", width="180px", height="45px", border_radius="10px",
                    #         weight="bold", on_click=lambda: rx.window_alert("Edit Exam Clicked")
                    #     ),
                    #     # rx.button(
                    #     #     "Grade Exam", padding="10px", background_color="#6EA9C5",
                    #     #     color="white", width="180px", height="45px", border_radius="10px",
                    #     #     weight="bold", on_click=lambda: ExamState.grade_exam()
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
                                ExamState.score,  # Score updates dynamically
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
                        rx.dialog.root(
                            rx.dialog.trigger(
                                rx.button(
                                    "Upload your file", 
                                    padding="10px", 
                                    background_color="#6EA9C5",
                                    color="white", 
                                    width="180px", 
                                    height="45px", 
                                    border_radius="10px",
                                    weight="bold",
                                ),
                            ),
                            rx.dialog.content(
                                rx.dialog.title("Upload File"),
                                rx.dialog.description("Select your file"),
                                rx.upload(
                                    rx.vstack(
                                        rx.button("Select File"),
                                        rx.text("Drag and drop files here or click to select files"),
                                    ),
                                    id="exam_upload",
                                    accept={
                                        "application/pdf": [".pdf"],
                                        "image/png": [".png"],
                                        "image/jpeg": [".jpg", ".jpeg"]
                                    },
                                    max_files=1,
                                    on_drop=ExamState.handle_upload(
                                        rx.upload_files(upload_id="exam_upload")
                                    ),
                                ),
                                rx.flex(
                                    rx.dialog.close(
                                        rx.button(
                                            "Cancel",
                                            variant="soft",
                                            color_scheme="gray",
                                        ),
                                    ),
                                    rx.dialog.close(
                                        rx.button("Confirm", type="submit"),
                                    ),
                                    spacing="3",
                                    justify="end",
                                ),
                                max_width="450px",
                            ),
                        ),
                        rx.button(
                            "Submit", padding="10px", background_color="#6EA9C5",
                            color="white", width="180px", height="45px", border_radius="10px",
                            weight="bold", on_click=lambda: ExamState.submit()
                        ),
                        rx.button(
                            "Unsubmit", padding="10px", background_color="#6EA9C5",
                            color="white", width="180px", height="45px", border_radius="10px",
                            weight="bold", on_click=lambda: ExamState.unsubmit()
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
