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

from rest_framework.decorators import api_view, permission_classes, authentication_classes



class DocumentView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        docs = Document.objects.filter(created_by=request.user)
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