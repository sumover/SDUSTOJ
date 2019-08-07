from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.toLoginPage, name='toLoginPage'),
    path('POSTlogin/', views.loginParameterChecker, name='loginParameterChecker'),
    path('logout/', views.logout, name='logout'),
    path('courses/', views.userCourse, name='userCourse'),
    path('<int:course_id>/course/', views.courseDetail, 'courseDetail'),
    path('<int:course_id>/course/<int:contest_id>/contest/', views.contestDetail, name='contestDetail'),
    path('<int:course_id>course/<int:contest_id>/contest/<int:problem_id>/problem/', views.problemDetail,
         name='problemDetail'),
    path('submit/<int:contest_id>/contest/<int:problem_id>/problem/', views.submit, name='submit'),
    path('<int:contest_id>/status/', views.contestProblemStatus, name='contestProblemStatus'),

]
