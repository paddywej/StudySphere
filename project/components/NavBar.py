import reflex as rx

def navbar_link(text: str, url: str) -> rx.Component:
    return rx.link(
        rx.text(text, size="2",color="white"), href=url
    )

def navbar() -> rx.Component:
    return rx.box(
        # Desktop version
        rx.desktop_only(
            rx.hstack(
                rx.hstack(
                    rx.image(src="/hat_icon.png", width="50px", height="auto"),
                    # rx.icon("menu", size=30), 
                    rx.heading(
                        "StudySphere", size="7", weight="bold"
                    ),
                    align_items="center",
                ),
                rx.hstack(
                    rx.button(
                        rx.icon("bell", size=30),  
                        # on_click=lambda: print("Bell icon clicked"), 
                        bg="transparent",
                        border="none",  
                        padding="2", 
                    ),
                    rx.menu.root(
                        rx.menu.trigger(
                            rx.icon_button(
                                rx.icon("user"),
                                size="2",
                                radius="full",
                            )
                        ),
                        rx.menu.content(
                            rx.menu.item("Settings"),
                            rx.menu.separator(),
                            rx.menu.item("Log out"),
                        ),
                        justify="end",
                    ),
                    rx.text("User", font_size="1.2em", color="white"),
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
                    # rx.icon("menu", size=25), 
                    rx.heading(
                        "StudySphere", size="6", weight="bold"
                    ),
                    align_items="center",
                ),
                rx.hstack(
                    rx.button(
                        rx.icon("bell", size=25), 
                        # on_click=lambda: print("Bell icon clicked"),  # Placeholder action
                        bg="transparent", 
                        border="none", 
                        padding="2",
                    ),
                    rx.menu.root(
                        rx.menu.trigger(
                            rx.icon_button(
                                rx.icon("user"),
                                size="2",
                                radius="full",
                            )
                        ),
                        rx.menu.content(
                            rx.menu.item("Settings"),
                            rx.menu.separator(),
                            rx.menu.item("Log out"),
                        ),
                        justify="end",
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