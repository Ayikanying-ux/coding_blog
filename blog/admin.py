from django.contrib import admin
from .models import Contact,Blog,Feedback, IpModel,Python,BlogComment,Projects
# Register your models here.
admin.site.register(Contact)

#admin.site.register(Blog)
#admin.site.register(Python)
admin.site.register(Feedback)
admin.site.register(BlogComment)
admin.site.register(IpModel)

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    class Media:
        js= ('tinyInject.js',)

@admin.register(Python)
class PythonAdmin(admin.ModelAdmin):
    class Media:
        js= ('tinyInject.js',)

@admin.register(Projects)
class ProjectsAdmin(admin.ModelAdmin):
    class Media:
        js= ('tinyInject.js',)