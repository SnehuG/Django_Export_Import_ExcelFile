from django.contrib import admin
from first_app.models import FileContent

# Register your models here.
class FileContentAdmin(admin.ModelAdmin):
    list_display = ['id','Category','X','Y']

admin.site.register(FileContent,FileContentAdmin)