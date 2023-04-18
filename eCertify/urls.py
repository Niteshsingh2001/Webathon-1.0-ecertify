from django.urls import path

from . import views

urlpatterns = [
    path("admin", views.index, name="index"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("logout", views.logout_view, name="logout"),
    path("student_data", views.student_data, name="student_data"),
    path("add_student_data", views.add_student, name="add_student"),
    path("del_student_data/<int:id>", views.delete_student, name="delete_student"),
    path("edit_student_data/<int:id>", views.edit_student, name="edit_student"),
    path("", views.studentInterface, name="studentInterface"),
    path("gen_certificate/<int:id>", views.generate, name="generate")
]
