from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
import traceback
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from g_muso_app.models import CustomUser, Membre, tbcotisation, tbcredit,tbremboursement,FeedBackMembre,LeaveReportMembre,CustomUser, tbdepense, tbdetailproduit, tbdetailcredit, Comment, tbmuso
from .forms import EditMembreForm
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.core.paginator import Paginator
from django.db.models import Sum, Count
from django.db import connection
import csv
from django.db import transaction
from django.db.models import F
import io
import xlrd
import datetime , openpyxl
import pandas as pd
from django.shortcuts import redirect
from django.db.models.functions import Coalesce
from datetime import datetime, timedelta, date
from calendar import monthrange
from django.http import JsonResponse
from django.db.models import Func
from django.db.models.functions import Substr
from django.db.models import F, ExpressionWrapper, CharField
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission, PermissionsMixin,User,AbstractUser,Group,AbstractBaseUser
from django.contrib.auth import models as auth_models
from django.db.models import F, ExpressionWrapper, DecimalField
from django.db.models.functions import Coalesce
from django.db.models import Sum, FloatField
from django.db.models import F, ExpressionWrapper, FloatField, Subquery, OuterRef

def admin_home(request):
    current_user = request.user
    #membre_info=Membre.objects.get(id=current_user.id)
    #print(membre_info.muso,flat=True)
  
    #membre_count=Membre.objects.filter(membre_actif='True', muso=membre_info.muso_id).count()
    membre_count=Membre.objects.filter(membre_actif='True', admin__muso=current_user.muso).count()
    cotisation_info=tbcotisation.objects.all().filter(code_membre__admin__muso=current_user.muso,code_membre__membre_actif='True' )
    montant_tot = sum(cotisation_info.values_list('montant', flat=True))
    
    _credit  =tbcotisation.objects.filter(typecotisation__icontains='Fond de Credit', code_membre__admin__muso=current_user.muso,code_membre__membre_actif='True')
    montant_ccredit = sum(_credit.values_list('montant', flat=True))

    _ijans  =tbcotisation.objects.filter(typecotisation__icontains="Fond d'Urgence", code_membre__admin__muso=current_user.muso,code_membre__membre_actif='True')
    montant_ijans = sum(_ijans.values_list('montant', flat=True))

    _fonctionnement  =tbcotisation.objects.filter(typecotisation__icontains='Fond de Fonctionnement', code_membre__admin__muso=current_user.muso,code_membre__membre_actif='True')
    montant_fonk = sum(_fonctionnement.values_list('montant', flat=True))

    #rembourseent_infor=tbremboursement.objects.all().filter(faites_par__admin__muso=current_user.muso)
    #interet_tot = format(sum(rembourseent_infor.values_list('interet_remb', flat=True)),'.2f')
    cotisation_int = tbcotisation.objects.filter(code_membre__admin__muso=current_user.muso,code_membre__membre_actif='True')
    interet_tot = format(sum(cotisation_int.values_list('interet', flat=True)),'.2f')

    valeur2 = tbremboursement.objects.filter(faites_par__admin__muso=2).values('date_remb').order_by('date_remb').annotate(sum=Sum('interet_remb'))
  
    credit_info = tbcredit.objects.filter(credit_status__icontains="En cour", code_membre__admin__muso=current_user.muso)
    montant_credit = sum(credit_info.values_list('montant_credit', flat=True))
    #remb_info = tbremboursement.objects.all()
    remb_info = tbremboursement.objects.filter(faites_par__admin__muso=current_user.muso, codecredit__credit_status__icontains="En cour").values('codecredit_id').order_by('codecredit_id').annotate(capital_remb=Sum('capital_remb'))
    montant_rembourse = format(sum(remb_info.values_list('capital_remb', flat=True)),'.2f')

    return render(request, "hod_template/home_content.html",{ "credit_info":credit_info, "membre_count":membre_count, "montant_tot":montant_tot, "montant_credit":montant_credit,"montant_rembourse":montant_rembourse, "remb_info":remb_info, "montant_ccredit":montant_ccredit, "montant_ijans":montant_ijans, "montant_fonk":montant_fonk , "valeur2":valeur2, "interet_tot":interet_tot})
   
def add_personne(request):
    pass

def add_membre(request):
    #form = AddMembreForm()
    return render(request, "hod_template/add_membre_templates.html")

def add_membre_save(request):
    if request.method !="POST":
        return HttpResponse("Method Not Allowed")
    else:
        current_user = request.user
        muso_id = current_user.muso
        #code_muso = request.POST.get("muso_id")
        #muso_id = tbmuso.objects.get(id=code_muso)
        prenomp = request.POST.get("prenomp")
        nomp = request.POST.get("nomp")
        codep = request.POST.get("codep")
        email = request.POST.get("emailp")
        password = request.POST.get("passwordp")
        adressep = request.POST.get("adressep")
        sexep = request.POST.get("sexep")

        #datenaissancep = form.cleaned_data["datenaissancep"]
        villep = request.POST.get("villep")
        communep = request.POST.get("communep")
        departementp = request.POST.get("departementp")
        paysp = request.POST.get("paysp")
        nifp = request.POST.get("nifp")
        
        telephone1p = request.POST.get("telephone1p")
        telephone2p = request.POST.get("telephone2p")
        activiteprofessionp = request.POST.get("activiteprofessionp")
        referencep = request.POST.get("referencep")
        lieunaissancep = request.POST.get("lieunaissancep")
        #muso = form.cleaned_data["muso"]
        
        profile_pic = request.FILES['profile_pic']
        fs = FileSystemStorage()
        filename = fs.save(profile_pic.name, profile_pic)
        profile_pic_url = fs.url(filename)

        try:
            user=CustomUser.objects.create_user(username=prenomp +' '+ nomp, password=password, email=email, last_name=nomp, first_name=prenomp, user_type=2, muso=muso_id )
            user.membre.codep=codep
            user.membre.nomp = nomp
            user.membre.prenomp=prenomp
            user.membre.sexep = sexep
            #user.membre.datenaissancep = datenaissancep
            user.membre.lieunaissancep=lieunaissancep
            user.membre.adressep=adressep
            user.membre.villep=villep
            user.membre.communep = communep
            user.membre.departementp=departementp
            user.membre.paysp = paysp
            user.membre.nifp=nifp
            user.membre.telephone1p = telephone1p
            user.membre.telephone2p=telephone2p
            user.membre.activiteprofessionp = activiteprofessionp
            user.membre.referencep = referencep
            user.membre.profile_pic=profile_pic_url
            #user.membre.muso = muso=muso_id
            user.membre.save()
           
            messages.success(request,"Successfully Added membre")
            return HttpResponseRedirect(reverse("add_membre")) 
        except Exception as e:
            messages.error(request,traceback.format_exc())
            return HttpResponseRedirect(reverse("add_membre"))


#@login_required
def add_tbcotisation(request):
    #if not request.user.has_perm('g_muso_app.add_tbcotisation'):
        #is_button_disabled = False
        #return HttpResponseForbidden('Vous n\'avez pas l\'autorisation d\'accéder à cette page.')
    # Le reste du code pour traiter la vue lorsqu'un utilisateur a l'autorisation
    is_button_disabled = True
    current_user = request.user
    muso_id = current_user.muso
    cotisations = tbcotisation.objects.all()
    membre_info = Membre.objects.filter(admin__muso=current_user.muso)
    membres = CustomUser.objects.filter(user_type=2, muso=current_user.muso)
    return render(request, "hod_template/add_cotisation_template.html", {"is_button_disabled": is_button_disabled, "membres":membres, "cotisations":cotisations, "membre_info":membre_info})

def add_cotisation_save(request):
  
    if request.method !="POST":
        return HttpResponse("Method Not Allowed")
    else:
        current_user = request.user
        muso_id = current_user.muso
        cotisations = tbcotisation.objects.filter(code_membre__admin__muso = muso_id)

        code_membres = request.POST.get("membre")
        code_membre=Membre.objects.get(id=code_membres)
        #cotisation.code_membre=code_membre
        montant_recu = request.POST.get("montant_cotis")
        interet_recu = request.POST.get("interet_")
        penalite_recu = request.POST.get("penalite_")
        type_cotisation_recu = request.POST.get("type_cotisation")
        balance_recu = request.POST.get("balance")
        date_fait = request.POST.get("date_fait")
        penalite_recu = request.POST.get("penalite_")

        try:
            cotisation=tbcotisation(typecotisation=type_cotisation_recu, montant=float(montant_recu), interet=float(interet_recu), balance=float(balance_recu), date_fait=date_fait, code_membre=code_membre, penalite=float(penalite_recu), recu_par=request.user.username)
            cotisation.save()
            messages.success(request,"Successfully Added cotisation")
            return HttpResponseRedirect(reverse("add_tbcotisation")) 
        except Exception as e:
            messages.error(request,traceback.format_exc())
            return HttpResponseRedirect(reverse("add_tbcotisation"))
        # except:
        #     messages.error(request,"Failed to Add cotisation")
        #     return HttpResponseRedirect(reverse("add_cotisation")) 

def add_credit(request):
    current_user = request.user
    muso_id = current_user.muso
    credits = tbcredit.objects.filter(code_membre__admin__muso=current_user.muso)
    membre_info = Membre.objects.filter(admin__muso=current_user.muso)
    membres = CustomUser.objects.filter(user_type=2, muso=current_user.muso)
    return render(request, "hod_template/add_credit_template.html", {"membres":membres, "credits":credits, "membre_info":membre_info})

def add_credit_save(request):
    if request.method !="POST":
        return HttpResponse("Method Not Allowed")
    else:
        code_membres = request.POST.get("membre")
        code_membre=Membre.objects.get(id=code_membres)
        #cotisation.code_membre=code_membre
        numero_credit = request.POST.get("numero_credit")
        date_credit = request.POST.get("date_credit")
        date_debut = request.POST.get("date_debut")
        date_fin = request.POST.get("date_fin")
        nbre_de_mois = request.POST.get("nbre_mois")
        montant_recu = request.POST.get("montant_credit")
        interet_recu = request.POST.get("interet_credit")
        commentaire = request.POST.get("commentaire")
        valider_par = request.POST.get("valider_par")
       

        try:
            credit=tbcredit(numero=numero_credit, date_credit=date_credit, nbre_de_mois=nbre_de_mois,date_debut=date_debut, date_fin=date_fin, montant_credit=float(montant_recu), interet_credit=float(interet_recu), code_membre=code_membre, commentaire=commentaire, valider_par=valider_par)
            credit.save()
            messages.success(request,"Successfully Added credit")
            return HttpResponseRedirect(reverse("add_credit")) 
        except Exception as e:
            messages.error(request,traceback.format_exc())
            return HttpResponseRedirect(reverse("add_credit"))

