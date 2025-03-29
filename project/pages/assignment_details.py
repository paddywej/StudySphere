import reflex as rx

class AssignmentState(rx.State):
    """Manages assignment-related state."""
    
    assignment_title: str = "Homework 4"
    due_date: str = "28 Feb 2024"
    assignment_file: str = "homework4.pdf"  # Simulated backend file name
    user_file: str = ""  # Stores uploaded file
    
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

def create_container(title: str, items: list) -> rx.Component:
    """Creates a scrollable container for assignment-related content."""
    return rx.box(
        # Title for the section (Assignment File or Your Work)
        rx.text(title, font_size="18px", font_weight="bold", color="#1d2023"),
        # Content that will exceed the container to make it scrollable
        rx.vstack(
            *[rx.box(item, padding="8px", background_color="#f8f8f8", border_radius="5px") for item in items],
            spacing="9"
        ),
        height="450px",  # Container height
        width="450px",  # Width for better centering
        background_color="#d0e2eb",  # Container background color
        border_radius="25px",  # Increased border radius for more rounded corners
        padding="10px",  # Reduced padding inside the container
        overflow_y="scroll",  # Enable vertical scrolling when content overflows
    )

def assignment_details() -> rx.Component:
    """Dynamic assignment page with scrollable containers."""
    return rx.box(
        rx.vstack(
            # Page Title
            rx.text("Assignment Details", font_size="24px", font_weight="bold", color="#598da2"),
            
            # Assignment information and action buttons
            rx.hstack(
                # Assignment File Box
                create_container("Assignment File", [AssignmentState.assignment_file]),
                # Your Work Box
                create_container("Your Work", []),  # No need for content here, just the layout
                spacing="9",  # Space between the boxes
                justify="center",  # Center the containers horizontally
            ),
            
            # Upload, Submit, Unsubmit buttons below the containers
            rx.vstack(
                rx.button(
                    "Upload your file", 
                    padding="15px", 
                    background_color="#6EA9C5", 
                    color="white", 
                    width="200px", 
                    height="50px", 
                    border_radius="10px", 
                    weight="bold",
                    on_click=lambda: AssignmentState.upload_file("sample_file.pdf")  # Trigger file upload (example)
                ),
                rx.button(
                    "Submit", 
                    padding="15px", 
                    background_color="#6EA9C5", 
                    color="white", 
                    width="200px", 
                    height="50px", 
                    border_radius="10px", 
                    weight="bold",
                    on_click=lambda: AssignmentState.submit()  # Trigger submission
                ),
                rx.button(
                    "Unsubmit", 
                    padding="15px", 
                    background_color="#6EA9C5", 
                    color="white", 
                    width="200px", 
                    height="50px", 
                    border_radius="10px", 
                    weight="bold",
                    on_click=lambda: AssignmentState.unsubmit()  # Trigger unsubmission
                ),
                spacing="2",  # Space between buttons
                justify="end",  # Center the buttons horizontally
                margin_left="50rem",
                margin_top="0px",  # Space between containers and buttons
            ),
            
            # Add Assignment and Edit Assignment buttons
            rx.vstack(
                rx.button(
                    "Add Assignment", 
                    padding="15px", 
                    background_color="#6EA9C5", 
                    color="white", 
                    width="200px", 
                    height="50px", 
                    border_radius="10px", 
                    weight="bold",
                    on_click=lambda: rx.window_alert("Add Assignment Clicked")  # Trigger Add Assignment action
                ),
                rx.button(
                    "Edit Assignment", 
                    padding="15px", 
                    background_color="#6EA9C5", 
                    color="white", 
                    width="200px", 
                    height="50px", 
                    border_radius="10px", 
                    weight="bold",
                    on_click=lambda: rx.window_alert("Edit Assignment Clicked")  # Trigger Edit Assignment action
                ),
                spacing="2",  # Space between buttons
                justify="end",  # Align the buttons to the right
                margin_left="50rem",
                margin_top="10px",  # Space between action buttons and new buttons
            ),
            spacing="9",  # Space between the title and materials content
            align_items="center",  # Align everything in the center
        ),
        width="100%",
        min_height="100vh",
        display="flex",
        justify_content="center",  # Center everything horizontally
        align_items="center",  # Center everything vertically
        margin_top="90px",
        margin_left="90px", 
    )
