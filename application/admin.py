from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Project)
admin.site.register(Sprint)
admin.site.register(PBI)
admin.site.register(Task)
admin.site.register(WorksOnProject)
admin.site.register(WorksOnTask)
admin.site.register(Notification)