def add_remboursement(request):
    current_user = request.user
    muso_id = current_user.muso
    remboursements = tbremboursement.objects.all()
    credits=tbcredit.objects.all()
    membre_info = Membre.objects.filter(admin__muso=current_user.muso)
    membres = CustomUser.objects.filter(user_type=2,muso=current_user.muso)
    return render(request, "hod_template/add_remboursement_template.html", {"membres":membres, "remboursements":remboursements, "membre_info":membre_info, "credits":credits})

def add_remboursement_save(request):
 
    if request.method !="POST":
        return HttpResponse("Method Not Allowed")
    else:
        code_membres = request.POST.get("membre")
        code_membre=Membre.objects.get(id=code_membres)
        date_remboursement = request.POST.get("date_remboursement")
        numero_credit = request.POST.get("numero_credit")
        code_credit=tbcredit.objects.get(numero=numero_credit)
        montant_recu = request.POST.get("montant_a_rembourser")
        capital_recu = request.POST.get("capital_a_rembourser")
        interet_recu = request.POST.get("interet_a_rembourser")
        balance_recu = request.POST.get("balance_remb")
        penalite_recu = request.POST.get("penalite_remb")
        commentaire = request.POST.get("commentaire")
        valider_par = request.POST.get("recu_par")

        try:
            remboursement=tbremboursement(date_remb=date_remboursement,  montant_a_remb=float(montant_recu),capital_remb=float(capital_recu), interet_remb=float(interet_recu), balance=float(balance_recu), penalite=float(penalite_recu), commentaire=commentaire, recu_par=valider_par, codecredit=code_credit, faites_par=code_membre)
            remboursement.save()
            # editer status_credit, si la qtite de remboursement arrive a sa fin
            nbre_remb = tbremboursement.objects.filter(codecredit_id = code_credit).count()
            nbreM = tbcredit.objects.get(numero = request.POST.get("numero_credit"))
            if (nbre_remb == nbreM.nbre_de_mois ):
                credit=tbcredit.objects.get(numero=request.POST.get("numero_credit"))
                credit.credit_status = 'Termine'
                credit.save()
        
            messages.success(request,"Successfully Added remboursement")
            return HttpResponseRedirect(reverse("add_remboursement")) 
        except Exception as e:
            messages.error(request,traceback.format_exc())
            return HttpResponseRedirect(reverse("add_remboursement"))
        
def add_detailalimentaire(request):
    current_user = request.user
    muso_id = current_user.muso
    detailalimentaires = tbdetailproduit.objects.all()
    credits=tbcredit.objects.all()
    membre_info = Membre.objects.filter(admin__muso=current_user.muso)
    membres = CustomUser.objects.filter(user_type=2,muso=current_user.muso)
    return render(request, "hod_template/add_detailalimentaire_template.html", {"membres":membres, "detailalimentaires":detailalimentaires, "membre_info":membre_info, "credits":credits})

def add_detailalimentaire_save(request):
    if request.method !="POST":
        return HttpResponse("Method Not Allowed")
    else:
        numero_credit = request.POST.get("numero_credit")
        code_credit=tbcredit.objects.get(numero=numero_credit)
        description = request.POST.get("description")
        quantite= request.POST.get("quantite_prod")
        unite= request.POST.get("unite")
        prix_unitaire = request.POST.get("prix_unitaire")
        prix_total = float(quantite)*float(prix_unitaire)
        frais_transport = request.POST.get("frais_transport")
        prix_revient = float(prix_total)+float(frais_transport)
        prix_vente = float(prix_revient)+(float(prix_revient)*0.01)

        try:
            detailproduct=tbdetailproduit(codecredit=code_credit,  description=description, quantite_prod=float(quantite), unite=unite, prix_unitaire=float(prix_unitaire), prix_total=float(prix_total), frais_transport=float(frais_transport), prix_de_revient=float(prix_revient), prix_de_vente=float(prix_vente))
            detailproduct.save()
        
            messages.success(request,"Successfully Added Detail Product")
            return HttpResponseRedirect(reverse("add_detailalimentaire")) 
        except Exception as e:
            messages.error(request,traceback.format_exc())
            return HttpResponseRedirect(reverse("add_detailalimentaire"))


def add_depense(request):
    depenses = tbdepense.objects.all()
    return render(request, "hod_template/add_depense_template.html", {"depenses":depenses})

def add_depense_save(request):
    current_user = request.user
    muso_id = current_user.muso
 
    if request.method !="POST":
        return HttpResponse("Method Not Allowed")
    else:
        date_depense = request.POST.get("date_depense")
        description = request.POST.get("description")
        depense_unit = request.POST.get("depense_unit")
        quantite_dep = request.POST.get("quantite_dep")

        try:
            depense=tbdepense(date_depense=date_depense,  description=description, depense_unit=float(depense_unit), quantite_dep=float(quantite_dep), muso_id=muso_id)
            depense.save()
        
            messages.success(request,"Successfully Added Depense")
            return HttpResponseRedirect(reverse("add_depense")) 
        except Exception as e:
            messages.error(request,traceback.format_exc())
            return HttpResponseRedirect(reverse("add_depense"))
        

def add_cotisationRemplacerMEMBRE_save(request):
    if request.method !="POST":
        return HttpResponse("Method Not Allowed")
    else:
        code_ancienMembre = request.POST.get("code_amembre")
        code_nouveauMembre = request.POST.get("code_nmembre")
        code_nmembre=Membre.objects.get(id=code_nouveauMembre)

        try:

            # Effectuer la sélection
            result = tbcotisation.objects.filter(code_membre=int(code_ancienMembre))

            # Parcourir les résultats et effectuer les modifications
            for row in result:
                row.code_membre = code_nmembre
                row.save()

            messages.success(request,"Successfully Added cotisation")
            return HttpResponseRedirect(reverse("add_cotisation")) 
        except Exception as e:
            messages.error(request,traceback.format_exc())
            return HttpResponseRedirect(reverse("add_cotisation"))

        
def add_cotisationnouveauMEMBRE_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        code_membrean = request.POST.get("code_amembre")
        code_ancienMembre=Membre.objects.get(id=code_membrean)

        #code_ancienMembre = request.POST.get("code_amembre")
        code_membrenou = request.POST.get("code_nmembre")
        code_nmembre=Membre.objects.get(id=code_membrenou)
        #code_nouveauMembre = request.POST.get("code_nmembre")
        #code_nmembre = Membre.objects.get(id=code_nouveauMembre)
        choix_ = request.POST.get("choix")

        if choix_ == "Tout":
            try:
                # Effectuer la sélection
                result = tbcotisation.objects.filter(code_membre=code_ancienMembre)

                # Parcourir les résultats et effectuer les modifications
                for row in result:
                    cotisation = tbcotisation(
                        typecotisation=row.typecotisation,
                        montant=row.montant,
                        interet=row.interet,
                        balance=row.balance,
                        date_fait=row.date_fait,
                        code_membre=code_nmembre,
                        penalite=row.penalite,
                        recu_par=request.user.username
                    )
                    cotisation.save()

                messages.success(request, "Successfully added cotisation")
                return HttpResponseRedirect(reverse("add_tbcotisation"))
            except Exception as e:
                messages.error(request, traceback.format_exc())
                return HttpResponseRedirect(reverse("add_tbcotisation"))
            
        elif choix_ == "Fond d'Urgence":
            try:
                # Effectuer la sélection
                #result = tbcotisation.objects.filter(code_membre=int(code_ancienMembre) )
                result = tbcotisation.objects.filter(code_membre_id=code_ancienMembre, typecotisation="Fond d'Urgence")
                # Parcourir les résultats et effectuer les modifications
                for row in result:
                    cotisation = tbcotisation(
                        typecotisation=row.typecotisation,
                        montant=row.montant,
                        interet=row.interet,
                        balance=row.balance,
                        date_fait=row.date_fait,
                        code_membre=code_nmembre,
                        penalite=row.penalite,
                        recu_par=request.user.username
                    )
                    cotisation.save()

                messages.success(request, "Successfully added cotisation")
                return HttpResponseRedirect(reverse("add_tbcotisation"))
            except Exception as e:
                messages.error(request, traceback.format_exc())
                return HttpResponseRedirect(reverse("add_tbcotisation"))
            
        elif choix_ == "Fond de Fonctionnement":
            try:
                # Effectuer la sélection
                result = tbcotisation.objects.filter(code_membre_id=code_ancienMembre, typecotisation="Fond de Fonctionnement")

                # Parcourir les résultats et effectuer les modifications
                for row in result:
                    cotisation = tbcotisation(
                        typecotisation=row.typecotisation,
                        montant=row.montant,
                        interet=row.interet,
                        balance=row.balance,
                        date_fait=row.date_fait,
                        code_membre=code_nmembre,
                        penalite=row.penalite,
                        recu_par=request.user.username
                    )
                    cotisation.save()

                messages.success(request, "Successfully added cotisation")
                return HttpResponseRedirect(reverse("add_tbcotisation"))
            except Exception as e:
                messages.error(request, traceback.format_exc())
                return HttpResponseRedirect(reverse("add_tbcotisation"))
            
        elif choix_ == "Fond de Credit":
            try:
                # Effectuer la sélection
                result = tbcotisation.objects.filter(code_membre_id=code_ancienMembre, typecotisation="Fond de Credit")

                # Parcourir les résultats et effectuer les modifications
                for row in result:
                    cotisation = tbcotisation(
                        typecotisation=row.typecotisation,
                        montant=row.montant,
                        interet=row.interet,
                        balance=row.balance,
                        date_fait=row.date_fait,
                        code_membre=code_nmembre,
                        penalite=row.penalite,
                        recu_par=request.user.username
                    )
                    cotisation.save()

                messages.success(request, "Successfully added cotisation")
                return HttpResponseRedirect(reverse("add_tbcotisation"))
            except Exception as e:
                messages.error(request, traceback.format_exc())
                return HttpResponseRedirect(reverse("add_tbcotisation"))
            
        elif choix_ == "Fond d'urgence et de Fonctionnement'":
            try:
                # Effectuer la sélection
                result =  tbcotisation.objects.filter(code_membre_id=code_ancienMembre, typecotisation__in=["Fond d'Urgence", "Fond de Fonctionnement"])
                # Parcourir les résultats et effectuer les modifications
                for row in result:
                    cotisation = tbcotisation(
                        typecotisation=row.typecotisation,
                        montant=row.montant,
                        interet=row.interet,
                        balance=row.balance,
                        date_fait=row.date_fait,
                        code_membre=code_nmembre,
                        penalite=row.penalite,
                        recu_par=request.user.username
                    )
                    cotisation.save()

                messages.success(request, "Successfully added cotisation")
                return HttpResponseRedirect(reverse("add_tbcotisation"))
            except Exception as e:
                messages.error(request, traceback.format_exc())
                return HttpResponseRedirect(reverse("add_tbcotisation"))
              
             
