import reflex as rx

class MaterialsState(rx.State):
    """Manages materials-related state."""
    
    material_file: str = ""  # Stores uploaded file name
    selected_category: str = ""  # Stores selected category (Textbook or Notes)

    textbooks: list[str] = []  # List to store textbook files
    notes: list[str] = []  # List to store note files

    def set_category(self, category: str):
        """Sets the category before uploading."""
        self.selected_category = category

    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handles file upload and sorts into correct category."""
        if not self.selected_category:
            rx.window_alert("Please select a category before uploading.")
            return

        for file in files:
            upload_data = await file.read()
            outfile = rx.get_upload_dir() / file.filename
            with outfile.open("wb") as file_object:
                file_object.write(upload_data)
            self.material_file = file.filename

            # Add the file to the correct list
            if self.selected_category == "Textbook":
                self.textbooks.append(file.filename)
            elif self.selected_category == "Notes":
                self.notes.append(file.filename)

            rx.window_alert(f"Successfully uploaded to {self.selected_category}: {file.filename}")

    def remove_file(self, file_name: str):
        """Removes a file from the correct category list."""
        if file_name in self.textbooks:
            self.textbooks.remove(file_name)
        elif file_name in self.notes:
            self.notes.remove(file_name)

def create_materials_container(title: str, items_var) -> rx.Component:
    """Creates a container for materials with clickable links and delete buttons."""
    return rx.box(
        rx.box(
            rx.text(title, font_size="18px", font_weight="bold", color="#1d2023"),
            position="relative",
            width="100%",
        ),
        rx.vstack(
            rx.foreach(
                items_var,
                lambda item: rx.hstack(
                    rx.link(
                        item,  # Display file name
                        href=rx.get_upload_url(item),  # Open file in new tab
                        target="_blank",
                        padding="8px",
                        background_color="#f8f8f8",
                        border_radius="5px",
                        text_decoration="none",
                        color="#0073e6",
                        _hover={"text_decoration": "underline"},
                    ),
                    rx.button(
                        "❌",  # Delete button
                        on_click=lambda: MaterialsState.remove_file(item),
                        background_color="transparent",
                        color="red",
                        font_size="14px",
                        padding="2px 5px",
                        border="none",
                        _hover={"color": "darkred"},
                    ),
                    spacing="3",  # Reduced spacing between file links and buttons
                ),
            ),
            spacing="5"  # Reduced overall spacing between the items
        ),
        height="450px",
        width="450px",
        background_color="#d0e2eb",
        border_radius="25px",
        padding="10px",
        overflow_y="scroll",
        position="relative",
    )

def materials() -> rx.Component:
    """Dynamic materials page with containers, file upload, and delete functionality."""
    return rx.box(
        rx.vstack(
            rx.text("Course Materials", font_size="24px", font_weight="bold", color="#598da2"),
            
            rx.hstack(
                rx.vstack(
                    create_materials_container("Textbooks", MaterialsState.textbooks),
                ),
                rx.vstack(
                    create_materials_container("Notes", MaterialsState.notes),
                ),
                spacing="5",  # Reduced spacing between the two containers
                justify="center",
            ),
            
            # Upload Button & Dialog
            rx.dialog.root(
                rx.dialog.trigger(
                    rx.button(
                        "Upload File", padding="10px", background_color="#6EA9C5",
                        color="white", width="180px", height="45px", border_radius="10px",
                        weight="bold",
                    ),
                ),
                rx.dialog.content(
                    rx.dialog.title("Upload Material"),
                    rx.dialog.description("Select a category and upload your file"),
                    
                    # Dropdown for category selection
                    rx.select(
                        ["Textbook", "Notes"],
                        name="role",
                        placeholder="Select Category",
                        border_radius="20px",
                        border="none",
                        color="black",
                        background_color="#EFFAFF",
                        width="20rem",
                        height="2.4rem",
                        on_change=MaterialsState.set_category,  
                    ),
                    
                    # Upload Component
                    rx.upload(
                        rx.vstack(
                            rx.button("Select File"),
                            rx.text("Drag and drop files here or click to select"),
                            align="center",
                            spacing="4",
                        ),
                        id="material_upload",
                        accept={ 
                            "application/pdf": [".pdf"],
                            "image/png": [".png"],
                            "image/jpeg": [".jpg", ".jpeg"]
                        },
                        max_files=1,
                        border="1px dotted rgb(107,99,246)",
                        padding="5em",
                        on_drop=MaterialsState.handle_upload(rx.upload_files(upload_id="material_upload")),
                    ),
                    
                    # Buttons for confirmation and cancellation
                    rx.flex(
                        rx.dialog.close(
                            rx.button("Cancel", variant="soft", color_scheme="gray"),
                        ),
                        rx.dialog.close(
                            rx.button("Confirm", type="submit"),
                        ),
                        spacing="3",
                        justify="end",
                    ),
                    max_width="450px",
                    align="center",
                ),
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
