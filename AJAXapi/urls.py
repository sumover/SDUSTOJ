from django.urls import path
from . import views

urlpatterns = [
    path('<int:course_id>/course/', views.contestStaticReload, name='contestStaticReload'),
]
