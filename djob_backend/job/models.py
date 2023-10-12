from django.contrib.auth.models import User
from django.db import models
from django.template import defaultfilters
import os
from fuzzywuzzy import fuzz
from fuzzywuzzy import process





class Category(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        ordering = ('title',)



class Job(models.Model):
    category = models.ForeignKey(Category, related_name='jobs', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    position_salary = models.CharField(max_length=255)
    position_location = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    company_location = models.CharField(max_length=255)
    company_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='jobs', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created_at',)
    
    def created_at_formatted(self):
        return defaultfilters.date(self.created_at, 'M d, Y')


class Employee(models.Model):
    job = models.ForeignKey(Job, related_name='employees', on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    matricule = models.CharField(max_length=55, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    phone = models.CharField(max_length=255)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='employees', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created_at',)
    
    def created_at_formatted(self):
        return defaultfilters.date(self.created_at, 'M d, Y')

    def __str__(self):
        return self.name
    




class Document(models.Model):
    created_by = models.ForeignKey(User,blank=True, null=True, related_name='documents', on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee,blank=True, null=True, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True, blank=True, null=True,)

    document = models.FileField(upload_to='uploads/%Y/%m/%d')
    is_email_delivered = models.BooleanField(default=False)  # New field for tracking email delivery
    
    def created_at_formatted(self):
        return defaultfilters.date(self.uploaded_at, 'M d, Y')

    def mark_as_email_delivered(self):
            self.is_email_delivered = True
            self.save()

    def save(self, *args, **kwargs):
        

        # Extract information from the document's name (assuming it's a PDF file)
        file_name = os.path.basename(self.document.name)
        full_name = file_name.strip().lower()

        # Try to find an employee using fuzzy string matching
        employee = None
        if self.created_by:
            employees = Employee.objects.filter(created_by=self.created_by)
            best_match = process.extractOne(full_name, employees.values_list('name', flat=True))

            if best_match and best_match[1] >= 80:  # Adjust the similarity threshold as needed
                best_match_name = best_match[0]
                employee = employees.get(name=best_match_name)

        if employee:
            self.employee = employee
        super().save(*args, **kwargs)