def manage_muso(request):
    pass
   
def manage_membre(request):
    #membre_muso = CustomUser.objects.filter(muso=2)
    #ModelB.objects.select_related('a').all()
    #membres = Membre.objects.prefetch_related(Prefetch('CustomUser', queryset=membre_muso))
    #membres =Membre.objects.all().prefetch_related('CustomUser').filter(muso=2)
    current_user = request.user
    muso_id = current_user.muso_id
    membres = Membre.objects.filter(admin__muso=current_user.muso)

    if 'q' in request.GET:
        q = request.GET['q']
        
        all_membre_list = Membre.objects.filter( Q(nomp__icontains=q) | Q(prenomp__icontains=q) | Q(codep__icontains=q) | Q(referencep__icontains=q))
    else:
        all_membre_list = Membre.objects.filter(admin__muso=current_user.muso)
        #all_membre_list = Membre.objects.prefetch_related('CustomUser').filter(muso=2)
    paginator = Paginator(all_membre_list,15,orphans=5)
    page = request.GET.get('page')
    membres = paginator.get_page(page)
    return render(request, "hod_template/manage_membre_template.html", { "membres": membres })

#@login_required
def view_tbcotisation(request):

    is_button_disabled = True
    current_user = request.user
    muso_id = current_user.muso_id
    cotisations = tbcotisation.objects.filter(code_membre__admin__muso = muso_id).order_by('-date_fait')
    
    if 'q' in request.GET:
        q = request.GET['q']
        id_membre = Membre.objects.raw('select id from membre  where codep =%s', [q])
        all_cotisation_list = tbcotisation.objects.filter( Q(typecotisation__icontains=q) | Q(date_fait__icontains=q) | Q(id__icontains=id_membre)).order_by('-date_fait')
    else:
        all_cotisation_list = tbcotisation.objects.filter(code_membre__admin__muso = muso_id).order_by('-date_fait')
    paginator = Paginator(all_cotisation_list,25)
    page = request.GET.get('page')
    cotisations = paginator.get_page(page)
    return render(request, "hod_template/manage_cotisation_template.html", { "cotisations":cotisations, "is_button_disabled": is_button_disabled })


def manage_credit(request):
    #credits = tbcredit.objects.filter(date_credit__iso_year=2021)
    credits = tbcredit.objects.order_by('-date_credit')
    return render(request, "hod_template/manage_credit_template.html", { "credits":credits })

def liste_credit(request):
    current_user = request.user
    muso_id = current_user.muso_id
    credits = tbcredit.objects.filter(code_membre__admin__muso = muso_id).order_by('-date_credit')

    if 'q' in request.GET:
        q = request.GET['q']
        all_credit_list = tbcredit.objects.filter(Q(code_membre_id__in=Membre.objects.filter(admin_id__in=CustomUser.objects.filter(muso_id=muso_id))),  Q(numero__icontains=q)  | Q(date_credit__icontains=q) ).order_by('-date_credit')
    else:
        all_credit_list = tbcredit.objects.filter(code_membre__admin__muso = muso_id).order_by('-date_credit')
    paginator = Paginator(all_credit_list,25)
    page = request.GET.get('page')
    credits = paginator.get_page(page)
    qte_credit =tbcredit.objects.filter(code_membre__admin__muso = muso_id).count()
    qte_credit_en_cours = tbcredit.objects.filter(credit_status='En cour', code_membre__admin__muso = muso_id).count()
    qte_credit_fini=tbcredit.objects.filter(credit_status='Termine', code_membre__admin__muso = muso_id).count()
    
    return render(request, "hod_template/manage_credit_template.html", { "credits":credits, "qte_credit_en_cours":qte_credit_en_cours,"qte_credit_fini":qte_credit_fini, "qte_credit":qte_credit  })

def liste_credit_encour(request):
    current_user = request.user
    muso_id = current_user.muso_id
    credits = tbcredit.objects.filter(credit_status='En cour', code_membre__admin__muso = muso_id).order_by('-date_credit')

    if 'q' in request.GET:
        q = request.GET['q']
        all_credit_list = tbcredit.objects.filter(  Q(numero__icontains=q)  | Q(date_credit__icontains=q) ).order_by('-date_credit')
    else:
        all_credit_list = tbcredit.objects.filter(credit_status='En cour', code_membre__admin__muso = muso_id).order_by('-date_credit')
    paginator = Paginator(all_credit_list,25)
    page = request.GET.get('page')
    credits = paginator.get_page(page)
    qte_credit =tbcredit.objects.filter(credit_status='En cour',code_membre__admin__muso = muso_id).count()
    
    return render(request, "hod_template/liste_creditencour_template.html", { "credits":credits, "qte_credit":qte_credit  })


def manage_creditalimentaire(request):
    current_user = request.user
    muso_id = current_user.muso_id
    creditalimentaires = tbcredit.objects.filter(Q(numero__in=tbdetailproduit.objects.filter(codecredit_id__in=tbcredit.objects.values('numero')).values('codecredit_id')) &Q(code_membre_id__in=Membre.objects.filter(admin_id__in=CustomUser.objects.filter(muso_id=muso_id).values('id')).values('id'))).order_by('-date_credit')
     
    if 'q' in request.GET:
        q = request.GET['q']
        all_credit_list = tbcredit.objects.filter(numero=tbdetailproduit.objects.filter(codecredit_id=tbcredit.numero) and Q(numero__icontains=q)  | Q(date_credit__icontains=q) ).order_by('-date_credit')
    else:
        
        all_credit_list = tbcredit.objects.filter(numero__in=tbdetailproduit.objects.filter(codecredit_id__in=tbcredit.objects.values('numero')),code_membre_id__in=Membre.objects.filter(admin__id__in=CustomUser.objects.filter(muso_id=muso_id)).values('id')).order_by('-date_credit')
    
    paginator = Paginator(all_credit_list,25)
    page = request.GET.get('page')
    qte_credit= tbcredit.objects.filter(Q(numero__in=tbdetailproduit.objects.filter(codecredit_id__in=tbcredit.objects.values('numero')).values('codecredit_id')) &Q(code_membre_id__in=Membre.objects.filter(admin_id__in=CustomUser.objects.filter(muso_id=muso_id).values('id')).values('id'))).count()
    qte_credit_en_cours = tbcredit.objects.filter( Q(credit_status="En cour", numero__in=tbdetailproduit.objects.filter(codecredit_id__in=tbcredit.objects.values('numero')).values('codecredit_id')) &Q(code_membre_id__in=Membre.objects.filter(admin_id__in=CustomUser.objects.filter(muso_id=muso_id).values('id')).values('id'))).count()
    qte_credit_fini = tbcredit.objects.filter(Q(credit_status="Termine",numero__in=tbdetailproduit.objects.filter(codecredit_id__in=tbcredit.objects.values('numero')).values('codecredit_id')) &Q(code_membre_id__in=Membre.objects.filter(admin_id__in=CustomUser.objects.filter(muso_id=muso_id).values('id')).values('id'))).count()
    return render(request, "hod_template/manage_creditalimentaire_template.html", { "creditalimentaires":creditalimentaires, "qte_credit_en_cours":qte_credit_en_cours,"qte_credit_fini":qte_credit_fini, "qte_credit":qte_credit  })

def divide_by_100(value):
    return value / 100

def manage_detailalimentaire(request):
    current_user = request.user
    muso_id = current_user.muso_id
    detalimentaires = tbdetailproduit.objects.filter(codecredit_id__in=tbcredit.objects.filter(Q(code_membre_id__in=Membre.objects.filter(admin_id__in=CustomUser.objects.filter(muso_id=muso_id).values('id')).values('id'))).values('numero'))
    if 'q' in request.GET:
        q = request.GET['q']
        all_detailproduit_list = tbdetailproduit.objects.filter(codecredit__in=tbcredit.objects.filter(Q(code_membre_id__in=Membre.objects.filter(admin_id__in=CustomUser.objects.filter(muso_id=muso_id).values('id')).values('id')),numero=q).values('numero'))
    else:
        all_detailproduit_list = tbdetailproduit.objects.filter(codecredit_id__in=tbcredit.objects.filter(Q(code_membre_id__in=Membre.objects.filter(admin_id__in=CustomUser.objects.filter(muso_id=muso_id).values('id')).values('id'))).values('numero'))
    paginator = Paginator(all_detailproduit_list,15)
    page = request.GET.get('page')
    detalimentaires = paginator.get_page(page)
    return render(request, "hod_template/manage_detailalimentaire_template.html", {"detalimentaires": detalimentaires})


def manage_remboursement(request):
    current_user = request.user
    muso_id = current_user.muso_id
    rembs = tbremboursement.objects.filter(faites_par__admin__muso = muso_id).order_by('-date_remb')

    if 'q' in request.GET:
        q = request.GET['q']
        all_remboursement_list = tbremboursement.objects.filter(Q(codecredit_id=q)).order_by('-date_remb')
    else:
        all_remboursement_list = tbremboursement.objects.filter(faites_par__admin__muso = muso_id).order_by('-date_remb')
    paginator = Paginator(all_remboursement_list,15)
    page = request.GET.get('page')
    rembs = paginator.get_page(page)

    return render(request, "hod_template/manage_remboursement_template.html", { "rembs":rembs })

def manage_depense(request):
    current_user = request.user
    muso_id = current_user.muso_id
    depenses = tbdepense.objects.filter(muso_id=muso_id).order_by('-date_depense')

    if 'q' in request.GET:
        q = request.GET['q']
        all_depense_list = tbdepense.objects.filter(muso_id=muso_id  & Q(id=q)).order_by('-date_depense')
    else:
        all_depense_list = tbdepense.objects.filter(muso_id=muso_id).order_by('-date_depense')
    paginator = Paginator(all_depense_list,15)
    page = request.GET.get('page')
    rembs = paginator.get_page(page)
    depense_info=tbdepense.objects.filter(muso_id=muso_id)
    depense_total = sum(depense_info.values_list('depense_unit', flat=True))

    return render(request, "hod_template/manage_depense_template.html", { "depenses":depenses, "depense_total":depense_total })

