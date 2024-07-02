def extract_data(soup):
    data = {}

    # Extracting specific data from the BeautifulSoup object

    # Date limite de remise des plis
    date_limite_elem = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_dateHeureLimiteRemisePlis')
    if date_limite_elem:
        date_limite = date_limite_elem.text.strip()
        data['Date limite de remise des plis'] = date_limite


# <div id="ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_prixAcquisitionPlans" class="line" style="display:;">
# 							<div class="intitule-240 bold">Prix d'acquisition des plans : </div>
# 							<div class="content-bloc bloc-500"><span id="ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_prixAcquisitionPlan">0,00 MAD </span></div>
# 						</div>
    
    prix_acc_elem = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_prixAcquisitionPlan')
    if prix_acc_elem:
        reference = prix_acc_elem.text.strip()
        data['Prix d/acquisition des plans'] = reference
    # Référence
    reference_elem = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_reference')
    if reference_elem:
        reference = reference_elem.text.strip()
        data['Référence'] = reference

    # Objet
    objet_elem = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_objet')
    if objet_elem:
        objet = objet_elem.text.strip()
        data['Objet'] = objet

    # Acheteur public
    acheteur_public_elem = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_entiteAchat')
    if acheteur_public_elem:
        acheteur_public = acheteur_public_elem.text.strip()
        data['Acheteur public'] = acheteur_public

    # Type d'annonce
    type_annonce_elem = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_annonce')
    if type_annonce_elem:
        type_annonce = type_annonce_elem.text.strip()
        data['Type d\'annonce'] = type_annonce

    # Procédure
    procedure_elem = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_typeProcedure')
    mode_passation_elem = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_modePassation')
    if procedure_elem and mode_passation_elem:
        procedure = procedure_elem.text.strip()
        mode_passation = mode_passation_elem.text.strip()
        data['Procédure'] = f'{procedure} | {mode_passation}'

    # Catégorie principale
    categorie_principale_elem = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_categoriePrincipale')
    if categorie_principale_elem:
        categorie_principale = categorie_principale_elem.text.strip()
        data['Catégorie principale'] = categorie_principale

    # Allotissement
    allotissement_elem = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_allotissement')
    if allotissement_elem:
        allotissement = allotissement_elem.text.strip()
        data['Allotissement'] = allotissement

    # Lieu d'exécution
    lieu_execution_elem = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_lieuxExecutions')
    if lieu_execution_elem:
        lieu_execution = lieu_execution_elem.text.strip()
        data['Lieu d\'exécution'] = lieu_execution

    # Estimation (en Dhs TTC)
    estimation_elem = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_estimation')
    if estimation_elem:
        estimation = estimation_elem.text.strip()
        data['Estimation (en Dhs TTC)'] = estimation

    # Réservé à la TPE et PME installées au Maroc, jeunes entreprises innovantes, Coopératives et auto-entrepreneurs
    reserve_tpe_pme_elem = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_reserveTpePme')
    if reserve_tpe_pme_elem:
        reserve_tpe_pme = reserve_tpe_pme_elem.text.strip()
        data['Réservé à la TPE et PME installées au Maroc, jeunes entreprises innovantes, Coopératives et auto-entrepreneurs'] = reserve_tpe_pme

    # Domaines d'activité
    domaines_activite_elem = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_domainesActivite')
    if domaines_activite_elem:
        domaines_activite_list = domaines_activite_elem.find_all('li')
        domaines_activite = [item.text.strip() for item in domaines_activite_list if item.text.strip()]
        data['Domaines d\'activité'] = domaines_activite

    # Adresse de retrait des dossiers
    adresse_retrait_dossiers_elem = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_adresseRetraitDossiers')
    if adresse_retrait_dossiers_elem:
        adresse_retrait_dossiers = adresse_retrait_dossiers_elem.text.strip()
        data['Adresse de retrait des dossiers'] = adresse_retrait_dossiers

    # Adresse de dépôt des offres
    adresse_depot_offres_elem = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_adresseDepotOffres')
    if adresse_depot_offres_elem:
        adresse_depot_offres = adresse_depot_offres_elem.text.strip()
        data['Adresse de dépôt des offres'] = adresse_depot_offres

    # Lieu d'ouverture des plis
    lieu_ouverture_plis_elem = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_lieuOuverturePlis')
    if lieu_ouverture_plis_elem:
        lieu_ouverture_plis = lieu_ouverture_plis_elem.text.strip()
        data['Lieu d\'ouverture des plis'] = lieu_ouverture_plis

    # Prix d'acquisition des plans
    prix_acquisition_plans_elem = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_prixAcquisitionPlans')
    if prix_acquisition_plans_elem:
        prix_acquisition_plans = prix_acquisition_plans_elem.text.strip()
        data['Prix d\'acquisition des plans'] = prix_acquisition_plans

    # Caution provisoire
    caution_provisoire_elem = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_cautionProvisoire')
    if caution_provisoire_elem:
        caution_provisoire = caution_provisoire_elem.text.strip()
        data['Caution provisoire'] = caution_provisoire

    # Qualifications
    qualifications_elem = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_qualifications')
    if qualifications_elem:
        qualifications = qualifications_elem.text.strip()
        data['Qualifications'] = qualifications

    # Agréments
    agrements_elem = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_agrements')
    if agrements_elem:
        agrements = agrements_elem.text.strip()
        data['Agréments'] = agrements

    # Prospectus, notices ou autres documents
    prospectus_notices_elem = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_prospectusNotices')
    if prospectus_notices_elem:
        prospectus_notices = prospectus_notices_elem.text.strip()
        data['Prospectus, notices ou autres documents'] = prospectus_notices

    # Réunion
    reunion_elem = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_reunion')
    if reunion_elem:
        reunion = reunion_elem.text.strip()
        data['Réunion'] = reunion

    # Visites des lieux
    visites_lieux_elem = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_visitesLieux')
    if visites_lieux_elem:
        visites_lieux = visites_lieux_elem.text.strip()
        data['Visites des lieux'] = visites_lieux

    # Variante
    variante_elem = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_variante')
    if variante_elem:
        variante = variante_elem.text.strip()
        data['Variante'] = variante

    # Contact Administratif
    contact_administratif_elem = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_contactAdministratif')
    if contact_administratif_elem:
        contact_administratif = contact_administratif_elem.text.strip()
        data['Contact Administratif'] = contact_administratif

    # Adresse électronique
    adresse_electronique_elem = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_adresseElectronique')
    if adresse_electronique_elem:
        adresse_electronique = adresse_electronique_elem.text.strip()
        data['Adresse électronique'] = adresse_electronique

    # Téléphone
    telephone_elem = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_telephone')
    if telephone_elem:
        telephone = telephone_elem.text.strip()
        data['Téléphone'] = telephone

    # Télécopieur
    telecopieur_elem = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_telecopieur')
    if telecopieur_elem:
        telecopieur = telecopieur_elem.text.strip()
        data['Télécopieur'] = telecopieur

# Additional fields extraction from infosPrincipales section
    infos_principales = soup.find('div', id='infosPrincipales')
    if infos_principales:
        lines = infos_principales.find_all('div', class_='line')
        for line in lines:
            label_element = line.find('div', class_='intitule-240 bold')
            value_element = line.find('span', class_='content-bloc')

            if label_element and value_element:
                label = label_element.find('span').text.strip()
                value = value_element.text.strip()
                data[label] = value
    return data
