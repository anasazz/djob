from django.db import models

from django.utils import timezone



class Sector(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Sector"
        verbose_name_plural = "Sectors"
    
class SectorCategory(models.Model):
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Sector Category"
        verbose_name_plural = "Sector Categories"


class ProcedureChoice(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ScrapedData(models.Model):
    procedure = models.ManyToManyField(ProcedureChoice, blank=True)
    categorie = models.ForeignKey(Sector, on_delete=models.SET_NULL, blank=True, null=True)
    publie_le = models.DateTimeField(blank=True, null=True)  # Date and time field

    org = models.CharField(max_length=20, blank=True)
    reference = models.CharField(max_length=20, unique=True, blank=True)
    reference_hash = models.CharField(max_length=20, blank=True)
    objet = models.TextField(blank=True)
    acheteur_public = models.CharField(max_length=200, blank=True)
    lieu_execution = models.CharField(max_length=200, blank=True)
    date_limite = models.DateTimeField(blank=True, null=True)  # Date and time field
    
    # New fields with null=True
    estimation = models.CharField(max_length=50, blank=True, null=True)
    reserve_tpe_pme = models.CharField(max_length=3, blank=True, null=True)
    domaines_activite = models.ManyToManyField(SectorCategory, blank=True)
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
    def time_left(self):
            now = timezone.now()
            if self.date_limite and self.date_limite > now:
                delta = self.date_limite - now
                return delta
            return None