def statistique_credit(request):
    current_user = request.user
    muso_id = current_user.muso_id
    
    subquery = tbremboursement.objects.filter(codecredit_id=OuterRef('numero')).values('codecredit_id')
    credit_info = tbcredit.objects.annotate(
        montant_rembourser=ExpressionWrapper(
            (F('montant_credit') * F('interet_credit') * F('nbre_de_mois')) + F('montant_credit'),
            output_field=FloatField()
        ),
        interet_total_credit=ExpressionWrapper(
            ((F('montant_credit') * F('interet_credit') * F('nbre_de_mois')) + F('montant_credit')) - F('montant_credit'),
            output_field=FloatField()
        ),
    ).filter(
        code_membre__id=F('code_membre_id'),
        code_membre__admin__id=F('code_membre__admin__id'),
        code_membre__admin__muso_id=muso_id,
        pk__in=Subquery(subquery)
    ).values(
        'numero',
        'montant_credit',
        'date_debut',
        'montant_rembourser',
        'interet_total_credit'
    ).order_by('date_debut')
    
    result_tot = tbcredit.objects.filter(
        code_membre__id=F('code_membre_id'),
        code_membre__admin__id=F('code_membre__admin__id'),
        code_membre__admin__muso_id=muso_id,
        tbremboursement__codecredit_id=F('numero')
    ).aggregate(
        sum_montant_credit=Sum('montant_credit'),
        montant_rembourser=ExpressionWrapper(
            Sum((F('montant_credit') * F('interet_credit') * F('nbre_de_mois')) + F('montant_credit')),
            output_field=FloatField()
        ),
        interet_total_credit=ExpressionWrapper(
            Sum(((F('montant_credit') * F('interet_credit') * F('nbre_de_mois')) + F('montant_credit')) - F('montant_credit')),
            output_field=FloatField()
        )
    )

    
    query = """
        SELECT SUM(a.montant_credit * a.interet_credit) AS interet_anticipe
        FROM g_muso_app_tbcredit a
        INNER JOIN g_muso_app_tbremboursement b ON a.numero = b.codecredit_id
        INNER JOIN g_muso_app_membre c ON a.code_membre_id = c.id
        INNER JOIN g_muso_app_customuser d ON c.admin_id = d.id
        WHERE b.interet_remb = 0 AND d.muso_id = %s
    """

    with connection.cursor() as cursor:
        cursor.execute(query, [int(muso_id)])
        result = cursor.fetchone()
    interet_anticipe = result[0] if result else 0

    if 'q' in request.GET:
        q = request.GET['q']
        subquery = tbremboursement.objects.filter(codecredit_id=OuterRef('numero')).values('codecredit_id')
        all_credit_info = tbcredit.objects.annotate(
            montant_rembourser=ExpressionWrapper(
                (F('montant_credit') * F('interet_credit') * F('nbre_de_mois')) + F('montant_credit'),
                output_field=FloatField()
            ),
            interet_total_credit=ExpressionWrapper(
                ((F('montant_credit') * F('interet_credit') * F('nbre_de_mois')) + F('montant_credit')) - F('montant_credit'),
                output_field=FloatField()
            ),
        ).filter(
            code_membre__id=F('code_membre_id'),
            code_membre__admin__id=F('code_membre__admin__id'),
            code_membre__admin__muso_id=muso_id,
            numero=q,
            pk__in=Subquery(subquery)
        ).values(
            'numero',
            'montant_credit',
            'date_debut',
            'montant_rembourser',
            'interet_total_credit'
        ).order_by('date_debut')
        #///////////////////////////////////
        query = """
            SELECT SUM(a.montant_credit * a.interet_credit) AS interet_anticipe
            FROM g_muso_app_tbcredit a
            INNER JOIN g_muso_app_tbremboursement b ON a.numero = b.codecredit_id
            INNER JOIN g_muso_app_membre c ON a.code_membre_id = c.id
            INNER JOIN g_muso_app_customuser d ON c.admin_id = d.id
            WHERE b.interet_remb = 0 AND d.muso_id = %s and a.numero=%s
        """

        with connection.cursor() as cursor:
            cursor.execute(query, [int(muso_id), q])
            result = cursor.fetchone()
        interet_anticipe = result[0] if result else 0
        #/////////////////////////////////////////////
        result_tot = 0
    else:
        all_credit_info = credit_info
    paginator = Paginator(all_credit_info,15)
    page = request.GET.get('page')
    credit_info = paginator.get_page(page)
    return render(request, "hod_template/statistique_credit_template.html", { "credit_info":credit_info, "result_tot":result_tot, "interet_anticipe":interet_anticipe })


def statistique_remboursement(request):
    current_user = request.user
    muso_id = current_user.muso_id

    query = """
        SELECT 
    codecredit_id,
    COUNT(g_muso_app_tbremboursement.id) AS quantite_remboursement,
	(g_muso_app_tbcredit.nbre_de_mois- COUNT(g_muso_app_tbremboursement.id)) as Qtee_restant,
    SUM(capital_remb) + SUM(interet_remb) AS montant_total_rembourse,
	(((capital_remb+interet_remb)*nbre_de_mois) - (SUM(capital_remb) + SUM(interet_remb))) AS montant_total_Restant,
    SUM(interet_remb) AS total_interet,
	(interet_remb*nbre_de_mois) - SUM(interet_remb) AS total_interet_restant,
    SUM(penalite) AS total_penalite
    FROM
        g_muso_app_tbremboursement,g_muso_app_membre ,g_muso_app_customuser, g_muso_app_tbcredit
    WHERE
        g_muso_app_tbremboursement.faites_par_id = g_muso_app_membre.id and g_muso_app_membre.admin_id = g_muso_app_customuser.id and g_muso_app_tbremboursement.codecredit_id = g_muso_app_tbcredit.numero and g_muso_app_customuser.muso_id = %s
    GROUP BY
        codecredit_id
    ORDER BY
        codecredit_id ASC
    """

    with connection.cursor() as cursor:
        cursor.execute(query, [int(muso_id)])
        remboursement_info = cursor.fetchall()

    if 'q' in request.GET:
        q = request.GET['q']
        queryparametre = """
            SELECT 
        codecredit_id,
        COUNT(g_muso_app_tbremboursement.id) AS quantite_remboursement,
        (g_muso_app_tbcredit.nbre_de_mois- COUNT(g_muso_app_tbremboursement.id)) as Qtee_restant,
        SUM(capital_remb) + SUM(interet_remb) AS montant_total_rembourse,
        ((montant_a_remb*nbre_de_mois) - (SUM(capital_remb) + SUM(interet_remb))) AS montant_total_Restant,
        SUM(interet_remb) AS total_interet,
        (interet_remb*nbre_de_mois) - SUM(interet_remb) AS total_interet_restant,
        SUM(penalite) AS total_penalite
        FROM
            g_muso_app_tbremboursement,g_muso_app_membre ,g_muso_app_customuser, g_muso_app_tbcredit
        WHERE
            g_muso_app_tbremboursement.faites_par_id = g_muso_app_membre.id and g_muso_app_membre.admin_id = g_muso_app_customuser.id and g_muso_app_tbremboursement.codecredit_id = g_muso_app_tbcredit.numero and g_muso_app_customuser.muso_id = %s and g_muso_app_tbcredit.numero=%s
        GROUP BY
            codecredit_id
        ORDER BY
            codecredit_id ASC
        """

        with connection.cursor() as cursor:
            cursor.execute(queryparametre, [int(muso_id), q])
            all_remboursement_info = cursor.fetchall()

        #all_remboursement_info = tbremboursement.objects.filter(  Q(codecredit_id=q) ).values('codecredit_id').annotate(total=Count('codecredit_id'),faites_par__admin__muso = muso_id, sum=Sum('capital_remb')).order_by('-date_remb')
    else:
        #all_remboursement_info = tbremboursement.objects.filter(faites_par__admin__muso = muso_id).select_related("tbcredit").values('codecredit_id').annotate(total=Count('codecredit_id'), sum=Sum('capital_remb')).order_by('-date_remb')
        all_remboursement_info = remboursement_info
    paginator = Paginator(all_remboursement_info,15)
    page = request.GET.get('page')
    remboursement_info = paginator.get_page(page)
    return render(request, "hod_template/statistique_remboursement_template.html", { "remboursement_info":remboursement_info })

def interets_ajoutes(request):
    current_user = request.user
    muso_id = current_user.muso
    qte_membre=Membre.objects.filter(admin__muso=current_user.muso).count()

    remboursement_info = tbremboursement.objects.filter(
    faites_par_id__admin_id__muso_id=muso_id
    ).values('date_remb').annotate(
        total_interet=Sum('interet_remb'),
        total_penalite=Sum('penalite'),
        montant_total_rembourse=Sum('montant_a_remb') + Sum('interet_remb'),
        quantite_remboursement=Count('id')
    ).order_by('date_remb')
    cotisation_info = tbcotisation.objects.filter(code_membre__admin_id__muso_id=muso_id)
    penalite_total_cot =sum(cotisation_info.values_list('penalite', flat=True))
    interet_total = format(sum(remboursement_info.values_list('interet_remb', flat=True)),'.2f')
    penalite_total = sum(remboursement_info.values_list('penalite', flat=True)) + penalite_total_cot
    return render(request, "hod_template/Lesinterets_ajoutes.html", { "remboursement_info":remboursement_info, "interet_total":interet_total, "penalite_total":penalite_total})
    
def edit_membre(request, membre_id):
    request.session['membre_id']=membre_id
    #password = request.POST.get("password")
    membre_info=Membre.objects.get(admin=membre_id)
    
    form=EditMembreForm()
    form.fields['password'].initial=membre_info.admin.first_name
    form.fields['prenomp'].initial=membre_info.admin.first_name
    form.fields['nomp'].initial=membre_info.admin.last_name
    form.fields['codep'].initial=membre_info.codep
    form.fields['sexep'].initial=membre_info.sexep

    #form.fields['datenaissancep'].initial=membre_info.datenaissancep
    form.fields['lieunaissancep'].initial=membre_info.lieunaissancep
    form.fields['adressep'].initial=membre_info.adressep
    form.fields['villep'].initial=membre_info.villep
    form.fields['communep'].initial=membre_info.communep
    form.fields['departementp'].initial=membre_info.departementp
    form.fields['paysp'].initial=membre_info.paysp

    form.fields['nifp'].initial=membre_info.nifp
    form.fields['telephone1p'].initial=membre_info.telephone1p
    form.fields['telephone2p'].initial=membre_info.telephone2p
    form.fields['activiteprofessionp'].initial=membre_info.activiteprofessionp
    form.fields['referencep'].initial=membre_info.referencep
    form.fields['membre_actif'].initial=membre_info.membre_actif
    
    return render(request, "hod_template/edit_membre_template.html",{"form":form,"membre_info":membre_info, "id":membre_id})

