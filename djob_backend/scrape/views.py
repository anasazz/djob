from django.shortcuts import render
from django.http import HttpResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from .models import ScrapedData  , Sector # Import your Django model
import time
from django.shortcuts import get_object_or_404, HttpResponse
import re


def one_scrape_and_save(request, ref, org):
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

        # Find the specific div with id 'infosPrincipales'
        infos_principales_div = soup.find('div', {'id': 'infosPrincipales'})

        # Check if the div is found and extract its content
        if infos_principales_div:
            # Initialize a dictionary to store extracted data
            data = {
                'Acheteur public :': None,
                'Type d\'annonce :': None,
                'Procédure :': None,
                'Catégorie principale :': None,
                'Allotissement :': None,
                'Lieu d\'exécution :': None,
                'Estimation (en Dhs TTC) :': None,
                'Réservé à la TPE et PME installées au Maroc, jeunes entreprises innovantes, Coopératives et auto-entrepreneurs :': None,
                'Domaines d\'activité :': None,
                'Adresse de retrait des dossiers :': None,
                'Adresse de dépôt des offres :': None,
                'Lieu d\'ouverture des plis :': None,
                'Prix d\'acquisition des plans :': None,
                'Caution provisoire :': None,
                'Qualifications :': None,
                'Agréments  :': None,
                'Prospectus, notices ou autres documents :': None,
                'Réunion :': None,
                'Visites des lieux :': None,
                'Variante :': None,
                'Contact Administratif :': None,
            }

            # Extracting all lines within the div
            lines = infos_principales_div.find_all('div', class_='line')

            # Loop through each line and extract the bold and content values
            for line in lines:
                bold_element = line.find('div', class_='intitule-240 bold')
                content_element = line.find('div', class_='content-bloc bloc-500')
                if bold_element and content_element:
                    bold_text = bold_element.get_text(strip=True)
                    content_text = content_element.get_text(strip=True)
                    data[bold_text] = content_text

            # Debugging output to verify extracted data
            print("Extracted data:", data)

            # Create or update ScrapedData object
            scraped_data_obj, created = ScrapedData.objects.update_or_create(
                reference=ref,  # Adjust based on actual field name in data
                defaults={
                    'estimation': data.get('Estimation (en Dhs TTC) :', ''),
                    'reserve_tpe_pme': data.get('Réservé à la TPE et PME installées au Maroc, jeunes entreprises innovantes, Coopératives et auto-entrepreneurs :', ''),
                    'domaines_activite': data.get('Domaines d\'activité :', ''),
                    'adresse_retrait_dossiers': data.get('Adresse de retrait des dossiers :', ''),
                    'adresse_depot_offres': data.get('Adresse de dépôt des offres :', ''),
                    'lieu_ouverture_plis': data.get("Lieu d'ouverture des plis :", ''),
                    'prix_acquisition_plans': data.get('Prix d\'acquisition des plans :', ''),
                    'caution_provisoire': data.get('Caution provisoire :', ''),
                    'qualifications': data.get('Qualifications :', ''),
                    'agrements': data.get('Agréments  :', ''),
                    'prospectus_notices_documents': data.get('Prospectus, notices ou autres documents :', ''),
                    'reunion': data.get('Réunion :', ''),
                    'visites_lieux': data.get('Visites des lieux :', ''),
                    'variante': data.get('Variante :', ''),
                    'contact_administratif': data.get('Contact Administratif :', ''),
                }
            )

            # Debugging output for object creation or update
            if created:
                print("New object created:", scraped_data_obj)
            else:
                print("Object updated:", scraped_data_obj)

            # Return a success message or redirect
            return HttpResponse("Scraping and saving completed successfully.")

        else:
            return HttpResponse("Div 'infosPrincipales' not found on the page.")

    except Exception as e:
        # Print the exception for debugging
        print(f'Error during scraping with Selenium: {str(e)}')
        return HttpResponse(f'Error during scraping with Selenium: {str(e)}')

    finally:
        # Clean up
        if driver:
            driver.quit()

# Define default headers
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    # Add other headers as needed
}

def get_or_create_sector(name):
    sector, created = Sector.objects.get_or_create(name=name)
    return sector or created

