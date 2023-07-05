from django.contrib import admin
from django.db import models
# Register your models here.
from django.contrib.auth.admin import UserAdmin
from g_muso_app.models import CustomUser, Membre, tbcotisation, tbcredit, tbremboursement, tbmuso

admin.site.site_header = "MUTUEL SOLIDARITE"
admin.site.site_title = "MUSOES"
admin.site.index_title = "Manager"

class UserModel(UserAdmin):
    pass


class AdminMembre(admin.ModelAdmin):
    list_display = ('codep','nomp', 'prenomp','admin')

class AdminCotisation(admin.ModelAdmin):
    list_display = ('code_membre','id', 'typecotisation', 'montant', 'interet', 'penalite' )
    search_fields = ('typecotisation', )
    list_editable = ( 'interet', )

class AdminCredit(admin.ModelAdmin):
    list_display = ('code_membre','numero', 'date_credit', 'nbre_de_mois', 'date_debut', 'date_fin', 'montant_credit', 'interet_credit', 'valider_par', 'credit_status' )
    search_fields = ('code_membre', )

class AdminMuso(admin.ModelAdmin):
    list_display = ('id','codemuso', 'sigle', 'nom_muso', 'adresse_muso', 'telephone_muso', 'email_muso' )
    search_fields = ('nom_muso', )

class AdminRemboursement(admin.ModelAdmin):
    list_display = ('faites_par','date_remb', 'codecredit', 'montant_a_remb', 'capital_remb', 'interet_remb', 'balance', 'penalite', 'recu_par', 'commentaire' )
    search_fields = ('date_remb', )


admin.site.register(Membre, AdminMembre)
admin.site.register(tbcotisation, AdminCotisation)
admin.site.register(tbcredit,AdminCredit)
admin.site.register(tbremboursement,AdminRemboursement)
admin.site.register(CustomUser, UserModel)
admin.site.register(tbmuso, AdminMuso)