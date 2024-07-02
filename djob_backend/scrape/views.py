from django.shortcuts import render
from django.http import HttpResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from .models import ScrapedData , SectorCategory ,ProcedureChoice  , Sector # Import your Django model
import time
from django.shortcuts import get_object_or_404, HttpResponse
import re
from datetime import datetime
import hashlib
from .extract_data import extract_data
from django.utils.dateparse import parse_date, parse_datetime
from selenium.webdriver.support.ui import Select




# GET BON D ACHATS

def extract_data(soup):
    data_list = []

    # Find all instances of <div> with class 'entreprise__card'
    cards = soup.find_all('div', class_='d-flex align-items-center border mt-5 col-12 gap-5 entreprise__card justify-content-between')

    for card in cards:
        data = {}

        # Extracting Référence
        reference_elem = card.find('a', class_='font-bold table__links', href=True)
        if reference_elem:
            ref = reference_elem.text.strip().replace('Référence :', '')

            data['Référence'] = ref
            print(f"Acheteur: {ref}")


        # Extracting Objet
        objet_elem = card.find('a', class_='truncate_fullWidth table__links', href=True)
        if objet_elem:
            objet_text = objet_elem.text.strip().replace('Objet : ', '')
            data['Objet'] = objet_text

        acheteur_elem = soup.find_all('a', class_='table__links')
        for elem in acheteur_elem:
            if elem.text.strip().startswith('Acheteur :'):
                acheteur = elem.text.strip().replace('Acheteur :', '')
                print(f"Acheteur: {acheteur}")
                data['Acheteur public'] = acheteur

                break  # Stop after finding the correct element

        # Extracting Date limite de remise des devis and Lieu d'exécution
        right_sub_card = card.find('a', class_='d-flex flex-column entreprise__rightSubCard')
        if right_sub_card:
            # Extracting Date limite de remise des devis
            date_elem = right_sub_card.find('span', text='Date limite de remise des devis')
            if date_elem:
                date_parent = date_elem.parent
                date_value = date_parent.find_next('span', class_='font-bold').text.strip()
                data['Date limite'] = date_value
                print("date_value",date_value)

                

            # Extracting Lieu d'exécution
            lieu_elem = right_sub_card.find('span', class_='font-bold text-center truncate-two-lines px-1')
            if lieu_elem:
                lieu_value = lieu_elem.text.strip()
                data['Lieu d\'exécution'] = lieu_value
        data_list.append(data)

    return data_list
BON_D_ACHAT_URL = "https://www.marchespublics.gov.ma/bdc/entreprise/consultation/?search_consultation_entreprise%5Bkeyword%5D=&search_consultation_entreprise%5Breference%5D=&search_consultation_entreprise%5Bobjet%5D=&search_consultation_entreprise%5BdateLimiteStart%5D=&search_consultation_entreprise%5BdateLimiteEnd%5D=&search_consultation_entreprise%5BdateMiseEnLigneStart%5D=&search_consultation_entreprise%5BdateMiseEnLigneEnd%5D=&search_consultation_entreprise%5Bcategorie%5D=&search_consultation_entreprise%5BnaturePrestation%5D=&search_consultation_entreprise%5Bacheteur%5D=&search_consultation_entreprise%5Bservice%5D=&search_consultation_entreprise%5BlieuExecution%5D=&search_consultation_entreprise%5BpageSize%5D=10"


def parse_date(dat_str):
    try:
        date_obj = datetime.strptime(dat_str, '%d/%m/%Y')
        # Format the datetime object into a string suitable for Django's DateTimeField
        date_formatted = date_obj.strftime('%Y-%m-%d %H:%M:%S')
        return date_formatted
    except ValueError:
        return None  # Handle parsing error appropriately