def scrape_and_save(request):
    url = 'https://www.marchespublics.gov.ma/index.php?page=entreprise.EntrepriseAdvancedSearch&searchAnnCons'

    # Set up ChromeOptions for headless operation
    options = Options()
    options.add_argument('--headless')  # Run in headless mode without opening browser
    options.add_argument('--no-sandbox')  # Bypass OS security model
    options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems

    try:
        # Set up ChromeDriverManager and Service
        service = Service(ChromeDriverManager().install())

        # Initialize Chrome WebDriver with options and service
        driver = webdriver.Chrome(service=service, options=options)

        # Navigate to the page
        driver.get(url)

        # Find and click the search button
        search_button = driver.find_element(By.ID, 'ctl0_CONTENU_PAGE_AdvancedSearch_lancerRecherche')
        search_button.click()

        # Wait for the results to load (adjust wait time as needed)
        time.sleep(5)  # Adjust wait time as per the page load speed

        # Parse the updated HTML with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        table = soup.find('table', class_='table-results')

        # Scraping logic to extract data
        if table:
            rows = table.find_all('tr', class_='')

            for row in rows:
                try:
                    ref_cons = row.find('input', {'id': lambda x: x and x.endswith('_refCons')})['value']
                    org_cons = row.find('input', {'id': lambda x: x and x.endswith('_orgCons')})['value']
                    type_procedure = row.find('div', {'id': lambda x: x and x.endswith('_type_procedure')}).get_text(strip=True)
                    categorie = row.find('div', {'id': lambda x: x and x.endswith('_panelBlocCategorie')}).get_text(strip=True)
                    
                    # Extracting Date Publication
                    date_publication_div = row.find_all('div')[4]  # Adjust index as per the HTML structure
                    date_publication = date_publication_div.get_text(strip=True) if date_publication_div else ''

                    objet_div = row.find('div', {'id': lambda x: x and x.endswith('_panelBlocObjet')})
                    objet = objet_div.get_text(strip=True) if objet_div else ''

                    acheteur_public_div = row.find('div', {'id': lambda x: x and x.endswith('_panelBlocDenomination')})
                    acheteur_public = acheteur_public_div.get_text(strip=True) if acheteur_public_div else ''

                    lieux_execution_div = row.find('div', {'id': lambda x: x and x.endswith('_panelBlocLieuxExec')})
                    lieux_execution = lieux_execution_div.get_text(strip=True) if lieux_execution_div else ''

                    # Extracting Date Limite
                    date_limite_div = row.find('div', class_='cloture-line')
                    date_limite = date_limite_div.get_text(strip=True) if date_limite_div else ''
# Extracting Reference Hash
                    reference_div = row.find('span', {'id': lambda x: x and x.endswith('_reference')})
                    reference_hash = reference_div.get_text(strip=True) if reference_div else ''

                    # Printing extracted data for verification
                    print(f"Ref Cons: {ref_cons}")
                    print(f"Org Cons: {org_cons}")
                    print(f"Type Procedure: {type_procedure}")
                    print(f"Categorie: {categorie}")
                    print(f"Date Publication: {date_publication}")
                    print(f"Objet: {objet}")
                    print(f"Acheteur Public: {acheteur_public}")
                    print(f"Lieux Execution: {lieux_execution}")
                    print(f"Date Limite: {date_limite}")
                    print(f"Reference Hash: {reference_hash}")

                    print("\n")
                    sector_instance = get_or_create_sector(categorie)

                    # Save each row to the database
                    scraped_instance = ScrapedData.objects.create(
                        reference=ref_cons,
                        acheteur_public=acheteur_public,
                        procedure=type_procedure,
                        categorie=sector_instance,
                        publie_le=date_publication,
                        objet=objet,
                        lieu_execution=lieux_execution,
                        date_limite=date_limite,
                        org=org_cons,
                        reference_hash=reference_hash,  # Save reference hash

                    )
                    scraped_instance.save()

                except Exception as e:
                    print(f'Error during scraping: {str(e)}')

        else:
            print("Table not found.")

        # Return a success message or redirect
        return HttpResponse("Scraping and saving completed successfully.")

    except Exception as e:
        return HttpResponse(f'Error during scraping with Selenium: {str(e)}')

    finally:
        # Clean up
        if 'driver' in locals() or 'driver' in globals():
            driver.quit()




