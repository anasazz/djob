from django.urls import path

from . import views


urlpatterns = [
    path('', views.BrowseJobsView.as_view()),
    path('upload-files/', views.upload, name='upload_file'),

    path('categories/', views.CategoriesView.as_view()),
    path('my/', views.MyJobsView.as_view()),
    path('myemployees/', views.EmployeeView.as_view()),
    path('myDocuments/', views.DocumentView.as_view()),
    path('change-employee/<int:file_id>/', views.ChangeEmployeeView.as_view(), name='change-employee'),

    path('SendEmailsView/', views.SendEmailsView.as_view()),
    path('SendWhatsAppView/', views.SendWhatsAppView.as_view()),


    
    path('create/', views.CreateJobView.as_view()),

    path('employeeDetails/<int:pk>/delete/', views.CreateEmployeeView.as_view()),
    path('employeeUpdate/<int:pk>/edit/', views.CreateEmployeeView.as_view()),
    path('createEmployee/', views.CreateEmployeeView.as_view()),
    path('newest/', views.NewestJobsView.as_view()),
    path('<int:pk>/', views.JobsDetailView.as_view()),
    path('employeeDetails/<int:pk>/', views.EmployeeDetailView.as_view()),

    
    path('<int:pk>/delete/', views.CreateJobView.as_view()),
    path('<int:pk>/edit/', views.CreateJobView.as_view()),
]
