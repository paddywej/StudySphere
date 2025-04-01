import reflex as rx

def navbar_link(text: str, url: str) -> rx.Component:
    return rx.link(
        rx.text(text, size="2", color="white"), href=url
    )

def landingnavbar() -> rx.Component:
    return rx.box(
        # Desktop version
        rx.desktop_only(
            rx.hstack(
                rx.hstack(
                    rx.image(src="/hat_icon.png", width="50px", height="auto"),
                    rx.heading(
                        "StudySphere", size="7", weight="bold"
                    ),
                    align_items="center",
                ),
                rx.hstack(
                    rx.link(
                        rx.icon_button(
                            rx.icon("user"),
                            size="2",
                            radius="full",
                        ),
                        href="/login"
                    ),
                    rx.link(
                        rx.text("Login", font_size="1.2em", color="white"),
                        href="/login"
                    ),
                    spacing="2",  
                ),
                justify="between",
                align_items="center",
            ),
        ),

        # Mobile and Tablet version
        rx.mobile_and_tablet(
            rx.hstack(
                rx.hstack(
                    rx.image(src="/hat_icon.png", width="60px", height="auto"),
                    rx.heading(
                        "StudySphere", size="6", weight="bold"
                    ),
                    align_items="center",
                ),
                rx.hstack(
                    rx.link(
                        rx.icon_button(
                            rx.icon("user"),
                            size="2",
                            radius="full",
                            cursor="pointer"
                        ),
                        href="/login"
                    ),
                    rx.link(
                        rx.text("Login", font_size="1.2em", color="white", cursor="pointer"),
                        href="/login"
                    ),
                    spacing="2",  
                ),
                justify="between",
                align_items="center",
            ),
        ),
        bg="#346579",  
        color="white",  
        padding="1em",
        width="100%",
        position="fixed",
        top="0",
        left="0", 
        z_index="10", 
    )
