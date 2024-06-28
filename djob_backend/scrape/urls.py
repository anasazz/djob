from django.urls import path
from . import views

urlpatterns = [
    path('scrape/', views.scrape_and_save, name='scrape_and_save'),
    path('scrape/<str:ref>/<str:org>/', views.one_scrape_and_save, name='scrape_specific_data'),

    # Add other URLs as needed
]
