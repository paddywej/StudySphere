import reflex as rx

def assignment_item(assignment_id: str, name: str, due_date: str, status: str) -> rx.Component:
    # Background color based on status
    status_colors = {
        "new": "#EFFAFF",   # Light blue for new
        "viewed": "#D3F8E2", # Light green for viewed
        "done": "#D1E7F8",   # Light blue for done
    }
    
    return rx.link(
        rx.box(
            rx.vstack(
                rx.text(name, size="3", weight="bold"),
                rx.text(f"Due: {due_date}", size="2"),
                rx.text(f"Status: {status.capitalize()}", size="2", color="gray"),
                spacing="1",
            ),
            bg=status_colors.get(status, "#EFFAFF"),
            color="black",
            padding="1em",
            border_radius="8px",
            width="100%",
            shadow="md",
            _hover={"bg": "#BFD9E5"},
        ),
        href=f"/assignment_details/{assignment_id}",
        width="100%",
        text_decoration="none",
    )

def assignments() -> rx.Component:
    # Sample list of assignments with unique IDs
    assignments_list = [
        {"id": "math_hw_1", "name": "Math Homework 1", "due_date": "2025-03-29", "status": "new"},
        {"id": "science_proj", "name": "Science Project", "due_date": "2025-04-02", "status": "viewed"},
        {"id": "history_essay", "name": "History Essay", "due_date": "2025-03-25", "status": "done"},
    ]
    
    return rx.container(
        rx.hstack(
            # Unfinished Assignments
            rx.box(
                rx.vstack(
                    rx.text("Unfinished Assignments", size="4", weight="bold"),
                    *[assignment_item(a["id"], a["name"], a["due_date"], a["status"]) for a in assignments_list if a["status"] != "done"],
                    spacing="2",
                    width="100%",
                ),
                width="45%",
                height="500px",
                bg="#D0E2EB",
                color="black",
                padding="1em",
                overflow="auto",
                border_radius="25px",
                margin_right="2rem",
            ),
            # Done Assignments
            rx.box(
                rx.vstack(
                    rx.text("Done Assignments", size="4", weight="bold"),
                    *[assignment_item(a["id"], a["name"], a["due_date"], a["status"]) for a in assignments_list if a["status"] == "done"],
                    spacing="2",
                    width="100%",
                ),
                width="45%",
                height="500px",
                bg="#D0E2EB",
                color="black",
                padding="1em",
                overflow="auto",
                border_radius="25px",
            ),
            spacing="4",
            justify="center",
            width="100%",
        ),
        width="100%",
        padding="2em",
        padding_top="7rem",
        margin_left="7rem",
        min_height="100vh",
        bg="white",
    )