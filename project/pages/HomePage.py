import reflex as rx

def menu_year() -> rx.Component:
    return rx.container(
        rx.hstack(
            rx.link(  # Link to Year 1 page
                rx.button(
                    "Year 1", 
                    padding="20px", 
                    background_color="#42798F",
                    size="2",  
                    weight="bold",
                    color="white",  
                    width="180px", 
                    height="180px",
                    border_radius="20px",
                ),
                href="/year1",  # Navigates to Year 1 page
            ), 
            rx.link(  # Link to Year 2 page
                rx.button(
                    "Year 2", 
                    padding="20px", 
                    background_color="#42798F",
                    size="2", 
                    weight="bold",
                    color="white",  
                    width="180px", 
                    height="180px",
                    border_radius="20px",
                ),
                href="/year2",  # Navigates to Year 2 page
            ),
            justify="center", 
            align_items="center",  
            width="100%",  
        ),
        
        # Row 2: Year 3 and Year 4 buttons
        rx.hstack(
            rx.link(  # Link to Year 3 page
                rx.button(
                    "Year 3", 
                    padding="20px", 
                    background_color="#42798F",
                    size="2", 
                    weight="bold",
                    color="white",  
                    width="180px", 
                    height="180px",
                    border_radius="20px",
                ),
                href="/year3",  # Navigates to Year 3 page
            ),
            rx.link(  # Link to Year 4 page
                rx.button(
                    "Year 4", 
                    padding="20px", 
                    background_color="#42798F",
                    size="2",
                    weight="bold",
                    color="white",  
                    width="180px", 
                    height="180px",
                    border_radius="20px",
                ),
                href="/year4",  # Navigates to Year 4 page
            ),
            margin_top="20px",
            justify="center",  
            align_items="center",  
            width="100%", 
        ),
        width="100%", 
        align_items="center",  
    )