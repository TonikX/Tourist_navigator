from django.contrib import admin
from .models import User, Database, DatabaseImage, Task, SetOfTask, Theme, TaskInTheme, Course,\
    UserCourse, UserMasteringTheme, IncludedTask,\
    UserPriorityTheme, IndividualRouteStep, StudentGroup
from django.contrib.auth.admin import UserAdmin
from .models import User


admin.site.register(Database)
admin.site.register(DatabaseImage)
admin.site.register(Task)
admin.site.register(SetOfTask)
admin.site.register(Theme)
admin.site.register(TaskInTheme)
admin.site.register(Course)
# admin.site.register(TaskResult)
admin.site.register(UserCourse)
admin.site.register(UserMasteringTheme)
admin.site.register(IncludedTask)
admin.site.register(IndividualRouteStep)
admin.site.register(StudentGroup)

admin.site.register(User, UserAdmin)
# admin.site.register(Membership)
