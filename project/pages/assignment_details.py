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

def assignment_details() -> rx.Component:
    """Dynamic assignment page."""
    return rx.container(
        rx.vstack(
            rx.text(f"{AssignmentState.assignment_title}: Due {AssignmentState.due_date}", 
                    size="5", weight="bold", color="#6EA9C5"),
            
            rx.hstack(
                # Assignment File Box
                rx.box(
                    rx.text("Assignment File", size="4", weight="bold"),
                    rx.button(AssignmentState.assignment_file, 
                              size="3", width="90%", padding="1em", 
                              bg="#EFFAFF", border_radius="8px"),
                    bg="#D0E2EB", color="black", padding="2em", 
                    border_radius="15px", width="45%", height="300px"
                ),

                # Your Work Box
                rx.box(
                    rx.text("Your Work", size="4", weight="bold"),
                    
                    # Upload Section
                    rx.input(placeholder="Upload your file", 
                             on_change=AssignmentState.upload_file),
                    
                    rx.button("Upload", 
                              on_click=lambda: rx.window_alert("File uploaded"), 
                              size="3", width="90%", padding="1em", 
                              bg="#EFFAFF", border_radius="8px"),
                    
                    # Submission Actions
                    rx.hstack(
                        rx.button("Submit", 
                                  on_click=AssignmentState.submit, 
                                  bg="#6EA9C5", color="white", 
                                  padding="0.5em 1em", border_radius="8px"),
                        rx.button("Unsubmit", 
                                  on_click=AssignmentState.unsubmit, 
                                  bg="#6EA9C5", color="white", 
                                  padding="0.5em 1em", border_radius="8px"),
                        spacing="1"
                    ),
                    bg="#D0E2EB", color="black", padding="2em", 
                    border_radius="15px", width="45%", height="300px"
                ),
                spacing="2"
            ),
            spacing="2"
        ),
        padding="2em", width="100%", align="center"
    )
