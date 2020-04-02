from django.urls import path, re_path
from .views import ListUser, DoTask
from .views import DatabaseListCreateView, StudentGroupView, CoursesListView, DatabaseRetrieveView, DatabaseRetrieveUpdateView, DatabaseRetrieveDeleteView,  TaskListCreateView, TaskRetrieveView, TaskRetrieveUpdateView, TaskRetrieveDeleteView, TaskInThemeListCreateView, TaskInThemeRetrieveView,TaskInThemeRetrieveUpdateView, TaskInThemeRetrieveDeleteView, SetOfTaskListCreateView, SetOfTaskRetrieveView,SetOfTaskRetrieveUpdateView, SetOfTaskRetrieveDeleteView,ThemeListCreateView, ThemeRetrieveView, ThemeRetrieveUpdateView, ThemeRetrieveDeleteView,CourseListCreateView, CourseRetrieveView, CourseRetrieveUpdateView, CourseRetrieveDeleteView, UserCourseListCreateView, UserCourseSetInitialsView, IndividualRoute

    # KitList, ItemList, UserItemList
app_name = "kit"
# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('databases/', DatabaseListCreateView.as_view()),
    re_path(r'databases/(?P<pk>[0-9]+)/', DatabaseRetrieveView.as_view()),
    re_path(r'databases/(?P<pk>[0-9]+)/update/', DatabaseRetrieveUpdateView.as_view()),
    re_path(r'databases/(?P<pk>[0-9]+)/delete/', DatabaseRetrieveDeleteView.as_view()),

    path('tasks/', TaskListCreateView.as_view()),
    re_path(r'^tasks/(?P<pk>[0-9]+)/$', TaskRetrieveView.as_view()),
    re_path(r'^tasks/(?P<pk>[0-9]+)/update/$', TaskRetrieveUpdateView.as_view()),
    re_path(r'^tasks/(?P<pk>[0-9]+)/delete/$', TaskRetrieveDeleteView.as_view()),

    path('tasks-in-theme/', TaskInThemeListCreateView.as_view()),
    re_path(r'^tasks-in-theme/(?P<pk>[0-9]+)/$', TaskInThemeRetrieveView.as_view()),
    re_path(r'^tasks-in-theme/(?P<pk>[0-9]+)/update/$', TaskInThemeRetrieveUpdateView.as_view()),
    re_path(r'^tasks-in-theme/(?P<pk>[0-9]+)/delete/$', TaskInThemeRetrieveDeleteView.as_view()),

    path('sets-of-task/', SetOfTaskListCreateView.as_view()),
    re_path(r'^sets-of-task/(?P<pk>[0-9]+)/$', SetOfTaskRetrieveView.as_view()),
    re_path(r'^sets-of-task/(?P<pk>[0-9]+)/update/$', SetOfTaskRetrieveUpdateView.as_view()),
    re_path(r'^sets-of-task/(?P<pk>[0-9]+)/delete/$', SetOfTaskRetrieveDeleteView.as_view()),

    path('theme/', ThemeListCreateView.as_view()),
    re_path(r'^theme/(?P<pk>[0-9]+)/$', ThemeRetrieveView.as_view()),
    re_path(r'^theme/(?P<pk>[0-9]+)/update/$', ThemeRetrieveUpdateView.as_view()),
    re_path(r'^theme/(?P<pk>[0-9]+)/delete/$', ThemeRetrieveDeleteView.as_view()),

    path('course/', CourseListCreateView.as_view()),
    re_path(r'^course/(?P<pk>[0-9]+)/$', CourseRetrieveView.as_view()),
    re_path(r'^course/(?P<pk>[0-9]+)/update/$', CourseRetrieveUpdateView.as_view()),
    re_path(r'^course/(?P<pk>[0-9]+)/delete/$', CourseRetrieveDeleteView.as_view()),

    path('student-course/', UserCourseListCreateView.as_view()),
    re_path(r'^student-course/(?P<pk>[0-9]+)/set-initials/$', UserCourseSetInitialsView.as_view()),
    re_path(r'^student-course/(?P<student_course_id>[0-9]+)/theme/(?P<theme_id>[0-9]+)/sets-of-task/(?P<set_of_task_id>[0-9]+)/task/(?P<task_id>[0-9]+)/$', DoTask.as_view()),

    path('IndividualRoute/', IndividualRoute.as_view(), name='IndividualRoute'),

    path('student-groups/', StudentGroupView.as_view()),

    path('users/', ListUser.as_view()),

    path('courses/', CoursesListView.as_view()),
    # path('kit/', KitList.as_view()),
    # path('item/', ItemList.as_view()),
    # path('user_kit/<int:pk>/', UserItemList.as_view()),
    # path('user_kit/', UserItemList.as_view()),
    ]
