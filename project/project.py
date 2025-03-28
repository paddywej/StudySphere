import reflex as rx
from rxconfig import config
from project.components.NavBar import navbar
from project.components.SearchBar import search_bar
from project.pages.homepage import menu_year
from project.pages.register import register
from project.pages.login import login
from project.pages.year1 import Year1
from project.pages.year2 import Year2
from project.pages.year3 import Year3
from project.pages.year4 import Year4
from project.pages.lecturepage import lecture
from project.components.NavMenu import navmenu
from project.pages.assignments_page import assignments

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

def lecture_page()-> rx.Component:
    return rx.container(
        rx.vstack(
            navbar(),
            navmenu(),
        ),
        justify="center",
        min_height="100vh", 
        margin_top="70px", 
        bg="white"
    )

def index() -> rx.Component:
    return rx.container(
        # register(),
        # login(),
        # HomePage(),
        lecture_page(),
        bg="white"
    )

def year1() -> rx.Component:
    return rx.container(
        rx.vstack(
            navbar(), 
            Year1(),
        ),
        bg="white"
        
    )
def year2() -> rx.Component:
    return rx.container(
        rx.vstack(
            navbar(), 
            Year2(),
        ),
        bg="white"
        
    )

def assignments_page() -> rx.Component:
    return rx.container(
        rx.vstack(
            navbar(), 
            navmenu(),
            assignments(),
        ),
        bg="white"
        
    )
# def year3() -> rx.Component:
#     return rx.container(
#         Year3(),
#     )
# def year4() -> rx.Component:
#     return rx.container(
#         Year4(),
#     )
app = rx.App(style=style)

# Add all pages properly
app.add_page(index, route="/")
app.add_page(register_page, route="/register")
app.add_page(login_page, route="/login")
app.add_page(HomePage, route="/home")
app.add_page(year1, route="/year1")
app.add_page(year2, route="/year2")
app.add_page(assignments_page, route="/assignments")