def scrape_bons(request):

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
        driver.get(BON_D_ACHAT_URL)

        # Wait for the page to fully load (adjust wait time as needed)
        time.sleep(10)  # Use sleep instead of implicit wait due to dynamic content loading

        # Get the page source after waiting for the elements
        page_source = driver.page_source

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')

        # Extract data using the extract_data function (replace with your actual extraction logic)
        data_list = extract_data(soup)

        # Print or process the extracted data (for demonstration, printing here)
        for data in data_list:
            reference_value = data.get('Référence', '')

            if reference_value:
                dat = data.get('Date limite', ''),
                print('dat=====',dat )

                dat_str = dat[0]
                dat_f = parse_date(dat_str)
                print('dat=====',dat )
                print('dat=====', dat_f)
                obj, created = ScrapedData.objects.update_or_create(
                    reference_hash=reference_value,
                    reference=reference_value,

                    
                    defaults={
                    'categorie': None,  # Replace with actual Sector object if available
                    'objet': data.get('Objet', ''),
                    'acheteur_public': data.get('Acheteur public', ''),
                    'lieu_execution': data.get('Lieu d\'exécution', ''),
                    'date_limite': dat_f,
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
            else:
                print(f"Warning: Empty or non-unique 'Référence' found: {reference_value}")

            
            # categories = get_or_create_sector_categories(data.get('Domaines d\'activité', []))
            # obj.domaines_activite.set(categories)
            # obj.save()


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





# END 

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
                    date_publication_str = date_publication_div.get_text(strip=True) if date_publication_div else ''
                    
                    if date_publication_str:
                        date_publication_obj = datetime.strptime(date_publication_str, '%d/%m/%Y')
                        date_publication_formatted = date_publication_obj.strftime('%Y-%m-%d')
                    else:
                        date_publication_formatted = None

                    # Extracting Objet
                    objet_div = row.find('div', {'id': lambda x: x and x.endswith('_panelBlocObjet')})
                    objet_text = objet_div.get_text(strip=True) if objet_div else ''

                    # Remove "Objet :" from the beginning of the text, if present
                    objet = objet_text.replace('Objet :', '', 1).strip()

                    # Extracting Acheteur Public
                    acheteur_public_div = row.find('div', {'id': lambda x: x and x.endswith('_panelBlocDenomination')})
                    acheteur_public_text = acheteur_public_div.get_text(strip=True) if acheteur_public_div else ''

                    # Remove "Acheteur public :" from the beginning of the text, if present
                    acheteur_public = acheteur_public_text.replace('Acheteur public :', '', 1).strip()

                    # Extracting Lieux Execution
                    lieux_execution_div = row.find('div', {'id': lambda x: x and x.endswith('_panelBlocLieuxExec')})
                    lieux_execution = lieux_execution_div.get_text(strip=True) if lieux_execution_div else ''

                    # Extracting Date Limite
                    date_limite_div = row.find('div', class_='cloture-line')
                    date_limite_str = date_limite_div.get_text(strip=True) if date_limite_div else ''

                    # Replace '/' with '-' in date_limite_str
                    date_limite_str = date_limite_str.replace('/', '-')

                    # Ensure there is a space between date and time components
                    if len(date_limite_str) > 10:
                        date_limite_str = f"{date_limite_str[:10]} {date_limite_str[10:]}"

                    # Parse date_limite_str into a datetime object
                    try:
                        date_limite_obj = datetime.strptime(date_limite_str, '%d-%m-%Y %H:%M')
                    except ValueError:
                        # Handle cases where date_limite_str does not match the expected format
                        date_limite_obj = None  # Or handle error as appropriate for your application

                    
                    # Extracting Reference Hash
                    reference_div = row.find('span', {'id': lambda x: x and x.endswith('_reference')})
                    reference_hash = reference_div.get_text(strip=True) if reference_div else ''

                    # Printing extracted data for verification
                    print(f"Ref Cons: {ref_cons}")
                    print(f"Org Cons: {org_cons}")
                    print(f"Type Procedure: {type_procedure}")
                    print(f"Categorie: {categorie}")
                    print(f"Date Publication: {date_publication_formatted}")
                    print(f"Objet: {objet}")
                    print(f"Acheteur Public: {acheteur_public}")
                    print(f"Lieux Execution: {lieux_execution}")
                    print(f"Date Limite: {date_limite_str}")
                    print(f"Reference Hash: {reference_hash}")
                    print("\n")

                    # Get or create sector instance
                    sector_instance = get_or_create_sector(categorie)

                    # Save each row to the database
                    scraped_instance = ScrapedData.objects.create(
                        reference=ref_cons,
                        acheteur_public=acheteur_public,
                        categorie=sector_instance,
                        publie_le=date_publication_formatted,
                        objet=objet,
                        lieu_execution=lieux_execution,
                        date_limite=date_limite_obj,
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



        
def get_500_scrape_and_save(request):
    url = 'https://www.marchespublics.gov.ma/index.php?page=entreprise.EntrepriseAdvancedSearch&searchAnnCons'

    # Set up ChromeOptions for headless operation
    options = Options()
    options.add_argument('--headless')  # Run in headless mode without opening browser
    options.add_argument('--no-sandbox')  # Bypass OS security model
    options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems

    try:
        # Set up ChromeDriverManager and Service
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


        # Select 500 rows per page
        select_element = driver.find_element(By.ID, 'ctl0_CONTENU_PAGE_resultSearch_listePageSizeTop')
        select = Select(select_element)
        select.select_by_value('500')

        # Wait for the results to load (adjust wait time as needed)
        time.sleep(10)  # Adjust wait time as per the page load speed

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
                    date_publication_str = date_publication_div.get_text(strip=True) if date_publication_div else ''
                    
                    if date_publication_str:
                        date_publication_obj = datetime.strptime(date_publication_str, '%d/%m/%Y')
                        date_publication_formatted = date_publication_obj.strftime('%Y-%m-%d')
                    else:
                        date_publication_formatted = None

                    # Extracting Objet
                    objet_div = row.find('div', {'id': lambda x: x and x.endswith('_panelBlocObjet')})
                    objet_text = objet_div.get_text(strip=True) if objet_div else ''

                    # Remove "Objet :" from the beginning of the text, if present
                    objet = objet_text.replace('Objet :', '', 1).strip()

                    # Extracting Acheteur Public
                    acheteur_public_div = row.find('div', {'id': lambda x: x and x.endswith('_panelBlocDenomination')})
                    acheteur_public_text = acheteur_public_div.get_text(strip=True) if acheteur_public_div else ''

                    # Remove "Acheteur public :" from the beginning of the text, if present
                    acheteur_public = acheteur_public_text.replace('Acheteur public :', '', 1).strip()

                    # Extracting Lieux Execution
                    lieux_execution_div = row.find('div', {'id': lambda x: x and x.endswith('_panelBlocLieuxExec')})
                    lieux_execution = lieux_execution_div.get_text(strip=True) if lieux_execution_div else ''

                    # Extracting Date Limite
                    date_limite_div = row.find('div', class_='cloture-line')
                    date_limite_str = date_limite_div.get_text(strip=True) if date_limite_div else ''

                    # Replace '/' with '-' in date_limite_str
                    date_limite_str = date_limite_str.replace('/', '-')

                    # Ensure there is a space between date and time components
                    if len(date_limite_str) > 10:
                        date_limite_str = f"{date_limite_str[:10]} {date_limite_str[10:]}"

                    # Parse date_limite_str into a datetime object
                    try:
                        date_limite_obj = datetime.strptime(date_limite_str, '%d-%m-%Y %H:%M')
                    except ValueError:
                        date_limite_obj = None

                    # Extracting Reference Hash
                    reference_div = row.find('span', {'id': lambda x: x and x.endswith('_reference')})
                    reference_hash = reference_div.get_text(strip=True) if reference_div else ''

                    # Print extracted data for verification
                    print(f"Ref Cons: {ref_cons}")
                    print(f"Org Cons: {org_cons}")
                    print(f"Type Procedure: {type_procedure}")
                    print(f"Categorie: {categorie}")
                    print(f"Date Publication: {date_publication_formatted}")
                    print(f"Objet: {objet}")
                    print(f"Acheteur Public: {acheteur_public}")
                    print(f"Lieux Execution: {lieux_execution}")
                    print(f"Date Limite: {date_limite_str}")
                    print(f"Reference Hash: {reference_hash}")
                    print("\n")

                    # Get or create sector instance
                    sector_instance = get_or_create_sector(categorie)

                    # Save each row to the database
                    scraped_instance = ScrapedData.objects.create(
                        reference=ref_cons,
                        acheteur_public=acheteur_public,
                        categorie=sector_instance,
                        publie_le=date_publication_formatted,
                        objet=objet,
                        lieu_execution=lieux_execution,
                        date_limite=date_limite_obj,
                        org=org_cons,
                        reference_hash=reference_hash,
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
