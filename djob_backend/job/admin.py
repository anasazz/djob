from django.contrib import admin

from .models import Job, Category , Employee ,EmployeeFile , Document


admin.site.register(Category)
admin.site.register(Job)
admin.site.register(Employee)
admin.site.register(EmployeeFile)
admin.site.register(Document)