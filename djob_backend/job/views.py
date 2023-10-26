from rest_framework import status, authentication, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .forms import JobForm ,EmployeeForm , UploadForm
from .models import Job, Category, Employee  ,Document
from .serializers import JobSerializer, JobDetailSerializer,DocumentSerializer,  CategorySerializer , EmployeeSerializer
import requests
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
from .send_whats import upload_pdf_as_media, send_pdf_as_whatsapp_message


class SendWhatsAppView(APIView):
    def post(self, request, format=None):
        try:
            # Retrieve a list of documents
            selected_document_ids = request.data.get("document_ids", [])
            print('selected_document_ids',selected_document_ids)
            
            # Retrieve a list of selected documents
            documents = Document.objects.select_related('employee').filter(id__in=selected_document_ids)
            print('documents',documents)

            for document in documents:
                # Compose your WhatsApp message data
                if not document.employee or not document.employee.phone:
                    continue

                # Use the path to your PDF file
                #'https://cloud.lidiye.com' +
                doc = document.document
                pdf_file_path = 'https://cloud.lidiye.com' +  document.document.path
                print('pdf_file_path' , pdf_file_path)
                # Upload the PDF as media and get the media_id
                access_token = "EAAVa3LuWDaQBO0tePyQ3wb7lwCWjrC55tJ9zSqdhXgetI1wzJ0aV9Axo7i91pGyUmE7zwl17X5pbt7GsZC2w0rLJVQxmJK2tKq9ixASVBglEM04ykMdmptzT1jxrlsq8X66RtnXZC2zaWc3sB85fZAFBMeiruNMO7cnLVDLJ4IPLmdNxO2dohKkAgmCKqbWpJfSt3eD49iXA3B3VLdy4PD6SzNB"
                phone_number_id = "109321572275515"  # Replace with recipient's phone number ID

                media_id = upload_pdf_as_media(access_token, phone_number_id, pdf_file_path , doc)

                if media_id:
                    print('media id' ,media_id )

                    # Send the WhatsApp message with the PDF media
                    recipient_phone_number = document.employee.phone  # Replace with recipient's phone number
                    success = send_pdf_as_whatsapp_message(access_token, recipient_phone_number, media_id)
                    print('heeeeeer')
                    if success:
                        print('succcesss')

                        # PDF sent successfully
                        document.mark_as_whatsapp_delivered()
                        return Response({'success': 'PDF sent successfully'})
                    else:
                        return Response({'error': 'no success'}, status=status.HTTP_400_BAD_REQUEST)

                else:
                    return Response({'error': 'no media id'}, status=status.HTTP_400_BAD_REQUEST)
                    

            return Response({'success': 'All PDFs sent successfully'})
        except Exception as e:
            print("exception", e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SendEmailsView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        try:
            selected_document_ids = request.data.get("document_ids", [])
            print('selected_document_ids',selected_document_ids)
            # Retrieve a list of selected documents
            documents = Document.objects.select_related('employee').filter(id__in=selected_document_ids)

      
            for document in documents:
                employee_name = document.employee.name if document.employee else 'Employee'

                email_template = render_to_string('email.html', {
                'employee_name': employee_name,  # Replace with the employee's name
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
                from_email = document.employee.job.company_email
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
        try:
            doc = Employee.objects.get(pk=pk, created_by=request.user)

        except Employee.DoesNotExist:
            return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

        # Get the old phone number
        old_phone = doc.phone

        form = EmployeeForm(request.data, instance=doc)

        if form.is_valid():
            form.save()

            # Check if the 'phone' field has changed
            if old_phone != doc.phone:
                # The 'phone' field has changed, send a WhatsApp message
                print("Your profile has been updated. Your phone number has been updated.")
                doc.send_whatsapp_message()
            else:
                print(" The 'phone' field has not changed, no need to send a WhatsA")

                # The 'phone' field has not changed, no need to send a WhatsApp message

            return Response({'status': 'updated'})
        else:
            return Response({'error': 'Data validation failed', 'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)

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

class EmployeeDetailView(APIView):
    def get(self, request, pk, format=None):
        employee = Employee.objects.get(pk=pk)
        serializer = EmployeeSerializer(employee)

        return Response(serializer.data)