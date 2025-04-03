import reflex as rx
# from project.pages.login import FormState

class NotificationState(rx.State):
    notifications: list[dict] = [
        {"title": "New Assignment", "content": "You have a new assignment"},
        {"title": "New Quiz", "content": "You have a new quiz"},
        {"title": "New Exam", "content": "You have a new exam"}
    ]

def notification_dialog():
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("bell", size=30),
                bg="transparent",
                border="none",
                padding="2",
                cursor="pointer",
            )
        ),
        rx.dialog.content(
            rx.dialog.title("Notifications"),
            rx.dialog.description(
                rx.vstack(
                    rx.foreach(
                        NotificationState.notifications,
                        lambda notification: rx.box(
                            rx.heading(
                                notification["title"], 
                                size="3", 
                                cursor="pointer", 
                                on_click=lambda: handle_notification_click(notification["title"])  # Function reference, not execution
                            ),
                            rx.text(notification["content"]),
                            padding="4",
                            border_bottom="1px solid #eee"
                        )
                    )
                )
            ),
            rx.dialog.close(
                rx.button("Close")
            ),
            max_width="450px",
        ),
    )

def handle_notification_click(title: str):
    return rx.cond(
        title == "New Assignment",
        rx.redirect("/assignments"),
        rx.cond(
            title == "New Quiz",
            rx.redirect("/quiz"),
            rx.cond(
                title == "New Exam",
                rx.redirect("/exam"),
                rx.toast.error("Unknown notification type.")  # Default case for unknown types
            )
        )
    )



def navbar_link(text: str, url: str) -> rx.Component:
    return rx.link(
        rx.text(text, size="2", color="white"),
        href=url,
        cursor="pointer",  # Added cursor pointer
    )

def navbar() -> rx.Component:
    return rx.box(
        # Desktop version
        rx.desktop_only(
            rx.hstack(
                rx.hstack(
                    rx.image(src="/hat_icon.png", width="50px", height="auto", on_click=rx.redirect("/home"), cursor="pointer"),  # Added cursor pointer
                    # rx.icon("menu", size=30), 
                    rx.heading(
                        "StudySphere", size="7", weight="bold", cursor="pointer"  # Added cursor pointer
                    ),
                    align_items="center",
                    on_click=rx.redirect("/home"),
                ),
                rx.hstack(
                    notification_dialog(),
                    rx.menu.root(
                        rx.menu.trigger(
                            rx.icon_button(
                                rx.icon("user"),
                                size="2",
                                radius="full",
                                cursor="pointer" # Added cursor pointer
                            )
                        ),
                        rx.menu.content(
                            rx.menu.item("Settings", cursor="pointer"),  # Added cursor pointer
                            rx.menu.separator(),
                            rx.menu.item("Log out", on_click=rx.redirect("/login"), cursor="pointer"),  # Added cursor pointer
                        ),
                        justify="end",
                    ),
                    # User text with dropdown menu
                    rx.menu.root(
                        rx.menu.trigger(
                            rx.text("User", font_size="1.2em", color="white", cursor="pointer"),
                            # rx.text(FormState.user_id, font_size="1.2em", color="white", cursor="pointer"),
                        ),
                        rx.menu.content(
                            rx.menu.item("Settings", cursor="pointer"),  # Added cursor pointer
                            rx.menu.separator(),
                            rx.menu.item("Log out", on_click=rx.redirect("/login"), cursor="pointer"),  # Added cursor pointer
                        ),
                        justify="end",
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
                    rx.image(src="/hat_icon.png", width="60px", height="auto", cursor="pointer"),  # Added cursor pointer
                    # rx.icon("menu", size=25), 
                    rx.heading(
                        "StudySphere", size="6", weight="bold", cursor="pointer"  # Added cursor pointer
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
                        cursor="pointer",  # Added cursor pointer
                    ),
                    rx.menu.root(
                        rx.menu.trigger(
                            rx.icon_button(
                                rx.icon("user"),
                                size="2",
                                radius="full",
                                cursor="pointer",  # Added cursor pointer
                            )
                        ),
                        rx.menu.content(
                            rx.menu.item("Settings", cursor="pointer"),  # Added cursor pointer
                            rx.menu.separator(),
                            rx.menu.item("Log out", cursor="pointer"),  # Added cursor pointer
                        ),
                        justify="end",
                    ),
                    # User text with dropdown menu for mobile/tablet version
                    rx.menu.root(
                        rx.menu.trigger(
                            rx.text("User", font_size="1.2em", color="white", cursor="pointer"),
                            # rx.text(FormState.user_id, font_size="1.2em", color="white", cursor="pointer"),
                        ),
                        rx.menu.content(
                            rx.menu.item("Settings", cursor="pointer"),  # Added cursor pointer
                            rx.menu.separator(),
                            rx.menu.item("Log out", cursor="pointer"),  # Added cursor pointer
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
