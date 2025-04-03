import reflex as rx

class AssignmentState(rx.State):
    """Manages assignment-related state."""
    
    assignment_title: str = "Homework 4"
    due_date: str = "28 Feb 2024"
    assignment_file: str = "homework4.pdf"  # Simulated backend file name
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

    def grade_assignment(self, new_score: str):
        """Handles grading an assignment."""
        self.score = new_score
        rx.window_alert(f"Assignment graded: {self.score}")

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

def assignment_details() -> rx.Component:
    """Dynamic assignment page with containers side by side and buttons below."""
    return rx.box(
        rx.vstack(
            rx.text("Assignment Details", font_size="24px", font_weight="bold", color="#598da2"),

            # HStack for side-by-side containers
            rx.hstack(
                # Assignment File Container
                rx.vstack(
                    create_container("Assignment File", [AssignmentState.assignment_file]),
                    # rx.vstack(
                    #     rx.button(
                    #         "Add Assignment", padding="10px", background_color="#6EA9C5",
                    #         color="white", width="180px", height="45px", border_radius="10px",
                    #         weight="bold", on_click=lambda: rx.window_alert("Add Assignment Clicked")
                    #     ),
                    #     rx.button(
                    #         "Edit Assignment", padding="10px", background_color="#6EA9C5",
                    #         color="white", width="180px", height="45px", border_radius="10px",
                    #         weight="bold", on_click=lambda: rx.window_alert("Edit Assignment Clicked")
                    #     ),
                    #     rx.button(
                    #         "View Submitted Works", padding="10px", background_color="#6EA9C5",
                    #         color="white", width="180px", height="45px", border_radius="10px",
                    #         weight="bold", on_click=rx.redirect("/manage_submitted_works")
                    #     ),
                    #     spacing="5",
                    #     align="center",
                    #     margin_top="10px"
                    # ),
                    # align="center",
                    # spacing="3"
                ),

                # Your Work Container with Score at the Top Right
                rx.vstack(
                    create_container(
                        "Your Work", 
                        [],
                        extra_content=rx.box(
                            rx.text("Score:", font_size="16px", font_weight="bold", color="#1d2023"),
                            rx.text(
                                AssignmentState.score,  # Score updates dynamically
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
                                rx.dialog.title("Upload Assignment"),
                                rx.dialog.description("Select your assignment file"),
                                rx.upload(
                                    rx.vstack(
                                        rx.button(
                                            "Select File",
                                        ),
                                        rx.text(
                                            "Drag and drop files here or click to select files"
                                        ),
                                        align="center",  # Center align the vstack contents
                                        spacing="4",
                                    ),
                                    id="assignment_upload",
                                    accept={
                                        "application/pdf": [".pdf"],
                                        "image/png": [".png"],
                                        "image/jpeg": [".jpg", ".jpeg"]
                                    },
                                    max_files=1,
                                    border="1px dotted rgb(107,99,246)",
                                    padding="5em",
                                    on_drop=AssignmentState.handle_upload(
                                        rx.upload_files(upload_id="assignment_upload")
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
                                align="center",  # Center align the dialog content
                            ),
                        ),
                        rx.button(
                            "Submit", padding="10px", background_color="#6EA9C5",
                            color="white", width="180px", height="45px", border_radius="10px",
                            weight="bold", on_click=lambda: AssignmentState.submit()
                        ),
                        rx.button(
                            "Unsubmit", padding="10px", background_color="#6EA9C5",
                            color="white", width="180px", height="45px", border_radius="10px",
                            weight="bold", on_click=lambda: AssignmentState.unsubmit()
                        ),
                        spacing="5",
                        align="center",
                        margin_top="10px"
                    ),
                    align="center",
                    spacing="3"
                ),
                spacing="9",
                justify="center",
            ),

            spacing="6",
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
