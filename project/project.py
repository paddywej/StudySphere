import reflex as rx
from rxconfig import config
from project.components.NavBar import navbar
from project.components.SearchBar import search_bar
from project.pages.homepage import menu_year  # Ensure lowercase file name
from project.pages.register import register
from project.pages.login import login

style = {
    "::placeholder": {
        "color": "#9AA7B2",
    },
}

def HomePage() -> rx.Component:
    return rx.container(
        rx.vstack(
            navbar(), 
            search_bar(),
            menu_year(),
        ),
        justify="center",
        min_height="100vh", 
        margin_top="70px", 
        bg="white"
    )

def register_page() -> rx.Component:
    return rx.container(
        register(),
    )

def login_page() -> rx.Component:
    return rx.container(
        login(),
    )

def index() -> rx.Component:
    return rx.container(
        register(),
        # login(),
        # HomePage(),
        bg="white"
    )

app = rx.App(style=style)

# Add all pages properly
app.add_page(index, route="/")
app.add_page(register_page, route="/register")
app.add_page(login_page, route="/login")
app.add_page(HomePage, route="/home")