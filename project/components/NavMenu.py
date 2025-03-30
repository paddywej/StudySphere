import reflex as rx

def navmenu_link(text: str, url: str, margin_top: str = "") -> rx.Component:
    return rx.box(
        rx.link(
            rx.text(text, size="4", color="white", weight="bold", text_align="center"),
            href=url,
            padding="1em",
            width="100%",
            display="block",  # Ensures full-width clickable area
            text_decoration="none",  # Removes underline
            _hover={"bg": "#2b4c59"}  # Hover effect on full row
        ),
        width="100%",  # Ensures full width for hover effect
        margin_top=margin_top  # Add margin_top here
    )

def navmenu() -> rx.Component:
    return rx.box(
        rx.vstack(            
            navmenu_link("Lectures", "/lectures"),
            navmenu_link("Assignments", "/assignments"),
            navmenu_link("Materials", "/materials"),
            navmenu_link("Quiz", "/quiz"),
            navmenu_link("Exam", "/exam"),
            navmenu_link("Grades", "/grades"),
            navmenu_link("Manage Students", "/manage_students"),
            
            navmenu_link("Back to Home", "/home", margin_top="30px"),  # Pass margin_top here
            
            align_items="start",
            spacing="4",
            width="100%",
            height="100%",  # Ensures vstack takes up the full height of its container
        ),
        bg="#598DA2",  
        color="white",  
        padding="1em",
        padding_left="0",  # Removes left padding
        padding_right="0",  # Removes right padding
        width="250px",  
        height="100vh",  # Full height
        position="fixed",
        top="82px",
        left="0",
        z_index="10",
        shadow="md",
    )
