from http.client import responses
from django.contrib import admin
from .models import User, Drives, Responses, Departments, Course, Companies, Announcements
# Register your models here.

admin.site.register(User)
admin.site.register(Drives)
admin.site.register(Responses)
admin.site.register(Departments)
admin.site.register(Course)
admin.site.register(Companies)
admin.site.register(Announcements)