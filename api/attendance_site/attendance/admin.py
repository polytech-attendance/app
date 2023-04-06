from django.contrib import admin
from .models import User
from .models import Teacher
from .models import GroupLeader
from .models import Group
from .models import Class
from .models import Subject

# Register your models here.

admin.site.register(User)
admin.site.register(Teacher)
admin.site.register(GroupLeader)
admin.site.register(Group)
admin.site.register(Class)
admin.site.register(Subject)