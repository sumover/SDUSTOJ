from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('login/', toLoginPage, name='login'),
    path('POSTlogin/', loginParameterChecker, name='loginParamater'),
    path('courses/', userCourse, name='userCourse'),
    path('<int:course_id>/course/', courseDetail, 'courseDetail'),
    path('<int:course_id>/course/<int:contest_id>/contest/', contestDetail, name='contestDetail'),
    path('<int:course_id>course/<int:contest_id>/contest/<int:problem_id>/problem/', problemDetail,
         name='problemDetail'),
    path('submit/<int:contest_id>/contest/<int:problem_id>/problem/', submit, name='submit'),
    path('<int:contest_id>/status/', contestProblemStatus, name='contestStatus'),

]
