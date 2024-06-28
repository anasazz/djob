from django.db import models




class Sector(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Sector"
        verbose_name_plural = "Sectors"
    
class SectorCategory(models.Model):
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.sector} - {self.name}"

    class Meta:
        unique_together = ('sector', 'name',)
        verbose_name = "Sector Category"
        verbose_name_plural = "Sector Categories"

def create_dynamic_models():
    # Fetch sectors and their categories from your data source or define them statically
    sectors_and_categories = {
        'Travaux': [
            'Travaux de voiries, chemins et pistes',
            'Travaux hydrauliques, maritimes et fluviaux',
            'Travaux d’assainissement, d’eau potable et de réseaux divers',
            'Construction d\'ouvrages d\'art',
            'Travaux d’électricité',
            'Aménagement de jardins, d\'espaces verts',
            'Travaux de construction et d’aménagement',
            'Travaux d’installation',
            'Terrassements',
            'Fondations, injections, parois moulées, sondages et forages',
            'Travaux d’étanchéité, isolation, plomberie et menuiserie',
            'Travaux de revêtement, platerie et peinture',
            'Travaux forestiers'
        ],
        'Fournitures': [
            'Effets d’habillement et accessoires',
            'Matériel et fournitures électriques, électronique, électromécanique et pièces de rechange',
            'Matériel technique, de lutte contre l’incendie et pièces de rechange',
            'Matériel de transport, pièces de rechange et pneumatiques',
            'Matériel, mobilier et fournitures de bureau',
            'Matériel informatique, logiciels et pièces de rechanges',
            'Engins de chantier, matériel de manutention et de levage',
            'Documentation, manuels, fournitures scolaires et d’enseignement',
            'Equipements et produits médicaux, pharmaceutiques et de laboratoire',
            'Produits alimentaires, d’élevage, de la pêche, d’agriculture, d’horticulture et pépinière',
            'Matériaux de construction, plomberie, quincaillerie et outillages',
            'Imprimés, produits d’impression, de reproduction, et de photographie',
            'Produits chimiques, de nettoyage, insecticides',
            'Matériel et articles de literie, de couchage, de cuisine et de buanderie',
            'Produits pétroliers, carburants, lubrifiants et produits de chauffage',
            'Matériel et articles de sport, médailles, effigies et drapeaux',
            'Matières premières et produits de textile, cuir, caoutchouc et plastique',
            'Location avec option d’achat de biens, d’équipements de matériel et d’outillage',
            'Objets d’art, articles artistiques, de divertissement et de médiathèque'
        ],
        'Services': [
            'Services de location sans option d’achat',
            'Services d’assurance',
            'Services architecturales et topographiques',
            'Services courants',
            'Conseil, audit et assistance à maitrise d’ouvrage (à l’exception du domaine des nouvelles technologies)',
            'Nettoyage, gardiennage, entretien et maintenance',
            'Etudes d’ingénierie',
            'Prestations d’essais, de contrôle et de laboratoire',
            'Services d’hôtellerie, hébergement, restauration, événementiel et marketing',
            'Transport, collecte et services connexes',
            'Services de technologies de l\'information et télécommunications',
            'Services de santé, vétérinaire',
            'Services agricoles, d’élevage, de pêche'
        ]
    }

    # Create dynamic models for each sector category
    for sector_name, categories in sectors_and_categories.items():
        sector, _ = Sector.objects.get_or_create(name=sector_name)
        for category_name in categories:
            sector_category, _ = SectorCategory.objects.get_or_create(sector=sector, name=category_name)
            # Dynamic model creation logic (to be implemented based on requirements)




class ScrapedData(models.Model):
    procedure = models.CharField(max_length=50, blank=True)
    categorie = models.ForeignKey(Sector, on_delete=models.SET_NULL, blank=True, null=True)
    publie_le = models.CharField(max_length=20, blank=True)
    org = models.CharField(max_length=20, blank=True)
    reference = models.CharField(max_length=20, blank=True)
    reference_hash = models.CharField(max_length=20, blank=True)
    objet = models.TextField(blank=True)
    acheteur_public = models.CharField(max_length=200, blank=True)
    lieu_execution = models.CharField(max_length=200, blank=True)
    date_limite = models.CharField(max_length=20, blank=True)
    
    # New fields with null=True
    estimation = models.CharField(max_length=50, blank=True, null=True)
    reserve_tpe_pme = models.CharField(max_length=3, blank=True, null=True)
    domaines_activite = models.CharField(max_length=200, blank=True, null=True)
    adresse_retrait_dossiers = models.CharField(max_length=200, blank=True, null=True)
    adresse_depot_offres = models.CharField(max_length=200, blank=True, null=True)
    lieu_ouverture_plis = models.CharField(max_length=200, blank=True, null=True)
    prix_acquisition_plans = models.CharField(max_length=50, blank=True, null=True)
    caution_provisoire = models.CharField(max_length=50, blank=True, null=True)
    qualifications = models.CharField(max_length=50, blank=True, null=True)
    agrements = models.CharField(max_length=50, blank=True, null=True)
    prospectus_notices_documents = models.CharField(max_length=50, blank=True, null=True)
    reunion = models.CharField(max_length=50, blank=True, null=True)
    visites_lieux = models.CharField(max_length=50, blank=True, null=True)
    variante = models.CharField(max_length=3, blank=True, null=True)
    contact_administratif = models.CharField(max_length=200, blank=True, null=True)
    
    json_raw = models.CharField(max_length=500, blank=True, null=True)

    categories = models.ManyToManyField(SectorCategory, related_name='scraped_data', blank=True)

    def __str__(self):
        return f'{self.reference} - {self.objet[:50]}'
