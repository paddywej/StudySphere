import reflex as rx

def navmenu_link(text: str, url: str, margin_top: str = "") -> rx.Component:
    return rx.box(
        rx.link(
            rx.text(text, size="4", color="white", weight="bold", text_align="center"),
            href=url,
            padding="1em",
            width="100%",
            display="block", 
            text_decoration="none", 
            _hover={"bg": "#2b4c59"}  
        ),
        width="100%",  
        margin_top=margin_top  
    )
    
def homenavmenu() -> rx.Component:
    return rx.box(
        rx.vstack(            
            navmenu_link("Lectures", "/lectures"),
            navmenu_link("Assignments", "/assignments"),
            navmenu_link("Materials", "/materials"),
            navmenu_link("Quiz", "/quiz"),
            navmenu_link("Exam", "/exam"),
            navmenu_link("Grades", "/grades"),
            navmenu_link("Manage Students", "/manage_students"),

            align_items="start",
            spacing="4",
            width="100%",
            height="100%",
        ),
        bg="#598DA2",  
        color="white",  
        padding="1em",
        padding_left="0",
        padding_right="0",
        width="250px",  
        height="100vh",
        position="fixed",
        top="82px",
        left="0",
        z_index="10",
        shadow="md",
    )