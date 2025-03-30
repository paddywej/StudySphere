import reflex as rx

def landing():
    return rx.box(
        rx.image(src="/StudySphere.png", width="100vw", height="100vh", object_fit="cover"),
        rx.box(
            rx.button(
                "Get Started",
                on_click=rx.redirect("/login"),
                bg="#5996af",
                color="white",
                border_radius="20px",
                width="200px",     # Add button width
                height="60px",     # Add button height
                padding="20px",    # Add padding
                font_size="20px"   # Add font size
            ),
            text_align="center", 
            position="absolute",
            top="55%",
            left="25%",
            transform="translate(-50%, -50%)",
            padding="4",
            border_radius="lg",
            bg="rgba(255, 255, 255, 0.8)"
        ),
    )