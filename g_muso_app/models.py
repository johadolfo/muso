from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
import datetime
import os

def filepath(request, filename):
    old_filename=filename
    timenow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('uploads/', filename)

# Create your models here.
gender_choice = {
    ('M', 'Masculin'),
    ('F', 'Feminin'),
}


typecotisation_choice = {
    ('Fonds de Credit', 'Fonds de Credit'),
    ('Fonds Urgences', 'Fonds Urgences'),
    ('Fonds de Fonctionnement', 'Fonds de Fonctionnement'),
}

class SessionYearModel(models.Model):
    id=models.AutoField(primary_key=True)
    session_start_year=models.DateField()
    session_end_year=models.DateField()
    objects = models.Manager()
    
class CustomUser(AbstractUser):
    user_type_data = ((1,"HOD"), (2, "Membre"))
    user_type=models.CharField(default=1, choices=user_type_data, max_length=10)

class AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Membre(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    codep =  models.CharField("CODE MEMBRE ",max_length=50, blank=True)
    nomp =  models.CharField("NOM MEMBRE ",max_length=50, blank=True, null=True)
    prenomp =  models.CharField("PRENOM MEMBRE ",max_length=50, blank=True, null=True)
    sexep =  models.CharField("SEXE MEMBRE ",max_length=50, blank=True, null=True, choices=gender_choice)
    #datenaissancep =  models.DateField("DATE DE NAISSANCE (YYYY-MM-DD)", default=datetime.date.today(), auto_now_add=False, auto_now=False, blank=True)
    lieunaissancep =  models.CharField("LIEU DE NAISSANCE ",max_length=50, blank=True, null=True)
    adressep =  models.CharField("ADRESSE ",max_length=50, blank=True, null=True)
    villep =  models.CharField("VILLE ",max_length=50, blank=True, null=True)
    communep =  models.CharField("COMMUNE ",max_length=50, blank=True, null=True)
    departementp =  models.CharField("DEPARTEMENT ",max_length=50, blank=True, null=True)
    paysp =  models.CharField("PAYS ",max_length=50, blank=True, null=True)
    nifp =  models.CharField("NIF/CIN ",max_length=50, blank=True, null=True)
    telephone1p =  models.CharField("TELEPHONE 1 ",max_length=50, blank=True, null=True)
    telephone2p =  models.CharField("TELEPHONE 2 ",max_length=50, blank=True, null=True)
    activiteprofessionp =  models.CharField("ACTIVITE / PROFESSION ",max_length=50, blank=True, null=True)
    referencep =  models.CharField("REFERENCE ",max_length=50, blank=True, null=True)
    dateajout =  models.DateTimeField(auto_now_add=False, auto_now=True, null=True)
    profile_pic=models.FileField(upload_to=filepath, null=True, blank=True)
    objects=models.Manager()

class tbcotisation(models.Model):
    typecotisation = models.CharField("Type de Cotisation",max_length=50, blank=True, null=True, choices=typecotisation_choice)
    montant = models.FloatField("Montant",default='0.0', blank=True, null=True)
    interet = models.FloatField("Interet",default='0.0', blank=True, null=True)
    balance = models.FloatField("Balance",default='0.0', blank=True, null=True)
    date_fait = models.DateTimeField("Date Cotisation (YYYY-MM-DD)",auto_now_add=False, auto_now=False)
    code_membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    penalite = models.FloatField("Penalite",default='0.0', blank=True, null=True)
    recu_par = models.CharField("Recu Par",max_length=50, blank=True, null=True)
    objects=models.Manager()


class tbcredit(models.Model):
    numero = models.CharField("Numero Credit",max_length=50, blank=True, primary_key=True)
    date_credit =  models.DateTimeField("Date Credit (YYYY-MM-DD)",auto_now_add=False, auto_now=False)
    nbre_de_mois = models.FloatField("Nombre de Mois",default='0.0', blank=True, null=True)
    date_debut =  models.DateTimeField("Date debut (YYYY-MM-DD)",auto_now_add=False, auto_now=False)
    date_fin = models.DateTimeField("Date Fin (YYYY-MM-DD)",auto_now_add=False, auto_now=False)
    montant_credit = models.FloatField("Montant Credit",default='0.0', blank=True, null=True)
    interet_credit = models.FloatField("Interet Credit",default='0.0', blank=True, null=True)
    code_membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    commentaire = models.TextField()
    valider_par = models.CharField("Valider Par",max_length=50, blank=True, null=True)
    credit_status = models.CharField("Status Credit",max_length=50, blank=True, default="En cour", null=True)
    objects=models.Manager()
    
class tbremboursement(models.Model):
    date_remb =  models.DateField("Date Remboursement (YYYY-MM-DD)",auto_now_add=False, auto_now=False, blank=True)
    codecredit=models.ForeignKey(tbcredit, on_delete=models.CASCADE,  blank=True)
    montant_a_remb = models.FloatField("Montant Credit",default='0.0', blank=True, null=True)
    capital_remb =  models.FloatField("Capital Remboursement",default='0.0', blank=True, null=True)
    interet_remb = models.FloatField("Interet Remboursement",default='0.0', blank=True, null=True)
    balance = models.FloatField("Balance",default='0.0', blank=True, null=True)
    penalite = models.FloatField("Penalite",default='0.0', blank=True, null=True)
    commentaire = models.TextField()
    faites_par = models.ForeignKey(Membre, on_delete=models.CASCADE)
    recu_par = models.CharField("Recu Par",max_length=50, blank=True, null=True)
    objects=models.Manager()

class LeaveReportMembre(models.Model):
    id=models.AutoField(primary_key=True)
    code_membre=models.ForeignKey(Membre, on_delete=models.CASCADE)
    leave_date=models.CharField(max_length=255)
    leave_message=models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()


class FeedBackMembre(models.Model):
    id=models.AutoField(primary_key=True)
    code_membre=models.ForeignKey(Membre, on_delete=models.CASCADE)
    feedback=models.TextField()
    feedback_reply=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()



class NotificationMembre(models.Model):
    id=models.AutoField(primary_key=True)
    code_membre=models.ForeignKey(Membre, on_delete=models.CASCADE)
    message=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created,**kwargs):
    if created:
        if instance.user_type==1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type==2:
            Membre.objects.create(admin=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, created,**kwargs):
    if created:
        if instance.user_type==1:
            instance.adminhod.save()
        if instance.user_type==2:
            instance.membre.save()
       