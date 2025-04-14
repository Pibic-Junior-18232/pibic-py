from django.urls import path
from dengue_tracker_app import views

urlpatterns = [
    path("", views.home_page, name="home"),
    path("registros/", views.list_cases, name="registros"),
    path("form_case/", views.case_register_or_edit, name="new_case"),
    path("form_case/<int:case_id>/", views.case_register_or_edit, name="edit_case"),
    path("delete/<int:case_id>/", views.case_delete, name="delete_case"),
]