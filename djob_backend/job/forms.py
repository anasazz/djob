from django.forms import ModelForm
from django import forms

from .models import Job , Employee ,Document

class UploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('document',)

class JobForm(ModelForm):
    class Meta:
        model = Job
        fields = (
            'category', 
            'title', 
            'description', 
            'position_salary', 
            'position_location', 
            'company_name',
            'company_location',
            'company_email',
        )


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = (
 
            'name', 
            'description', 
            'email', 
            'phone', 
            'matricule',
        )