def edit_membre_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed </h2>")
    else:
        membre_id = request.session.get("membre_id")
        if membre_id == None:
            return HttpResponseRedirect(reverse("manage_membre"))

        form = EditMembreForm(request.POST, request.FILES)
        if form.is_valid():
            # email=form.cleaned_data["email"]
            prenomp=form.cleaned_data["prenomp"]
            password=form.cleaned_data["password"]
            nomp=form.cleaned_data["nomp"]
            codep=form.cleaned_data["codep"]
            # email=form.cleaned_data["email"]
            # password=form.cleaned_data["password"]
            adressep=form.cleaned_data["adressep"]
            sexep = form.cleaned_data["sexep"]
            membre_actif = form.cleaned_data["membre_actif"]
            #datenaissancep=form.cleaned_data["datenaissancep"]
            villep=form.cleaned_data["villep"]
            communep=form.cleaned_data["communep"]
            departementp=form.cleaned_data["departementp"]
            paysp=form.cleaned_data["paysp"]
            nifp = form.cleaned_data["nifp"]

            telephone1p=form.cleaned_data["telephone1p"]
            telephone2p=form.cleaned_data["telephone2p"]
            activiteprofessionp=form.cleaned_data["activiteprofessionp"]
            referencep=form.cleaned_data["referencep"]

            if request.FILES.get('profile_pic', False):
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename=fs.save(profile_pic.name, profile_pic)
                profile_pic_url=fs.url(filename)
                #profile_pic_url = request.FILES['profile_pic']
            else:
                profile_pic_url = None

            try:
                user=CustomUser.objects.get(id=membre_id)
                user.first_name = prenomp
                user.last_name = nomp
                if password != None and password !="":
                    user.set_password(password)
                user.save()

                membre=Membre.objects.get(admin=membre_id)
                membre.adressep=adressep
                membre.sexep = sexep
                membre.codep=codep
                membre.nomp = nomp
                membre.prenomp=prenomp
                #membre.datenaissancep = datenaissancep
                membre.villep=villep
                membre.communep = communep

                membre.departementp=departementp
                membre.paysp = paysp
                membre.nifp=nifp
                membre.telephone1p = telephone1p
                membre.telephone2p=telephone2p
                membre.activiteprofessionp = activiteprofessionp
                membre.referencep = referencep
                membre.profile_pic=profile_pic_url  
                if profile_pic_url != None:
                    membre.profile_pic=profile_pic_url
                membre.membre_actif = membre_actif
                membre.save()
                del request.session['membre_id']
                messages.success(request,"Successfully Edited membre")
                return HttpResponseRedirect(reverse("edit_membre", kwargs={"membre_id":membre_id})) 
            except Exception as e:
                messages.error(request,traceback.format_exc())
                return HttpResponseRedirect(reverse("edit_membre", kwargs={"membre_id":membre_id}))
        else:
            form=EditMembreForm(request.POST)
            membre = Membre.objects.get(admin=membre_id)
            return render(request, "hod_template/edit_membre_template.html", {"form":form, "id":membre_id, "username":membre.admin.username})
           
def edit_cotisation(request, cotisation_id):
    membre_info = Membre.objects.all()
    cotisation = tbcotisation.objects.get(id=cotisation_id)
    membres = CustomUser.objects.filter(user_type=2)
    return render(request, "hod_template/edit_cotisation_template.html", {"cotisation":cotisation, "membres":membres,"membre_info":membre_info})

def edit_cotisation_save(request):
    if request.method !="POST":
        return HttpResponse("<h2> Methode Not Allowed </h2>")
    else:
        cotisation_id = request.POST.get("cotisation_id")
        code_membres = request.POST.get("membre")
        montant_recu = request.POST.get("montant_edit_cot")
        interet_recu = request.POST.get("interet_")
        penalite_recu = request.POST.get("penalite_")
        type_cotisation_recu = request.POST.get("type_cotisation")
        balance_recu = request.POST.get("balance")
        date_fait = request.POST.get("date_fait")
       

        try:
            cotisation=tbcotisation.objects.get(id=cotisation_id)
            cotisation.typecotisation=type_cotisation_recu
            cotisation.code_membre_id = code_membres
            cotisation.montant = montant_recu
            cotisation.interet = interet_recu
            cotisation.penalite = penalite_recu
            cotisation.balance = balance_recu
            cotisation.date_fait = date_fait
            cotisation.recu_par = request.user.username
            cotisation.save()

            messages.success(request,"Successfully Edited Cotisation")
            return HttpResponseRedirect(reverse("edit_cotisation",kwargs={"cotisation_id":cotisation_id}))
        except:
            messages.error(request,traceback.format_exc())
            return HttpResponseRedirect(reverse("edit_cotisation",kwargs={"cotisation_id":cotisation_id}))

def edit_credit(request, credit_id):
    membre_info = Membre.objects.all()
    credits = tbcredit.objects.get(numero=credit_id)
    membres = CustomUser.objects.filter(user_type=2)
    return render(request, "hod_template/edit_credit_template.html", {"credits":credits, "membres":membres,"membre_info":membre_info})

def edit_credit_save(request):

    if request.method !="POST":
        return HttpResponse("<h2> Methode Not Allowed </h2>")
    else:
        credit_id = request.POST.get("numero_credit")
        code_membres = request.POST.get("membre")
        nbre_de_mois = request.POST.get("nbre_de_mois")
        montant_recu = request.POST.get("montant_credit")
        interet_recu = request.POST.get("interet_credit")
        date_credit = request.POST.get("date_credit")
        date_debut = request.POST.get("date_debut")
        date_fin = request.POST.get("date_fin")
        commentaire = request.POST.get("commentaire")
        valider_par = request.POST.get("valider_par")
        status = request.POST.get("credit_status")
        

        try:
            credit=tbcredit.objects.get(numero=credit_id)
            credit.date_credit=date_credit
            credit.nbre_de_mois = nbre_de_mois
            credit.date_debut = date_debut
            credit.date_fin = date_fin
            credit.montant_credit = montant_recu
            credit.interet_credit = interet_recu
            credit.code_membre_id = code_membres
            credit.commentaire = commentaire
            credit.valider_par = valider_par
            credit.credit_status = status
            credit.save()

            messages.success(request,"Successfully Edited Credit")
            return HttpResponseRedirect(reverse("edit_credit",kwargs={"credit_id":credit_id}))
        except:
            messages.error(request,traceback.format_exc())
            return HttpResponseRedirect(reverse("edit_credit",kwargs={"credit_id":credit_id}))

def edit_remboursement(request, remboursement_id):
    
    codec=request.POST.get("numero_credit")
    info_re=tbcredit.objects.filter(numero=codec)

    membre_info = Membre.objects.all()
    remboursements = tbremboursement.objects.get(id=remboursement_id)
    membres = CustomUser.objects.filter(user_type=2)
    return render(request, "hod_template/edit_remboursement_template.html", {"remboursements":remboursements, "membres":membres,"membre_info":membre_info, "info_re":info_re})

def edit_remboursement_save(request):
    if request.method !="POST":
        return HttpResponse("<h2> Methode Not Allowed </h2>")
    else:
        remboursement_id = request.POST.get("remboursement_id")
        code_membres = request.POST.get("membre")
        montant_recu = request.POST.get("montant_a_rembourser")
        interet_recu = request.POST.get("interet_a_rembourser")
        capital_recu = request.POST.get("capital_a_rembourser")
        date_remb = request.POST.get("date_remboursement")
        balance = request.POST.get("balance_remb")
        penalite = request.POST.get("penalite_remb")
        commentaire = request.POST.get("commentaire")
        recu_par = request.POST.get("recu_par")
        code_credit = request.POST.get("numero_credit")
        

        try:
            remboursement=tbremboursement.objects.get(id=remboursement_id)
            remboursement.date_remb=date_remb
            remboursement.codecredit.id = code_credit
            remboursement.montant_a_remb = montant_recu
            remboursement.capital_remb = capital_recu
            remboursement.interet_remb = interet_recu
            remboursement.balance = balance
            remboursement.penalite = penalite
            remboursement.commentaire = commentaire
            remboursement.faites_par_id = code_membres
            remboursement.recu_par = recu_par
            remboursement.save()

            messages.success(request,"Successfully Edited Remboursement")
            return HttpResponseRedirect(reverse("edit_remboursement",kwargs={"remboursement_id":remboursement_id}))
        except:
            messages.error(request,traceback.format_exc())
            return HttpResponseRedirect(reverse("edit_remboursement",kwargs={"remboursement_id":remboursement_id}))

def edit_detailproduct(request, detailproduct_id):
    
    codec=request.POST.get("numero_credit")
    info_re=tbcredit.objects.filter(numero=codec)
    detailsproduits = tbdetailproduit.objects.get(no=detailproduct_id)
    
    return render(request, "hod_template/edit_detailproduit_template.html", {"detailsproduits":detailsproduits,  "info_re":info_re})

def edit_detailproduct_save(request):
    if request.method !="POST":
        return HttpResponse("<h2> Methode Not Allowed </h2>")
    else:
        code_credit = request.POST.get("numero_credit")
        detailproduct_id = request.POST.get("code_detailp")
        prix_unitaire = request.POST.get("prix_unitaire")
        quantite_product = request.POST.get("quantite_prod")
        prix_de_revient = request.POST.get("prix_revient")
        prix_de_vente = request.POST.get("prix_vente")
        prix_total = request.POST.get("prix_total")
        frais_transport = request.POST.get("frais_transport")
        description = request.POST.get("description")
    
        try:
            detailproduct=tbdetailproduit.objects.get(no=detailproduct_id)
            detailproduct.description=description
            detailproduct.codecredit.id = code_credit
            detailproduct.quantite_prod = quantite_product
            detailproduct.prix_unitaire = prix_unitaire
            detailproduct.prix_total = prix_total
            detailproduct.frais_transport = frais_transport
            detailproduct.prix_de_revient = prix_de_revient
            detailproduct.prix_de_vente = prix_de_vente
            
            detailproduct.save()

            messages.success(request,"Successfully Edited Remboursement")
            return HttpResponseRedirect(reverse("edit_detailproduit",kwargs={"detailproduct_id":detailproduct_id}))
        except:
            messages.error(request,traceback.format_exc())
            return HttpResponseRedirect(reverse("edit_detailproduit",kwargs={"detailproduct_id":detailproduct_id}))

def edit_depense(request, depense_id):
    depenses = tbdepense.objects.get(id=depense_id)
    return render(request, "hod_template/edit_depense_template.html", {"depenses":depenses})



def edit_depense_save(request):

    if request.method !="POST":
        return HttpResponse("<h2> Methode Not Allowed </h2>")
    else:
        depense_id = request.POST.get("depense_id")
        date_depense = request.POST.get("date_depense")
        description = request.POST.get("description")
        depense_unit = request.POST.get("depense_unit")
        quantite_dep = request.POST.get("quantite_dep")
        
        try:
            depense=tbdepense.objects.get(id=depense_id)
            depense.date_depense=date_depense
            depense.description = description
            depense.depense_unit = depense_unit
            depense.quantite_dep = quantite_dep
            depense.save()

            messages.success(request,"Successfully Edited Depense")
            return HttpResponseRedirect(reverse("edit_depense",kwargs={"depense_id":depense_id}))
        except:
            messages.error(request,traceback.format_exc())
            return HttpResponseRedirect(reverse("edit_depense",kwargs={"depense_id":depense_id}))

