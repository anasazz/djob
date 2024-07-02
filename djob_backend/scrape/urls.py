from django.urls import path
from . import views

urlpatterns = [
    path('scrape/', views.scrape_and_save, name='scrape_and_save'),
    path('get_500_scrape_and_save/', views.get_500_scrape_and_save, name='get_500_scrape_and_save'),
    path('scrape/<str:ref>/<str:org>/', views.one_scrape_and_save, name='scrape_specific_data'),
    path('bons/', views.scrape_bons, name='scrape_bons'),



    # Add other URLs as needed
]
