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
from project.pages.lecturepage import lectures
from project.pages.materialpage import materials
from project.components.NavMenu import navmenu
from project.pages.assignments_page import assignments
from project.pages.assignment_details import assignment_details
from project.pages.quizpage import quiz
from project.pages.exampage import exam
from project.pages.gradepage import grades


style = {
    "::placeholder": {
        "color": "#9AA7B2",
    },
}

def HomePage() -> rx.Component:
    return rx.container(
        rx.vstack(
            navbar(), 
            navmenu(),
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
            lectures(),
        ),
        justify="center",
        min_height="100vh", 
        margin_top="10px", 
        bg="white"
    )

def assignments_page() -> rx.Component:
    return rx.container(
        rx.vstack(
            navbar(), 
            navmenu(),
            assignments(),
        ),
        justify="center",
        min_height="100vh", 
        margin_top="10px", 
        bg="white"
    )

def assignment_details_page() -> rx.Component:
    return rx.container(
        rx.vstack(
            navbar(), 
            navmenu(),
            assignment_details(),
        ),
        justify="center",
        min_height="100vh", 
        margin_top="10px", 
        bg="white"
    )

def material_page()-> rx.Component:
    return rx.container(
        rx.vstack(
            navbar(),
            navmenu(),
            materials(),
        ),
        justify="center",
        min_height="100vh", 
        margin_top="10px", 
        bg="white"
    )

def quiz_page() -> rx.Component:
    return rx.container(
        rx.vstack(
            navbar(),
            navmenu(),
            quiz(),
        ),
        justify="center",
        min_height="100vh", 
        margin_top="10px", 
        bg="white"
    )

def exam_page() -> rx.Component:
    return rx.container(
        rx.vstack(
            navbar(),
            navmenu(),
            exam(),
        ),
        justify="center",
        min_height="100vh", 
        margin_top="10px", 
        bg="white"
    )

def grade_page() -> rx.Component:
    return rx.container(
        rx.vstack(
            navbar(),
            navmenu(),
            grades(),
        ),
        justify="center",
        min_height="100vh", 
        margin_top="10px", 
        bg="white"
    )

def index() -> rx.Component:
    return rx.container(
        # register(),
        login(),
        # HomePage(),
        # lectures(),
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
app.add_page(assignment_details_page, route="/assignment_details/[assignment_id]")
app.add_page(lecture_page, route="/lectures")
app.add_page(material_page, route="/materials")
app.add_page(quiz_page, route="/quiz")
app.add_page(exam_page, route="/exam")
app.add_page(grade_page, route="/grades")