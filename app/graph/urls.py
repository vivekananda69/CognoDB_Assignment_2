from django.urls import path
from . import views

urlpatterns = [
    path('graph/', views.student_graph_explorer, name='student_graph_explorer'),
]