from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


admin.site.register(User, UserAdmin)
# admin.site.register(Membership)
admin.site.register(TouristClass)
admin.site.register(IndividualRoute)
admin.site.register(MapObject)
admin.site.register(ObjType)
admin.site.register(AuthorRoute)
admin.site.register(RouteComposition)
admin.site.register(AuthorRouteComposition)
