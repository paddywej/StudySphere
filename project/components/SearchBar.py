import reflex as rx

def search_bar() -> rx.Component:
    return rx.hstack(
            rx.input(
                rx.input.slot(rx.icon("search", color="black")),
                placeholder="Search for Courses",
                type="search",
                size="3",
                border_radius="20px", 
                border="2px solid black",
                color="black",  
                background_color="#EFFAFF",  
            ),
            margin_top="20px",
            justify="center",  
            align_items="center", 
            width="100%" 
        ),