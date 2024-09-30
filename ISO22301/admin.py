from django.contrib import admin
from .models import Answer, Comment, Question, Area, Topic, ISO, Area_Header, Column_Header, Choice, Project, Dashboard, Area_Topic, Surveys

# Register your models here.

admin.site.register(Answer)
admin.site.register(Comment)
admin.site.register(Question)
admin.site.register(Area)
admin.site.register(Topic)
admin.site.register(ISO)
admin.site.register(Area_Header)
admin.site.register(Column_Header)
admin.site.register(Choice)
admin.site.register(Dashboard)
admin.site.register(Project)
admin.site.register(Area_Topic)
admin.site.register(Surveys)