from django.urls import path
from dengue_tracker_app import views

urlpatterns = [
    path("", views.home_page, name="main_page")
]