def edit_muso(request):
    current_user = request.user
    muso_id = current_user.muso_id
    muso = tbmuso.objects.get(id=muso_id)
    return render(request, "hod_template/edit_muso.html", {"muso": muso})

def edit_muso_save(request):
    current_user = request.user
    muso_id = current_user.muso_id

    if request.method!="POST":
        return HttpResponseRedirect(reverse("edit_muso"))
    else:
        #code_muso = request.POST.get("depense_id")
        sigle = request.POST.get("sigle")
        nom_muso = request.POST.get("nom_muso")
        adresse_muso = request.POST.get("adresse_muso")
        telephone_muso = request.POST.get("telephone_muso")
        site_muso = request.POST.get("site_muso")
        email_muso = request.POST.get("email_muso")
        date_creation_muso = request.POST.get("date_creation")
        couleur_menu = request.POST.get("colorSelect")
        taux_interet_credit = request.POST.get("taux_interet")
        couleur_text_menu = request.POST.get("colorSelecttext")
        try:
            muso = tbmuso.objects.get(id=muso_id)
            muso.sigle = sigle
            muso.nom_muso = nom_muso
            muso.adresse_muso = adresse_muso
            muso.telephone_muso = telephone_muso
            muso.taux_interet = taux_interet_credit
            muso.site_muso = site_muso
            muso.email_muso = email_muso
            muso.date_creation = date_creation_muso
            
            # Vérifier si une couleur est sélectionnée, sinon conserver la couleur précédente
            if couleur_menu:
                muso.couleur_preferee = couleur_menu

            # Vérifier si une couleur de texte est sélectionnée, sinon conserver la couleur précédente
            if couleur_text_menu:
                muso.couleur_text_menu = couleur_text_menu

            muso.save()

            messages.success(request, "MUSO Successfully Updated")
            return HttpResponseRedirect(reverse("edit_muso"))
        except:
            messages.error(request, "Failed to Update MUSO")
            return HttpResponseRedirect(reverse("edit_muso"))

def manage_session(request):
    return render(request, "hod_template/manage_session_template.html")

@csrf_exempt
def check_email_exist(request):
    email=request.POST.get("email")
    user_obj=CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

@csrf_exempt
def check_codep_exist(request):
    codep=request.POST.get("codep")
    user_obj=Membre.objects.filter(codep=codep).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

@csrf_exempt
def check_codeCredit(request):
    codec=request.POST.get("numero_credit")
    user_obj=tbcredit.objects.filter(numero=codec)
    if user_obj:
        return HttpResponse(True)
        capital = user_obj.montant_credit / user_obj.nbre_de_mois
        interet = user_obj.montant_credit * 0.1
        montant_ = capital + interet
    else:
        return HttpResponse(False)

def membre_feedback_message(request):
    current_user = request.user
    muso_id = current_user.muso_id
    feedbacks=FeedBackMembre.objects.filter(code_membre__admin__muso = muso_id)
    return render(request, "hod_template/membre_feedback_template.html", {"feedbacks":feedbacks})

@csrf_exempt
def membre_feedback_message_replied(request):
    current_user = request.user
    muso_id = current_user.muso_id
    feedback_id=request.POST.get("id")
    feedback_message=request.POST.get("message")
    try:
        feedback=FeedBackMembre.objects.get(id=feedback_id, code_membre__admin_muso = muso_id)
        feedback.feedback_reply=feedback_message
        feedback.save()
        return HttpResponse(True)
    except:
        return HttpResponse(False)

def membre_leave_view(request):
    current_user = request.user
    muso_id = current_user.muso_id
    leaves =LeaveReportMembre.objects.filter(code_membre__admin__muso = muso_id)
    return render(request, "hod_template/membre_leave_view.html",{"leaves":leaves})

def membre_approve_leave(request, leave_id):
    current_user = request.user
    muso_id = current_user.muso_id
    leave=LeaveReportMembre.objects.get(id=leave_id)
    leave.leave_status=1
    leave.save()
    return HttpResponseRedirect(reverse("membre_leave_view"))

def membre_disapprove_leave(request, leave_id):
    current_user = request.user
    muso_id = current_user.muso_id
    #return HttpResponse("ID : "+leave_id)
    leave=LeaveReportMembre.objects.get(id=leave_id)
    leave.leave_status=2
    leave.save()
    return HttpResponseRedirect(reverse("membre_leave_view"))

def comiteSMS_feedback(request):
    feedback_data=FeedBackMembre.objects.all()
    return render(request, "hod_template/comiteSMS_feedback.html",{"membre_data":feedback_data})

def comiteSMS_feedback_save(request):
    current_user = request.user
    muso_id = current_user.muso
 
    if request.method !="POST":
        return HttpResponse("Method Not Allowed")
    else:
        #date_depense = request.POST.get("date_depense")
        feedback_msg=request.POST.get("feedback_msg")

        try:
            ####################################
            feedback=FeedBackMembre(code_membre=request.user.id, feedback=feedback_msg, feedback_reply="")
            feedback.save()
            messages.success(request,"Successfully Message Sended")
            return HttpResponseRedirect(reverse("comiteSMS_feedback")) 
        except Exception as e:
            messages.error(request,traceback.format_exc())
            return HttpResponseRedirect(reverse("comiteSMS_feedback"))
    
def admin_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    #membre_infocon = Membre.object.get(id=1)
    #membre_info=Membre.objects.get(admin=request.user.id)
    return render(request,"hod_template/admin_profile.html",{"user":user})

def admin_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("admin_profile"))
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")
       
    try:
        customuser=CustomUser.objects.get(id=request.user.id)
        customuser.first_name=first_name
        customuser.last_name=last_name
        if password != None and password !="":
            customuser.set_password(password)
        customuser.save()
        messages.success(request,"Successfully Update Profile")
        return HttpResponseRedirect(reverse("admin_profile"))
    except:
        messages.success(request,"Failed Update Profile")
        return HttpResponseRedirect(reverse("admin_profile"))

def import_datadepensee_csv(request):
    if request.method == 'POST':
        file = request.FILES['file']

        # Check if the uploaded file is a CSV file
        if not file.name.endswith('.csv'):
            messages.error(request, 'This is not a CSV file')
            return render(request, 'manage_depense_template.html')

        # Read the CSV file
        data = csv.reader(file.read().decode('utf-8').splitlines())

        # Loop through the rows in the CSV file and insert them into the database
        for row in data:
            tbdepense.objects.create(date_depense=row[0], description=row[1], depense_unit=row[2], quantite_dep=row[2])

        messages.success(request, 'Data imported successfully')
        return render(request, 'manage_depense_template.html')

    return render(request, 'manage_depense_template.html')

def import_datadepenses_csv(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        try:
            # Read the Excel file using Pandas
            df = pd.read_excel(excel_file)

            # Iterate over each row and create a MyModel object for each row
            for index, row in df.iterrows():
                obj = tbdepense(
                    #field1=row['Column1'],
                    #field2=row['Column2'],
                    date_depense=row[0],
                    description=row[1],
                    depense_unit=row[2],
                    quantite_dep=row[3]
                    # Add more fields here as necessary
                )
                obj.full_clean()  # Validate the object
                obj.save()  # Save the object to the database

            return render(request, 'manage_depense_template.html', {'message': 'Excel data imported successfully.'})

        except Exception as e:
            # Handle any exceptions that may occur during the import process
            return render(request, 'manage_depense_template.html', {'message': f'Error importing Excel data: {e}'})

    return render(request, 'manage_depense_template.html')

def import_data(request):
  if request.method == 'POST':
    file = request.FILES['file']
    print(f'File uploaded: {file}')

# importer les donnees
def import_datadepensees_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']

        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'This is not a CSV file')
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)

        for column in csv.reader(io_string, delimiter=',', quotechar='"'):
            _, created = tbdepense.objects.update_or_create(
                date_depense=column[0],
                description=column[1],
                depense_unit=column[2],
                quantite_dep=column[3]
            )

        return render(request, 'import.html')

    return render(request, 'import.html')

def import_datadepenseers_csv(request):
    if request.method == 'POST':
        file = request.FILES['csv_file']

        # Check if the uploaded file is a CSV file
        if not file.name.endswith('.xlsx'):
            messages.error(request, 'This is not a CSV file')
            return render(request, 'hod_template/manage_depense_template.html')

        # Read the CSV file with the correct encoding
        data = csv.reader(file.read().decode('latin1').splitlines())

        # Loop through the rows in the CSV file and insert them into the database
        for row in data:
            tbdepense.objects.create(date_depense=row[0], description=row[1], depense_unit=row[2], quantite_dep=row[2])

        messages.success(request, 'Data imported successfully')
        return render(request, 'hod_template/manage_depense_template.html')

    return render(request, 'hod_template/manage_depense_template.html')

def import_datadepensesss_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']

        # Check if the uploaded file is a CSV file
        if not csv_file.name.endswith('.xlsx'):
            messages.error(request, 'This is not a CSV file')
            return render(request, 'hod_template/manage_depense_template.html')

        # Read the CSV file and remove any null characters
        file_data = csv_file.read().decode('utf-8').replace('\0', '')

        # Create a CSV reader and skip the header row
        data = csv.reader(file_data.splitlines())
        next(data)

        # Loop through the rows in the CSV file and insert them into the database
        for row in data:
            tbdepense.objects.create(date_depense=row[0], description=row[1], depense_unit=row[2], quantite_dep=row[2])

        messages.success(request, 'Data imported successfully')
        return render(request, 'hod_template/manage_depense_template.html')

    return render(request, 'hod_template/manage_depense_template.html')

