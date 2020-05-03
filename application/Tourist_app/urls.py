from django.urls import path, re_path
from .views import *
    # Tourist_appList, ItemList, UserItemList
app_name = "Tourist_app"
# app_name will help us do a reverse look-up latter.
urlpatterns = [
path('users/', UserView.as_view()),
path('routes/<int:pk>', RouteView.as_view()),
path('points/', RoutePointView.as_view()),
path('user_routes/<int:pk>', UserRoutesView.as_view()),
path('classes/', UserClasses.as_view()),
path('objects/<slug:pk>', MapObjectView.as_view()),
path('objects/', MapObjectView.as_view()),

]
