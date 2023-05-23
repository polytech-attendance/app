from django.contrib import admin
from .models import *
# Register your models here.

# admin.site.register(User)
# ONLY WITH POST REQUEST
admin.site.register(Teacher)
admin.site.register(GroupLeader)
admin.site.register(Group)
admin.site.register(Lesson)
admin.site.register(Subject)