def import_datadepense_csvs(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        # Vérifiez que le fichier est bien un fichier Excel
        if not csv_file.name.endswith('.xlsx'):
            messages.error(request, 'Le fichier doit être au format Excel')
            return render(request, 'hod_template/manage_depense_template.html')
        # Ouvrez le fichier Excel
        workbook = xlrd.open_workbook(file_contents=csv_file.read())
        worksheet = workbook.sheet_by_index(0)
        # Parcourez les lignes du fichier Excel et créez des objets MyModel
        for row_num in range(1, worksheet.nrows):
            row = worksheet.row_values(row_num)
            obj = tbdepense()
            obj.date_depense=datetime.datetime(*xlrd.xldate_as_tuple(row[0], workbook.datemode)),
            obj.description=row[1],
            obj.depense_unit=row[2],
            obj.quantite_dep=row[3]
            # Ajuster les autres champs en fonction des colonnes du fichier Excel
            obj.save()
        messages.success(request, 'Les données ont été importées avec succès')
        return render(request, 'hod_template/manage_depense_template.html')
    else:
        return render(request, 'hod_template/manage_depense_template.html')
    
def import_datadepense_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']

        # Check if the uploaded file is an Excel file
        if not csv_file.name.endswith('.xlsx'):
            messages.error(request, 'This is not an Excel file')
            return render(request, 'hod_template/manage_depense_template.html')

        # Load the Excel file using openpyxl
        wb = openpyxl.load_workbook(csv_file)
        sheet = wb.active

        # Loop through the rows in the Excel file and insert them into the database
        for row in sheet.iter_rows(min_row=2, values_only=True):
            tbdepense.objects.create(date_depense=row[0], description=row[1], depense_unit=row[2], quantite_dep=row[2])

        messages.success(request, 'Data imported successfully')
        return render(request, 'hod_template/manage_depense_template.html')

    return render(request, 'hod_template/manage_depense_template.html')

    #----------------------- exporter fichier excel --------------------------------------
    # export tous les users       

# Exportation sur EXCEL----------------------------------------------------------------------------------
def export_membres_csv(request):
    current_user = request.user
    muso_id = current_user.muso_id
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Liste_membre.csv"'

    writer = csv.writer(response)
    writer.writerow(['Id','codep', 'nomp', 'prenomp', 'sexep', 'lieunaissance', 'adressep', 'activiteprofessionp','referencep', 'Date Ajout',  'Admin_id', 'membre_actif']) # Add column headers

    my_data = Membre.objects.filter(admin__muso=current_user.muso)
    for item in my_data:
        writer.writerow([item.id, item.codep, item.nomp,item.prenomp, item.sexep, item.lieunaissancep, item.adressep, item.activiteprofessionp, item.referencep,item.dateajout, item.admin_id,  item.membre_actif]) # Add data rows
    return response

def export_cotisation_csv(request):
    current_user = request.user
    muso_id = current_user.muso_id
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Liste_cotisation.csv"'

    writer = csv.writer(response)
    writer.writerow(['Id','typecotisation', 'montant', 'interet', 'balance', 'date_fait', 'code_membre', 'penalite','recu_par']) # Add column headers
    my_data = tbcotisation.objects.filter(code_membre_id__admin__muso=current_user.muso)
    for item in my_data:
        writer.writerow([item.id, item.typecotisation, item.montant,item.interet, item.balance, item.date_fait, item.code_membre_id, item.penalite, item.recu_par]) # Add data rows
    return response

def export_credit_csv(request):
    current_user = request.user
    muso_id = current_user.muso_id
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Liste_credit.csv"'

    writer = csv.writer(response)
    #credit=tbcredit(numero=numero_credit, date_credit=date_credit, nbre_de_mois=nbre_de_mois,date_debut=date_debut, date_fin=date_fin, montant_credit=float(montant_recu), interet_credit=float(interet_recu), code_membre=code_membre, commentaire=commentaire, valider_par=valider_par)
    writer.writerow(['numero','date_credit', 'nbre_de_mois', 'date_debut', 'date_fin', 'montant_credit', 'interet_credit', 'code_membre','commentaire','valider_par']) # Add column headers
    my_data = tbcredit.objects.filter(code_membre_id__admin__muso=current_user.muso)
    for item in my_data:
        writer.writerow([item.numero, item.date_credit, item.nbre_de_mois,item.date_debut, item.date_fin, item.montant_credit, item.interet_credit, item.code_membre, item.commentaire, item.valider_par]) # Add data rows
    return response

def export_remboursement_csv(request):
    current_user = request.user
    muso_id = current_user.muso_id
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Liste_remboursement.csv"'

    writer = csv.writer(response)
    #remboursement=tbremboursement(date_remb=date_remboursement,  montant_a_remb=float(montant_recu),capital_remb=float(capital_recu), interet_remb=float(interet_recu), balance=float(balance_recu), penalite=float(penalite_recu), commentaire=commentaire, recu_par=valider_par, codecredit=code_credit, faites_par=code_membre)
    writer.writerow(['ID','date_remb', 'montant_a_remb', 'capital_remb', 'interet_remb', 'balance', 'penalite','commentaire', 'recu_par','codecredit_id', 'faites_par_id']) # Add column headers
    my_data = tbremboursement.objects.filter(faites_par_id__admin__muso=current_user.muso)
    for item in my_data:
        writer.writerow([item.id, item.date_remb, item.montant_a_remb,item.capital_remb, item.interet_remb, item.balance, item.penalite,item.commentaire, item.recu_par, item.codecredit_id, item.faites_par_id]) # Add data rows
    return response

def export_detailcredit_csv(request):
    current_user = request.user
    muso_id = current_user.muso_id
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Liste_detail_credit.csv"'

    writer = csv.writer(response)
    #remboursement=tbremboursement(date_remb=date_remboursement,  montant_a_remb=float(montant_recu),capital_remb=float(capital_recu), interet_remb=float(interet_recu), balance=float(balance_recu), penalite=float(penalite_recu), commentaire=commentaire, recu_par=valider_par, codecredit=code_credit, faites_par=code_membre)
    writer.writerow(['codecredit','date_pret', 'montant_pret', 'montant_capital', 'montant_interet', 'total_montant', 'total_montant_rest']) # Add column headers
    my_data = tbdetailcredit.objects.filter(Q(codecredit_id__in=tbcredit.objects.filter( code_membre_id__in=Membre.objects.filter(admin_id__in=CustomUser.objects.filter(muso_id=muso_id))).values('numero')))
    for item in my_data:
        writer.writerow([item.codecredit_id, item.date_pret, item.montant_pret,item.montant_capital, item.montant_interet, item.total_montant_jr, item.total_montant_rest]) # Add data rows
    return response

def export_depense_csv(request):
    current_user = request.user
    muso_id = current_user.muso_id
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Liste_depense.csv"'

    writer = csv.writer(response)
    # depense=tbdepense(date_depense=date_depense,  description=description, depense_unit=float(depense_unit), quantite_dep=float(quantite_dep), muso_id=muso_id)
    writer.writerow(['ID','date_depense', 'description', 'depense_unit', 'quantite_dep']) # Add column headers
    my_data = tbdepense.objects.filter(muso_id=current_user.muso)
    for item in my_data:
        writer.writerow([item.id, item.date_depense, item.description,item.depense_unit, item.quantite_dep]) # Add data rows
    return response

def export_detailalimentaire_csv(request):
    current_user = request.user
    muso_id = current_user.muso_id
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Liste_detailAlimentaire.csv"'

    writer = csv.writer(response)
    #detailproduct=tbdetailproduit(codecredit=code_credit,  description=description, quantite_prod=float(quantite), prix_unitaire=float(prix_unitaire), prix_total=float(prix_total), frais_transport=float(frais_transport), prix_de_revient=float(prix_revient), prix_de_vente=float(prix_vente))
    writer.writerow(['No','codecredit', 'description', 'quantite_prod', 'prix_unitaire', 'prix_total', 'frais_transport', 'prix_de_revient','prix_de_vente']) # Add column headers
    my_data = tbdetailproduit.objects.filter(codecredit_id__code_membre_id__admin__muso=current_user.muso)
    for item in my_data:
        writer.writerow([item.no, item.codecredit, item.description,item.quantite_prod, item.prix_unitaire, item.prix_total, item.frais_transport, item.prix_de_revient, item.prix_de_vente]) # Add data rows
    return response

def export_statistique_remboursement_csv(request):
    current_user = request.user
    muso_id = str(current_user.muso_id)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="statistique_remboursement.csv"'

    writer = csv.writer(response)
    # depense=tbdepense(date_depense=date_depense,  description=description, depense_unit=float(depense_unit), quantite_dep=float(quantite_dep), muso_id=muso_id)
    
    writer.writerow(['ID','qte_rembourser', 'qte_restant', 'montant_rambourser', 'montant_restant', 'total_interet', 'Interet_restant', 'total_penalite']) # Add column headers
    #my_data = tbdepense.objects.filter(muso_id=current_user.muso)
    query = """
        SELECT 
    codecredit_id,
    COUNT(g_muso_app_tbremboursement.id) AS quantite_remboursement,
	(g_muso_app_tbcredit.nbre_de_mois- COUNT(g_muso_app_tbremboursement.id)) as Qtee_restant,
    SUM(capital_remb) + SUM(interet_remb) AS montant_total_rembourse,
	(((capital_remb+interet_remb)*nbre_de_mois) - (SUM(capital_remb) + SUM(interet_remb))) AS montant_total_Restant,
    SUM(interet_remb) AS total_interet,
	(interet_remb*nbre_de_mois) - SUM(interet_remb) AS total_interet_restant,
    SUM(penalite) AS total_penalite
    FROM
        g_muso_app_tbremboursement,g_muso_app_membre ,g_muso_app_customuser, g_muso_app_tbcredit
    WHERE
        g_muso_app_tbremboursement.faites_par_id = g_muso_app_membre.id and g_muso_app_membre.admin_id = g_muso_app_customuser.id and g_muso_app_tbremboursement.codecredit_id = g_muso_app_tbcredit.numero and g_muso_app_customuser.muso_id = %s
    GROUP BY
        codecredit_id
    ORDER BY
        codecredit_id ASC
    """
    with connection.cursor() as cursor:
        cursor.execute(query, [muso_id])
        my_data = cursor.fetchall()

    for item in my_data:
        writer.writerow([item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7]]) # Add data rows
            #writer.writerow([item.codecredit_id, item.quantite_remboursement, item.Qtee_restant, item.montant_total_rembourse, item.montant_total_Restant, item.total_interet, item.total_interet_restant, item.total_penalite]) # Add data rows
    return response



def export_statistique_credit_csv(request):
    current_user = request.user
    muso_id = current_user.muso_id

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="statistique_remboursement.csv"'

    writer = csv.writer(response)

    writer.writerow(['numero', 'Montant_Credit', 'Montant_rembourser', 'Montant_interet', 'Date_credit'])  # Add column headers

    subquery = tbremboursement.objects.filter(codecredit_id=OuterRef('numero')).values('codecredit_id')
    credit_info = tbcredit.objects.annotate(
        montant_rembourser=ExpressionWrapper(
            (F('montant_credit') * F('interet_credit') * F('nbre_de_mois')) + F('montant_credit'),
            output_field=FloatField()
        ),
        interet_total_credit=ExpressionWrapper(
            ((F('montant_credit') * F('interet_credit') * F('nbre_de_mois')) + F('montant_credit')) - F('montant_credit'),
            output_field=FloatField()
        ),
    ).filter(
        code_membre__id=F('code_membre_id'),
        code_membre__admin__id=F('code_membre__admin__id'),
        code_membre__admin__muso_id=muso_id,
        pk__in=Subquery(subquery)
    ).values(
        'numero',
        'montant_credit',
        'date_debut',
        'montant_rembourser',
        'interet_total_credit'
    ).order_by('date_debut')

    for item in credit_info:
        montant_credit = format(item['montant_credit'], ".2f")  # Format the value with 2 decimal places
        montant_rembourser = format(item['montant_rembourser'], ".2f")  # Format the value with 2 decimal places
        interet_total_credit = format(item['interet_total_credit'], ".2f")  # Format the value with 2 decimal places
        writer.writerow([
            item['numero'],
            montant_credit,
            montant_rembourser,
            interet_total_credit,
            item['date_debut']
        ])
        
    return response

