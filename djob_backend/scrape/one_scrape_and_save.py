from django.shortcuts import render
from django.http import HttpResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from .models import ScrapedData , ProcedureChoice , SectorCategory
import time
from django.shortcuts import get_object_or_404, HttpResponse
import re

from .extract_data import extract_data


def get_or_create_sector_categories(category_names):
    categories = []
    parent = None

    for category_name in category_names:
        # Split category names by '/'
        category_names_split = category_name.strip().split('/')

        for name in category_names_split:
            # Get or create the category and set parent for next iteration
            category, created = SectorCategory.objects.get_or_create(name=name.strip(), parent=parent)
            categories.append(category)
            parent = category  # Set current category as parent for the next level

    return categories

def _get_or_create_procedures(procedure_str):
    """
    Helper function to retrieve or create ProcedureChoice objects based on the input string.
    """
    procedure_names = [p.strip() for p in procedure_str.split('|') if p.strip()]  # Split and clean up the input

    procedures = []
    for name in procedure_names:
        procedure, _ = ProcedureChoice.objects.get_or_create(name=name)
        procedures.append(procedure)

    return procedures

def one_scrape_and_save(ref, org):
    url = f'https://www.marchespublics.gov.ma/index.php?page=entreprise.EntrepriseDetailsConsultation&refConsultation={ref}&orgAcronyme={org}'

    # Set up ChromeOptions for headless operation
    options = Options()
    options.add_argument('--headless')  # Run in headless mode without opening browser
    options.add_argument('--no-sandbox')  # Bypass OS security model
    options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems

    driver = None
    try:
        # Set up ChromeDriverManager and Service
        service = Service(ChromeDriverManager().install())

        # Initialize Chrome WebDriver with options and service
        driver = webdriver.Chrome(service=service, options=options)

        # Navigate to the page
        driver.get(url)

        # Wait for the page to fully load (adjust wait time as needed)
        driver.implicitly_wait(10)  # Wait for up to 10 seconds for elements to appear

        # Get the page source after waiting for the elements
        page_source = driver.page_source

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')

        # Extract data using the extract_data function
        data = extract_data(soup)

        # Print or process the extracted data (for demonstration, printing here)
        for key, value in data.items():
            print(f"{key}: {value}")

        # Create or update an object in your Django application with the extracted data
        obj, created = ScrapedData.objects.update_or_create(
            reference=ref,  # Assuming 'Référence' is a unique identifier
            defaults={
                'categorie': None,  # Replace with actual Sector object if available
                'reference_hash': data.get('Référence', ''),
                'objet': data.get('Objet', ''),
                'acheteur_public': data.get('Acheteur public', ''),
                'lieu_execution': data.get('Lieu d\'exécution', ''),
                'estimation': data.get('Estimation (en Dhs TTC)', None),
                'reserve_tpe_pme': data.get('Réservé à la TPE et PME', None),
                'adresse_retrait_dossiers': data.get('Adresse de retrait des dossiers', ''),
                'adresse_depot_offres': data.get('Adresse de dépôt des offres', ''),
                'lieu_ouverture_plis': data.get('Lieu d\'ouverture des plis', ''),
                'prix_acquisition_plans': data.get('Prix d/acquisition des plans', ''),
                'caution_provisoire': data.get('Caution provisoire', ''),
                'qualifications': data.get('Qualifications', ''),
                'agrements': data.get('Agréments', ''),
                'prospectus_notices_documents': data.get('Prospectus, notices ou autres documents', ''),
                'reunion': data.get('Réunion', ''),
                'visites_lieux': data.get('Visites des lieux', ''),
                'variante': data.get('Variante', None),
                'contact_administratif': data.get('Contact Administratif', ''),
                'json_raw': str(data),  # Store raw data as JSON string for reference
            }
        )
        obj.procedure.set(_get_or_create_procedures(data.get('Procédure', '')))
# Get or create SectorCategory instances and set them using .set()
        categories = get_or_create_sector_categories(data.get('Domaines d\'activité', []))
        obj.domaines_activite.set(categories)
        obj.save()
        # Optionally, save the data to database or file

        # Return an HttpResponse with a success message or rendered template
        return HttpResponse("Scraping and saving completed successfully!")

    except Exception as e:
        # Handle exceptions, log errors, etc.
        print(f"Error: {e}")
        return HttpResponse(f"Error occurred: {e}")

    finally:
        # Ensure WebDriver is properly closed
        if driver is not None:
            driver.quit()
# Define default headers