import reflex as rx
from rxconfig import config
from project.components.NavBar import navbar
from project.components.SearchBar import search_bar
from project.pages.HomePage import menu_year
from project.pages.Register import register
from project.pages.LogIn import login

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

def index() -> rx.Component:
    return rx.container(
        register(),
        # login(),
        # HomePage(),
        bg="white"
    )

app = rx.App()
app = rx.App(style=style)
app.add_page(index)