'''def export_statistique_credit_csv(request):
    current_user = request.user
    muso_id = current_user.muso_id

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="statistique_remboursement.csv"'

    writer = csv.writer(response)
   
    writer.writerow(['numero','Montant_Credit','Montant_rembourser', 'Montant_interet',  'Date_credit']) # Add column headers
    
    subquery = tbremboursement.objects.filter(codecredit_id=OuterRef('numero')).values('codecredit_id')
    credit_info = tbcredit.objects.annotate(
        montant_rembourser=ExpressionWrapper(
            (F('montant_credit') * F('interet_credit') * F('nbre_de_mois')) + F('montant_credit'),
            output_field=FloatField()
        ),
        interet_total_credit=ExpressionWrapper(
            ((F('montant_credit') * F('interet_credit') * F('nbre_de_mois')) + F('montant_credit')) - F('montant_credit'),
            output_field=FloatField()
        ),
    ).filter(
        code_membre__id=F('code_membre_id'),
        code_membre__admin__id=F('code_membre__admin__id'),
        code_membre__admin__muso_id=muso_id,
        pk__in=Subquery(subquery)
    ).values(
        'numero',
        'montant_credit',
        'date_credit',
        'montant_rembourser',
        'interet_total_credit'
    ).order_by('date_debut')

    for item in credit_info:
        writer.writerow([item.numero, item.montant_credit, item.date_credit, item.montant_rembourser, item.interet_total_credit, item.date_debut])
        #writer.writerow([item[0], item[1], item[2], item[3], item[4], item[5]]) # Add data rows
            #writer.writerow([item.codecredit_id, item.quantite_remboursement, item.Qtee_restant, item.montant_total_rembourse, item.montant_total_Restant, item.total_interet, item.total_interet_restant, item.total_penalite]) # Add data rows
    return response'''

def dernier_samedi(date):
        while date.weekday() != 5:
            date = date + timedelta(days=1)

        while True:
            dernier_jour = date.replace(day=1) + timedelta(days=32)
            dernier_jour = dernier_jour - timedelta(days=dernier_jour.day)
            while dernier_jour.weekday() != 5:
                dernier_jour = dernier_jour - timedelta(days=1)

            if dernier_jour >= date:
                yield dernier_jour
            date = dernier_jour + timedelta(days=7)

def CalculateurPretView(request):
    current_user = request.user
    muso_id = current_user.muso_id
     
    code_pret = request.POST.get('code_pret')
    montant_pret = request.POST.get('montant_credit')
    
    nombre_mois = request.POST.get('nombre_mois')
    date_deb = request.POST.get('date_debut')
    if date_deb is not None:
        date_debut = datetime.strptime(date_deb, "%d/%m/%Y")
    else:
        date_debut = "27/05/2023"
    
    generateur_samedis = dernier_samedi(date_debut)
        # Vérifiez si l'intérêt est fixe ou variable
    if request.POST.get('choix_interet') == "Fixe":
        taux_interet = request.POST.get('taux_interet')
        montant_interet = float(montant_pret) * float(taux_interet) / 100
        montant_total = float(montant_pret) + float(montant_interet)
            
    else:
        montant_interet_ = 0.0
        montant_pret = 0.0
        #montant_interet_ = request.POST.get('montant_interet')
        montant_total = float(montant_pret) + float(montant_interet_)
    # Calculez les paiements mensuels
    montant_restant = float(montant_total)
       
    count = 0
    if nombre_mois is not None:
        while count < int(nombre_mois):
            # Trouver le dernier samedi du mois pour la date de début
            derniersam = next(generateur_samedis)
            capital = float(montant_pret) / float(nombre_mois)
            interet = float(montant_interet)
            total = capital + interet
            montant_restant -= capital
            count += 1

            # Insérez les données dans la table
            tbdetailcredit.objects.create(date_pret=derniersam, montant_pret=montant_pret, montant_capital=capital, montant_interet=interet, total_montant_jr=total, total_montant_rest=montant_restant,codecredit_id=code_pret)
    else: 
        nombre_mois = 1
    # Récupérez tous les paiements de la base de données
    #creditalimentaires = tbcredit.objects.filter(Q(numero__in=tbdetailproduit.objects.filter(codecredit_id__in=tbcredit.objects.values('numero')).values('codecredit_id')) &Q(code_membre_id__in=Membre.objects.filter(admin_id__in=CustomUser.objects.filter(muso_id=muso_id).values('id')).values('id'))).order_by('-date_credit')
    
    paiements = tbdetailcredit.objects.filter(Q(codecredit_id__in=tbcredit.objects.filter( code_membre_id__in=Membre.objects.filter(admin_id__in=CustomUser.objects.filter(muso_id=muso_id))).values('numero')))

    # Return the appropriate HttpResponse
    return render(request, "hod_template/frmcalculateur_credit.html", { "paiements":paiements })
    #return render(request, self.template_name, {'paiements': paiements})

def get_credit_data(request):
    code_credit = request.GET.get('code_credit')
    credit = tbcredit.objects.get(numero=code_credit)
    #format(number, ".2f")
    capital_credit = credit.montant_credit / credit.nbre_de_mois
    montant_interet = credit.interet_credit * credit.montant_credit
    montant_a_rembourser = capital_credit + montant_interet
    data = {
        'montant_credit': format(montant_a_rembourser,".2f"),
        'capital_credit':  format(capital_credit,".2f"),
        'interet_credit': format(montant_interet,".2f"),
    }
    return JsonResponse(data)

def get_credit_info(request):
    code_credit = request.GET.get('code_credit')
    credit = tbcredit.objects.get(numero=code_credit)

    montant_credit = credit.montant_credit
    taux_interet = credit.interet_credit *100
    date_debut = credit.date_debut
    duree = credit.nbre_de_mois
    data = {

        'montant_credit': montant_credit,
        'taux_interet': taux_interet,
        'date_debut': date_debut.strftime('%d/%m/%Y'),
        'duree': duree
    }
    return JsonResponse(data)

def add_comments_save(request):
    current_user = request.user
    muso_id = current_user.muso
    membres = Membre.objects.filter(admin_id=request.user.id).values('id')
    if membres.exists():
        code_membre = membres[0]['id']

    if request.method !="POST":
        return HttpResponse("Method Not Allowed")
    else:
        #current_user = request.user
        text_comment = request.POST.get("content")
        try:
            comment=Comment(text=text_comment, author_id=code_membre, muso_id=muso_id)
            comment.save()
            return HttpResponseRedirect(reverse("profile_view")) 
        except Exception as e:
            traceback.print_exc() 
            #messages.error(request.traceback.format_exc())
            return HttpResponseRedirect(reverse("profile_view"))
        
def profile_view(request):
    current_user = request.user
    muso_id = current_user.muso
    # Logic for the profile view
    comments = Comment.objects.filter(author_id=F('author_id__id'), muso_id_id=muso_id).order_by('-created_at').values('id', 'text', 'created_at', 'author_id__nomp', 'author_id__prenomp')
    #comments = Comment.objects.annotate(champ_concatene=ExpressionWrapper(F('author_id__nomp') + ' ' + F('author_id__prenomp'),output_field=CharField())).values('id', 'text', 'created_at', 'champ_concatene')
    #comments = Comment.objects.filter(muso_id=muso_id).order_by('-created_at')
    return render(request, 'hod_template/commentaire.html', {'comments': comments})


#@login_required
def user_info(request):
    # Récupérer l'ID de l'utilisateur connecté
    user_id = request.user.id
    
    # Récupérer le type d'utilisateur (par exemple, nom d'utilisateur ou email)
    user_type = request.user.username  # Vous pouvez utiliser d'autres attributs tels que 'email'
    
    # Récupérer l'ID du groupe de l'utilisateur
    group_id = request.user.groups.first().id if request.user.groups.exists() else None
    
    # Récupérer les permissions de l'utilisateur
    permissions = request.user.get_all_permissions()
    
    # Passer les valeurs récupérées au contexte de rendu
    context = {
        'user_id': user_id,
        'user_type': user_type,
        'group_id': group_id,
        'permissions': permissions
    }
    
    return render(request, 'hod_template/user_info.html', context)

#@login_required
def user_access(request):
    # Récupérer les accès de l'utilisateur connecté
    #user_permissions = request.user.user_permissions.all()
    user_permissions = Permission.objects.all()
    # Passer les accès au contexte de rendu
    context = {
        'user_permissions': user_permissions
    }
    
    return render(request, 'hod_template/user_access.html', context)

def user_groups(request):
    # Récupérer les groupes d'utilisateurs de l'utilisateur connecté
    #user_groups = request.user.groups.all()
    user_groups = AbstractBaseUser.objects.all()
    #
    # Passer les groupes d'utilisateurs au contexte de rendu
    context = {
        'user_groups': user_groups
    }
    return render(request, 'hod_template/user_groups.html', context)


#permissions = Permission.objects.all()

# Afficher les noms de colonnes
#for field in permissions.model._meta.fields:
    #print(field.name)

# Afficher tous les noms de modèle dans django.contrib.auth.models
'''for model_name in dir(auth_models):
    model = getattr(auth_models, model_name)
    if hasattr(model, '_meta') and model._meta.app_label == 'auth':
        print(model_name)'''

'''
result = tbcredit.objects.filter(
    numero__in=tbremboursement.objects.filter(interet_remb=0).values('codecredit_id')
).filter(
    code_membre__id__in=Membre.objects.filter(
        admin__id__in=CustomUser.objects.filter(muso_id=1).values('id')
    ).values('id')
).annotate(
    Interet_anticipe=Sum(F('montant_credit') * F('interet_credit'))
).values('Interet_anticipe')

print(result)

result1 = tbcredit.objects.filter(
    numero__in=tbremboursement.objects.filter(interet_remb=0).values('codecredit_id')
).filter(
    code_membre__admin__id__in=CustomUser.objects.filter(muso_id=1).values('id')
).aggregate(
    interet_anticipe_total=Sum(F('montant_credit') * F('interet_credit'))
)

print(result1['interet_anticipe_total'])

interet_anticipe = tbcredit.objects.filter(
    numero__in=tbremboursement.objects.filter(interet_remb=0, codecredit__isnull=False).values('codecredit'),
    code_membre__admin__muso=1
).aggregate(
    interet_anticipe=Sum('montant_credit') * Sum('interet_credit')
)

somme_interet_anticipe = interet_anticipe['interet_anticipe']

print(somme_interet_anticipe)'''