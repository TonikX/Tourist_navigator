from django.urls import path, re_path
from .views import *
    # Tourist_appList, ItemList, UserItemList
app_name = "Tourist_app"
# app_name will help us do a reverse look-up latter.
urlpatterns = [
path('users/', UserView.as_view()),
path('routes/', RouteView.as_view()),
path('classes/', UserClasses.as_view())

]
