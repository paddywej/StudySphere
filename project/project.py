import reflex as rx
from rxconfig import config
from project.components.NavBar import navbar
from project.components.LandingNavBar import landingnavbar
from project.components.SearchBar import search_bar
from project.pages.homepage import menu_year
from project.pages.register import register
from project.pages.login import login
from project.pages.subjectpage import Subjects
from project.pages.year1 import Year1
from project.pages.year2 import Year2
from project.pages.year3 import Year3
from project.pages.year4 import Year4
from project.pages.lecturepage import lectures
from project.pages.materialpage import materials
from project.components.NavMenu import navmenu
from project.components.HomeNavMenu import homenavmenu
from project.pages.assignments_page import assignments
from project.pages.assignment_details import assignment_details
from project.pages.quizpage import quiz
from project.pages.quizdetailpage import quiz_details
from project.pages.exampage import exam
from project.pages.examdetailpage import exam_details
from project.pages.gradepage import grades
from project.pages.manage_students import manage_students
from project.pages.landingpage import landing
# from project.pages.submitted_works import manage_submitted_works
from project.pages.professor_subjects import professor_subjects
# from project.pages.gradingpage import grading
from project.pages.all_assignments import all_assignments
from project.pages.all_assignments import all_assignments
from project.pages.all_quizzes import all_quizzes
from project.pages.all_exams import all_exams
from project.pages.professorgrading import professor_grades

style = {
    "::placeholder": {
        "color": "#9AA7B2",
    },
}

def HomePage() -> rx.Component:
    return rx.container(
        rx.vstack(
            navbar(), 
            homenavmenu(),
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
    subject_title = "Dynamic Subject Title"
    return rx.container(
        rx.vstack(
            navbar(),
            navmenu(),
            lectures(subject_title),
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

def all_assignments_page() -> rx.Component:
    return rx.container(
        rx.vstack(
            navbar(), 
            navmenu(),
            all_assignments(),
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

def quiz_detail_page() -> rx.Component:
    return rx.container(
        rx.vstack(
            navbar(),
            navmenu(),
            quiz_details(),
        ),
        justify="center",
        min_height="100vh", 
        margin_top="10px", 
        bg="white"
    )

def all_quizzes_page() -> rx.Component:
    return rx.container(
        rx.vstack(
            navbar(), 
            navmenu(),
            all_quizzes(),
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

def exam_detail_page() -> rx.Component:
    return rx.container(
        rx.vstack(
            navbar(),
            navmenu(),
            exam_details(),
        ),
        justify="center",
        min_height="100vh", 
        margin_top="10px", 
        bg="white"
    )

def all_exams_page() -> rx.Component:
    return rx.container(
        rx.vstack(
            navbar(), 
            navmenu(),
            all_exams(),
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
        # login(),
        # HomePage(),
        # lectures(),
        landing_page(),
        # bg="white"
    )

def subject_page() -> rx.Component:
    return rx.container(
        rx.vstack(
            navbar(),
            Subjects(),
        ),
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

def year3() -> rx.Component:
    return rx.container(
        rx.vstack(
            navbar(),
            Year3(),
        ),
        bg="white"
        
    )

def year4() -> rx.Component:
    return rx.container(
        rx.vstack(
            navbar(), 
            Year4(),
        ),
        bg="white"
        
    )


def manage_students_page() -> rx.Component:
    return rx.container(
        rx.vstack(
            navbar(),
            navmenu(),
            manage_students(),
        ),
        justify="center",
        min_height="100vh", 
        margin_top="10px", 
        bg="white"
    )

def landing_page() -> rx.Component:
    return rx.container(
        rx.vstack(
            landingnavbar(), 
            landing(),
        ),
        justify="center",
        min_height="100vh", 
        margin_top="70px", 
        bg="white"
    )

# def manage_submitted_works_page() -> rx.Component:
#     return rx.container(
#         rx.vstack(
#             navbar(),
#             navmenu(),
#             manage_submitted_works(),
#         ),
#         justify="center",
#         min_height="100vh", 
#         margin_top="10px", 
#         bg="white"
#     )

def professor_subjects_page() -> rx.Component:
    return rx.container(
        rx.vstack(
            navbar(),
            professor_subjects(),
        ),
        justify="center",
        min_height="100vh", 
        margin_top="10px", 
        bg="white"
    )

def professor_grading_page() -> rx.Component:
    return rx.container(
        rx.vstack(
            navbar(),
            navmenu(),
            professor_grades(),
        ),
        justify="center",
        min_height="100vh", 
        margin_top="10px", 
        bg="white"
    )

# def grading_page() -> rx.Component:
#     return rx.container(
#         rx.vstack(
#             navbar(),
#             navmenu(),
#             grading(),
#         ),
#         justify="center",
#         min_height="100vh", 
#         margin_top="10px", 
#         bg="white"
#     )

app = rx.App(style=style)

# Add all pages properly
app.add_page(index, route="/")
app.add_page(register_page, route="/register")
app.add_page(login_page, route="/login")
app.add_page(HomePage, route="/home")
app.add_page(subject_page, route="/subject")
app.add_page(year1, route="/year1")
app.add_page(year2, route="/year2")
app.add_page(year3, route="/year3")
app.add_page(year4, route="/year4")
app.add_page(assignments_page, route="/assignments")
app.add_page(assignment_details_page, route="/assignment_details/[assignment_id]")
app.add_page(lecture_page, route="/lectures")
app.add_page(material_page, route="/materials")
app.add_page(quiz_page, route="/quiz")
app.add_page(quiz_detail_page, route="/quiz_details/[quiz_id]")
app.add_page(exam_page, route="/exam")
app.add_page(exam_detail_page, route="/exam_details/[exam_id]")
app.add_page(grade_page, route="/grades")
app.add_page(manage_students_page, route="/manage_students")
app.add_page(landing_page, route="/landingpage")
# app.add_page(manage_submitted_works_page, route="/manage_submitted_works")
app.add_page(professor_subjects_page, route="/professor_subjects")
# app.add_page(grading_page, route="/grading")
app.add_page(all_assignments_page, route="/all_assignments")
app.add_page(all_quizzes_page, route="/all_quizzes")
app.add_page(all_exams_page, route="/all_exams")
app.add_page(professor_grading_page, route="/professor_grades")