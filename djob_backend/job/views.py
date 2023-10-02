from rest_framework import status, authentication, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .forms import JobForm ,EmployeeForm , UploadForm
from .models import Job, Category, Employee, EmployeeFile  ,Document
from .serializers import JobSerializer, JobDetailSerializer,DocumentSerializer,  CategorySerializer , EmployeeSerializer

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from django.template.loader import render_to_string

from rest_framework.decorators import api_view, permission_classes, authentication_classes
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from django.core.mail import send_mail

from django.core.mail import EmailMessage
from django.conf import settings



class SendEmailsView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        try:
            # Retrieve a list of documents and their associated employees
            documents = Document.objects.select_related('employee').all()
            
            for document in documents:
                email_template = render_to_string('email.html', {
                'employee_name': document.employee.name,  # Replace with the employee's name
                'base_salary': 3000,          # Replace with the employee's base salary
                'overtime_hours': 10,         # Replace with the employee's overtime hours
                'total_salary': 3500,         # Replace with the total salary amount
            })
                # Skip documents without an associated employee or email
                if not document.employee or not document.employee.email:
                    continue

                # Load the PDF document to be attached
                pdf_document_path = document.document.path

                # Create an EmailMessage object
                email_subject = 'Fiche de paie de ce mois est pres'
                email_body = 'this is your pay roll today'
                from_email = 'contact@lidiye.com'
                to_email = [document.employee.email]

                email = EmailMessage(
                    email_subject,
                    email_template,
                    from_email,
                    to_email,
                    reply_to=[from_email],  # Optional: Set the reply-to address
                )

                # Attach the PDF document
                email.attach_file(pdf_document_path)

                # Send the email
                # Send the email and increment the counter if successful
                if email.send(fail_silently=False):
                    # Mark the document as email delivered
                    document.mark_as_email_delivered()

            return JsonResponse({'success': True})
        except Exception as e:
            print("exception", e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



class ChangeEmployeeView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, file_id):
        print("========", file_id,  request.data )
        try:
            
            # Get the newEmployeeId from the request data
            new_employee_id = request.data.get('newEmployeeId')

            # Your logic to update the employee for the file with ID 'file_id'
            # For example, you can retrieve the file object, update the employee field,
            # and save it.
            file = Document.objects.get(id=file_id)
            if file.is_email_delivered:
                return Response({'error': 'the email already sent to employee, can not change the employee'}, status=status.HTTP_400_BAD_REQUEST)


            file.employee = Employee.objects.get(id=new_employee_id)
            file.save()

            return Response({'message': 'Employee changed successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            # Handle errors here and return an appropriate response
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DocumentView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        docs = Document.objects.filter(created_by=request.user).order_by('-uploaded_at')
        serializer = DocumentSerializer(docs, many=True)

        return Response(serializer.data)




@api_view(["POST"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def upload(request):
    if request.FILES:
        form = UploadForm(request.POST, request.FILES)
        print('userrr' , request.user)

        if form.is_valid():
            doc = form.save(commit=False)
            doc.created_by = request.user
            doc.save()
    
    return JsonResponse({'success': True})

    
class CategoriesView(APIView):
    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)

        return Response(serializer.data)


class CreateEmployeeView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        form = EmployeeForm(request.data)

        if form.is_valid():
            doc = form.save(commit=False)
            doc.created_by = request.user
            doc.job = request.user.jobs.first()
            doc.save()

            return Response({'status': 'created'})
        else:
            return Response({'status': 'errors', 'errors': form.errors})
    
    def put(self, request, pk):
        doc = Employee.objects.get(pk=pk, created_by=request.user)
        form = EmployeeForm(request.data, instance=job)
        form.save()

        return Response({'status': 'updated'})
    
    def delete(self, request, pk):
        doc = Employee.objects.get(pk=pk, created_by=request.user)
        doc.delete()

        return Response({'status': 'deleted'})
    


class EmployeeView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        items = Employee.objects.filter(created_by=request.user)
        serializer = EmployeeSerializer(items, many=True)
        return Response(serializer.data)


class NewestJobsView(APIView):
    def get(self, request, format=None):
        jobs = Job.objects.all()[0:4]
        serializer = JobSerializer(jobs, many=True)

        return Response(serializer.data)


class MyJobsView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        jobs = Job.objects.filter(created_by=request.user)
        serializer = JobSerializer(jobs, many=True)

        return Response(serializer.data)


class CreateJobView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        form = JobForm(request.data)

        if form.is_valid():
            job = form.save(commit=False)
            job.created_by = request.user
            job.save()

            return Response({'status': 'created'})
        else:
            return Response({'status': 'errors', 'errors': form.errors})
    
    def put(self, request, pk):
        job = Job.objects.get(pk=pk, created_by=request.user)
        form = JobForm(request.data, instance=job)
        form.save()

        return Response({'status': 'updated'})
    
    def delete(self, request, pk):
        job = Job.objects.get(pk=pk, created_by=request.user)
        job.delete()

        return Response({'status': 'deleted'})
    

class BrowseJobsView(APIView):
    def get(self, request, format=None):
        jobs = Job.objects.all()
        categories = request.GET.get('categories', '')
        query = request.GET.get('query', '')

        if query:
            jobs = jobs.filter(title__icontains=query)

        if categories:
            jobs = jobs.filter(category_id__in=categories.split(','))

        serializer = JobSerializer(jobs, many=True)

        return Response(serializer.data)


class JobsDetailView(APIView):
    def get(self, request, pk, format=None):
        job = Job.objects.get(pk=pk)
        serializer = JobDetailSerializer(job)

        return Response(serializer.data)