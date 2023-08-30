from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
import traceback
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from g_muso_app.models import CustomUser, Membre, tbcotisation, tbcredit,tbremboursement,FeedBackMembre,LeaveReportMembre,CustomUser, tbdepense, tbdetailproduit, tbdetailcredit, Comment, tbmuso, tbtypecotisation
from .forms import EditMembreForm
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.core.paginator import Paginator
from django.db.models import Sum, Count,  F
from django.db import connection
import csv
from django.db import transaction
from django.db.models import F
import io
import xlrd
import datetime , openpyxl

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
from django.shortcuts import render, get_object_or_404
import random
from django.utils import timezone
import sqlite3

def membre_home(request):
    has_permission = request.user.has_perm('g_muso_app.add_depense')
    current_user = request.user
    #muso_id = current_user.muso
    membre_count=Membre.objects.filter(membre_actif='True', admin__muso=current_user.muso).count()
    membre_obj=Membre.objects.get(admin_id=request.user.id)

    caisseverte = tbtypecotisation.objects.get(reference='cv', cotisation_muso=current_user.muso)
    caisserouge = tbtypecotisation.objects.get(reference='cr', cotisation_muso=current_user.muso)
    caissebleue = tbtypecotisation.objects.get(reference='cb', cotisation_muso=current_user.muso)

    if caisseverte and caissebleue :
        cotisation_FU=tbcotisation.objects.filter(code_membre_id=membre_obj, typecotisation=caissebleue.nom_cotisation, code_membre__admin__muso=current_user.muso,code_membre__membre_actif='True')
        cotisation_info=tbcotisation.objects.filter(code_membre_id=membre_obj, typecotisation=caisseverte.nom_cotisation, code_membre__admin__muso=current_user.muso,code_membre__membre_actif='True')
        montant_tot = format((sum(cotisation_info.values_list('montant', flat=True))+ sum(cotisation_info.values_list('interet', flat=True))+ sum(cotisation_FU.values_list('montant', flat=True))),'.2f') 
    else:
        montant_tot =0
        
    if caisseverte:
        _credit  =tbcotisation.objects.filter(code_membre_id=membre_obj, typecotisation=caisseverte.nom_cotisation,code_membre__admin__muso=current_user.muso)
        montant_ccredit = sum(_credit.values_list('montant', flat=True))
    else:
       montant_ccredit=0

    if caissebleue:
         _ijans  =tbcotisation.objects.filter(code_membre_id=membre_obj, typecotisation__icontains=caissebleue.nom_cotisation ,code_membre__admin__muso=current_user.muso)
         montant_ijans = sum(_ijans.values_list('montant', flat=True))
    else:
        montant_ijans =0

    if caisserouge:
         _fonctionnement  =tbcotisation.objects.filter(code_membre_id=membre_obj, typecotisation__icontains=caisserouge.nom_cotisation,code_membre__admin__muso=current_user.muso)
         montant_fonk = sum(_fonctionnement.values_list('montant', flat=True))
    else:
        montant_fonk =0

    valeur2 = tbremboursement.objects.filter(faites_par__admin__muso=current_user.muso).values('date_remb').order_by('date_remb').annotate(sum=Sum('interet_remb'))
 
    credit_info = tbcredit.objects.filter(credit_status__icontains="En cour", code_membre__admin__muso=current_user.muso)
    montant_credit = sum(credit_info.values_list('montant_credit', flat=True))
    #remb_info = tbremboursement.objects.all()
    remb_info = tbremboursement.objects.filter(faites_par__admin__muso=current_user.muso,codecredit_id__credit_status__icontains="En cour").values('codecredit_id').order_by('codecredit_id').annotate(capital_remb=Sum('capital_remb'))
    montant_rembourse = format(sum(remb_info.values_list('capital_remb', flat=True)),'.2f')
    
 
    montant_rembourse = format(sum(remb_info.values_list('capital_remb', flat=True)),'.2f')

     #modificatio apporter
    creditsmt = tbcredit.objects.filter(code_membre__admin_id__muso_id=current_user.muso)
    
    montant_total_credit = creditsmt.aggregate(Sum('montant_credit'))['montant_credit__sum']
    
    creditsit = creditsmt.annotate(
        interet_montant=F('montant_credit') * F('interet_credit') * F('nbre_de_mois')
    )
    
    interet_total = creditsit.aggregate(Sum('interet_montant'))['interet_montant__sum']
    
    #-----
    creditencour = tbcredit.objects.filter(code_membre__admin_id__muso_id=current_user.muso, credit_status='En cour')
    
    montant_total_credit_encour = creditencour.aggregate(Sum('montant_credit'))['montant_credit__sum']
    
    creditssencour = creditencour.annotate(
        interet_montant=F('montant_credit') * F('interet_credit') * F('nbre_de_mois')
    )
    
    interet_total_encour = creditssencour.aggregate(Sum('interet_montant'))['interet_montant__sum']

    #------------
    remboursements_info = tbremboursement.objects.filter(codecredit__code_membre__admin__muso_id=current_user.muso).aggregate(total_montant_remb=Sum('montant_a_remb'),total_interet_remb=Sum('interet_remb'))
   #-------------------
    db_path = "db.sqlite3"
    
    query = """
        SELECT 
    g_muso_app_tbcredit.numero AS codecredit_id,
    COUNT(g_muso_app_tbremboursement.id) AS quantite_remboursement,
    (g_muso_app_tbcredit.nbre_de_mois - COUNT(g_muso_app_tbremboursement.id)) AS Qtee_restant,
    IFNULL(SUM(g_muso_app_tbremboursement.capital_remb), 0) + IFNULL(SUM(g_muso_app_tbremboursement.interet_remb), 0) AS montant_total_rembourse,
    (((g_muso_app_tbcredit.nbre_de_mois * (g_muso_app_tbcredit.interet_credit * g_muso_app_tbcredit.montant_credit)) + g_muso_app_tbcredit.montant_credit) - (sum(IFNULL(g_muso_app_tbremboursement.capital_remb, 0) + (IFNULL(g_muso_app_tbremboursement.interet_remb, 0))))) AS montant_total_Restant,
    IFNULL(SUM(g_muso_app_tbremboursement.interet_remb), 0) AS total_interet,
    (g_muso_app_tbcredit.nbre_de_mois * (g_muso_app_tbcredit.interet_credit * g_muso_app_tbcredit.montant_credit)) + g_muso_app_tbcredit.montant_credit AS Montant_tot,
    (IFNULL(SUM(g_muso_app_tbremboursement.interet_remb), 0) * nbre_de_mois) - IFNULL(SUM(g_muso_app_tbremboursement.interet_remb), 0) AS total_interet_restant,
    g_muso_app_tbcredit.date_debut, g_muso_app_tbcredit.date_fin,
    g_muso_app_membre.profile_pic, g_muso_app_membre.prenomp, g_muso_app_membre.nomp,
    SUM(penalite) AS total_penalite, (g_muso_app_tbcredit.interet_credit * g_muso_app_tbcredit.montant_credit) AS interetCredit
    FROM
        g_muso_app_tbcredit 
    LEFT JOIN
        g_muso_app_tbremboursement  ON g_muso_app_tbcredit.numero = g_muso_app_tbremboursement.codecredit_id
    JOIN
        g_muso_app_Membre  ON g_muso_app_tbcredit.code_membre_id = g_muso_app_Membre.id
    JOIN
        g_muso_app_CustomUser  ON g_muso_app_Membre.admin_id = g_muso_app_CustomUser.id
    WHERE
        (g_muso_app_tbcredit.credit_status = 'En cour' OR g_muso_app_tbremboursement.id IS NULL)
        AND g_muso_app_CustomUser.muso_id = ?
        
    GROUP BY
        g_muso_app_tbcredit.numero, g_muso_app_tbcredit.nbre_de_mois, g_muso_app_tbcredit.interet_credit, g_muso_app_tbcredit.montant_credit,
        g_muso_app_tbcredit.date_debut, g_muso_app_tbcredit.date_fin,
        g_muso_app_Membre.profile_pic, g_muso_app_Membre.prenomp, g_muso_app_Membre.nomp
    ORDER BY
        codecredit_id ASC;
    """

    # Créez une connexion à la base de données
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    current_users = request.user
   
    # Exécutez la requête
    cursor.execute(query, (current_users.muso_id,))

    # Parcourez les résultats pour calculer la somme du montant_total_Restant
    montant_total_restant = 0
    Total_interet_restant = 0
    for row in cursor.fetchall():
        montant_total_restant += row[4]
        Total_interet_restant += row[7]

    #-------------interet anticipe------------
    interet_anticipe = tbcredit.objects.filter(
    tbremboursement__interet_remb=0,
    code_membre__admin__muso_id=current_user.muso
    ).aggregate(
    interet_anticipe=Sum(F('montant_credit') * F('interet_credit'))
    )['interet_anticipe']

    remboursement_info = tbremboursement.objects.filter(
    faites_par_id__admin_id__muso_id=current_user.muso
    ).values('date_remb').annotate(
        total_interet=Sum('interet_remb'),
        total_penalite=Sum('penalite'),
        montant_total_rembourse=Sum('montant_a_remb') + Sum('interet_remb'),
        quantite_remboursement=Count('id')
    ).order_by('date_remb')
    
    cotisation_info = tbcotisation.objects.filter(code_membre__admin_id__muso_id=current_user.muso)
    penalite_total_cot =sum(cotisation_info.values_list('penalite', flat=True))
    penalite_total = sum(remboursement_info.values_list('penalite', flat=True)) + penalite_total_cot

    return render(request, "membre_template/membre_home_template.html",{"credit_info":credit_info,"remb_info":remb_info, "montant_credit":montant_credit,"valeur2":valeur2, "montant_rembourse":montant_rembourse, "interet_anticipe":interet_anticipe, "Total_interet_restant":Total_interet_restant, "montant_total_restant":montant_total_restant, "montant_total_credit":montant_total_credit, "interet_total":interet_total, "montant_total_credit_encour":montant_total_credit_encour, "interet_total_encour":interet_total_encour, "remboursements_info":remboursements_info, "membre_count":membre_count, "montant_tot":montant_tot, "montant_ccredit":montant_ccredit, "montant_ijans":montant_ijans, "montant_fonk":montant_fonk ,   "penalite_total":penalite_total, "membre_obj": membre_obj, "montant_ijans":montant_ijans, "montant_fonk":montant_fonk })

def manage_membres(request):

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
    membre_obj=Membre.objects.get(admin_id=request.user.id)
    return render(request, "membre_template/manage_membres_template.html", { "membres": membres, "membre_obj" :membre_obj})

def liste_credits_encour(request):
    current_user = request.user
    muso_id = current_user.muso_id

    query = """
     SELECT 
    g_muso_app_tbcredit.numero AS codecredit_id,
    COUNT(g_muso_app_tbremboursement.id) AS quantite_remboursement,
    (g_muso_app_tbcredit.nbre_de_mois - COUNT(g_muso_app_tbremboursement.id)) AS Qtee_restant,
    IFNULL(SUM(g_muso_app_tbremboursement.capital_remb), 0) + IFNULL(SUM(g_muso_app_tbremboursement.interet_remb), 0) AS montant_total_rembourse,
    ((IFNULL(SUM(g_muso_app_tbremboursement.capital_remb), 0) + (IFNULL(SUM(g_muso_app_tbremboursement.interet_remb), 0)) * nbre_de_mois) - IFNULL(SUM(g_muso_app_tbremboursement.capital_remb), 0) + IFNULL(SUM(g_muso_app_tbremboursement.interet_remb), 0)) AS montant_total_Restant,
    IFNULL(SUM(g_muso_app_tbremboursement.interet_remb), 0) AS total_interet,
    (g_muso_app_tbcredit.nbre_de_mois * (g_muso_app_tbcredit.interet_credit * g_muso_app_tbcredit.montant_credit)) + g_muso_app_tbcredit.montant_credit AS Montant_tot,
    (IFNULL(SUM(g_muso_app_tbremboursement.interet_remb), 0) * nbre_de_mois) - IFNULL(SUM(g_muso_app_tbremboursement.interet_remb), 0) AS total_interet_restant,
    g_muso_app_tbcredit.date_debut, g_muso_app_tbcredit.date_fin,
    g_muso_app_membre.profile_pic, g_muso_app_membre.prenomp, g_muso_app_membre.nomp,
    SUM(penalite) AS total_penalite, (g_muso_app_tbcredit.interet_credit * g_muso_app_tbcredit.montant_credit) AS interetCredit
    FROM
        g_muso_app_tbcredit 
    LEFT JOIN
        g_muso_app_tbremboursement  ON g_muso_app_tbcredit.numero = g_muso_app_tbremboursement.codecredit_id
    JOIN
        g_muso_app_Membre  ON g_muso_app_tbcredit.code_membre_id = g_muso_app_Membre.id
    JOIN
        g_muso_app_CustomUser  ON g_muso_app_Membre.admin_id = g_muso_app_CustomUser.id
    WHERE
        (g_muso_app_tbcredit.credit_status = 'En cour' OR g_muso_app_tbremboursement.id IS NULL)
        AND g_muso_app_CustomUser.muso_id = %s
        
    GROUP BY
        g_muso_app_tbcredit.numero, g_muso_app_tbcredit.nbre_de_mois, g_muso_app_tbcredit.interet_credit, g_muso_app_tbcredit.montant_credit,
        g_muso_app_tbcredit.date_debut, g_muso_app_tbcredit.date_fin,
        g_muso_app_Membre.profile_pic, g_muso_app_Membre.prenomp, g_muso_app_Membre.nomp
    ORDER BY
        codecredit_id ASC;
        """

    with connection.cursor() as cursor:
        cursor.execute(query, [int(muso_id)])
        remboursement_info = cursor.fetchall()

    if 'q' in request.GET:
        q = request.GET['q']
        queryparametre = """
            SELECT 
    g_muso_app_tbcredit.numero AS codecredit_id,
    COUNT(g_muso_app_tbremboursement.id) AS quantite_remboursement,
    (g_muso_app_tbcredit.nbre_de_mois - COUNT(g_muso_app_tbremboursement.id)) AS Qtee_restant,
    IFNULL(SUM(g_muso_app_tbremboursement.capital_remb), 0) + IFNULL(SUM(g_muso_app_tbremboursement.interet_remb), 0) AS montant_total_rembourse,
    ((IFNULL(SUM(g_muso_app_tbremboursement.capital_remb), 0) + (IFNULL(SUM(g_muso_app_tbremboursement.interet_remb), 0)) * nbre_de_mois) - IFNULL(SUM(g_muso_app_tbremboursement.capital_remb), 0) + IFNULL(SUM(g_muso_app_tbremboursement.interet_remb), 0)) AS montant_total_Restant,
    IFNULL(SUM(g_muso_app_tbremboursement.interet_remb), 0) AS total_interet,
    (g_muso_app_tbcredit.nbre_de_mois * (g_muso_app_tbcredit.interet_credit * g_muso_app_tbcredit.montant_credit)) + g_muso_app_tbcredit.montant_credit AS Montant_tot,
    (IFNULL(SUM(g_muso_app_tbremboursement.interet_remb), 0) * nbre_de_mois) - IFNULL(SUM(g_muso_app_tbremboursement.interet_remb), 0) AS total_interet_restant,
    g_muso_app_tbcredit.date_debut, g_muso_app_tbcredit.date_fin,
    g_muso_app_membre.profile_pic, g_muso_app_membre.prenomp, g_muso_app_membre.nomp,
    SUM(penalite) AS total_penalite, (g_muso_app_tbcredit.interet_credit * g_muso_app_tbcredit.montant_credit) AS interetCredit
    FROM
        g_muso_app_tbcredit 
    LEFT JOIN
        g_muso_app_tbremboursement  ON g_muso_app_tbcredit.numero = g_muso_app_tbremboursement.codecredit_id
    JOIN
        g_muso_app_Membre  ON g_muso_app_tbcredit.code_membre_id = g_muso_app_Membre.id
    JOIN
        g_muso_app_CustomUser  ON g_muso_app_Membre.admin_id = g_muso_app_CustomUser.id
    WHERE
        (g_muso_app_tbcredit.credit_status = 'En cour' OR g_muso_app_tbremboursement.id IS NULL)
        AND g_muso_app_CustomUser.muso_id = %s
        
    GROUP BY
        g_muso_app_tbcredit.numero, g_muso_app_tbcredit.nbre_de_mois, g_muso_app_tbcredit.interet_credit, g_muso_app_tbcredit.montant_credit,
        g_muso_app_tbcredit.date_debut, g_muso_app_tbcredit.date_fin,
        g_muso_app_Membre.profile_pic, g_muso_app_Membre.prenomp, g_muso_app_Membre.nomp
    ORDER BY
        codecredit_id ASC;
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
    credits = paginator.get_page(page)
    qte_credit =tbcredit.objects.filter(credit_status='En cour',code_membre__admin__muso = muso_id).count()
    today = timezone.now()
    montant_total_interet = tbcredit.objects.filter(credit_status='En cour',code_membre__admin__muso_id=1,).filter(Q(date_debut__lte=today, date_fin__gte=today) |Q(date_debut__gte=today)).aggregate(total_interet=Sum(F('interet_credit') * F('montant_credit')))['total_interet']
    membre_obj=Membre.objects.get(admin_id=request.user.id)
    return render(request, "membre_template/liste_creditencours_template.html", { "credits":credits, "qte_credit":qte_credit, "montant_total_interet":montant_total_interet, "membre_obj":membre_obj  })

def liste_credits_encours(request):
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
    
    return render(request, "membre_template/liste_creditencours_template.html", { "credits":credits, "qte_credit":qte_credit  })

def interet_ajoute(request):
    current_user = request.user
    muso_id = current_user.muso
    qte_membre=Membre.objects.filter(membre_actif='True',admin__muso=current_user.muso).count()
    membre_obj=Membre.objects.get(admin_id=request.user.id)
    valeur2 = tbremboursement.objects.filter(faites_par__admin__muso=current_user.muso).values('date_remb').order_by('date_remb').annotate(sum=Sum('interet_remb'), sum2=Count('interet_remb')).order_by('-date_remb')
    return render(request, "membre_template/interets_ajoutes.html", { "valeur2":valeur2, "qte_membre":qte_membre, "membre_obj":membre_obj })

def membre_cotisation(request):
    current_user = request.user
    membre_obj=Membre.objects.get(admin=request.user.id ,admin__muso=current_user.muso)
    caisseverte = tbtypecotisation.objects.get(reference='cr', cotisation_muso=current_user.muso)
    caisserouge = tbtypecotisation.objects.get(reference='cv', cotisation_muso=current_user.muso)
    caissebleue = tbtypecotisation.objects.get(reference='cb', cotisation_muso=current_user.muso)
    
    if caisseverte:
        _credit  =tbcotisation.objects.filter(code_membre_id=membre_obj, typecotisation=caisseverte.nom_cotisation, code_membre__admin__muso=current_user.muso)
        qtite_cotcredit = (_credit.values_list('montant', flat=True)).count()
    else:
        qtite_cotcredit =0
    
    if caissebleue:
        _ijans  =tbcotisation.objects.filter(code_membre_id=membre_obj,typecotisation=caissebleue.nom_cotisation, code_membre__admin__muso=current_user.muso)
        qtite_cotijans = (_ijans.values_list('montant', flat=True)).count()
    else:
        qtite_cotijans =0
    
    if caisserouge:
        _fonctionnement  =tbcotisation.objects.filter(code_membre_id=membre_obj,typecotisation=caisserouge.nom_cotisation, code_membre__admin__muso=current_user.muso)
        qtite_cotfonk = (_fonctionnement.values_list('montant', flat=True)).count()
    else:
        qtite_cotfonk =0
 
    cotisations = tbcotisation.objects.filter(code_membre_id=membre_obj, code_membre__admin__muso=current_user.muso).order_by('-date_fait')
    return render(request, "membre_template/membre_cotisation.html", { "membre_obj":membre_obj,  "cotisations":cotisations, "qtite_cotcredit":qtite_cotcredit, "qtite_cotijans":qtite_cotijans, "qtite_cotfonk":qtite_cotfonk })

def membre_credit(request):
    current_user = request.user
    membre_obj=Membre.objects.get(admin=request.user.id,admin__muso=current_user.muso)
    credits = tbcredit.objects.filter(code_membre_id=membre_obj, code_membre__admin__muso=current_user.muso).order_by('-date_credit')
    return render(request, "membre_template/membre_credit.html", {"membre_obj":membre_obj, "credits":credits })

def membre_remboursement(request):
    current_user = request.user
    membre_obj=Membre.objects.get(admin=request.user.id, admin__muso=current_user.muso)
    rembous = tbremboursement.objects.filter(faites_par_id=membre_obj, faites_par__admin__muso=current_user.muso).order_by('-date_remb')
    return render(request, "membre_template/membre_remboursement.html", { "membre_obj":membre_obj, "rembous":rembous })

def Lesinterets_membre_ajoutes(request):
    current_user = request.user
    #muso_id = current_user.muso
    qte_membre=Membre.objects.filter(membre_actif=1, admin__muso=current_user.muso).count()
    valeur2 = tbremboursement.objects.filter( faites_par__admin__muso=current_user.muso).values('date_remb').order_by('date_remb').annotate(sum=Sum('interet_remb')/qte_membre, sum2=Count('interet_remb')).order_by('-date_remb')
 
    if 'q' in request.GET:
        q = request.GET['q']
        qte_membre=Membre.objects.filter(membre_actif=1, admin__muso=current_user.muso).count()
        valeur2 = tbremboursement.objects.filter(  Q(date_remb__year=q) | Q(codecredit=q), Q(faites_par__admin__muso=current_user.muso) ).values('date_remb').order_by('-date_remb').annotate(sum=Sum('interet_remb')/qte_membre, sum2=Count('interet_remb'))
    else:
        qte_membre=Membre.objects.filter(membre_actif=1, admin__muso=current_user.muso).count()
        valeur2 = tbremboursement.objects.filter( faites_par__admin__muso=current_user.muso).values('date_remb').order_by('-date_remb').annotate(sum=Sum('interet_remb')/qte_membre, sum2=Count('interet_remb'))
       
    paginator = Paginator(valeur2,15)
    page = request.GET.get('page')
    rembs = paginator.get_page(page)
    membre_obj=Membre.objects.get(admin=request.user.id, admin__muso=current_user.muso)
    
    return render(request, "membre_template/Lesinterets_membre_ajoutes.html", {"membre_obj":membre_obj, "valeur2":valeur2, "qte_membre":qte_membre })

def statistique_remboursements(request):
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
    membre_obj=Membre.objects.get(admin_id=request.user.id)
    return render(request, "membre_template/statistique_remboursements_template.html", { "remboursement_info":remboursement_info, "membre_obj":membre_obj })

def statistique_credits(request):
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
    
    
    #--------------modification------------------------
    db_path = "db.sqlite3"
    query = """
        SELECT
        SUM(montant_credit) AS sum_montant_credit,
        SUM((montant_credit * interet_credit * nbre_de_mois) + montant_credit) AS montant_rembourser,
        SUM(((montant_credit * interet_credit * nbre_de_mois) + montant_credit) - montant_credit) AS interet_total_credit
        FROM
            g_muso_app_tbcredit 
        LEFT JOIN
        
            g_muso_app_Membre  ON g_muso_app_tbcredit.code_membre_id = g_muso_app_Membre.id
        JOIN
            g_muso_app_CustomUser  ON g_muso_app_Membre.admin_id = g_muso_app_CustomUser.id
        WHERE
            g_muso_app_CustomUser.muso_id = ?
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    current_users = request.user
   
    # Exécutez la requête
    cursor.execute(query, (current_users.muso_id,))

    # Parcourez les résultats pour calculer la somme du montant_total_Restant
    montant_total_credit = 0
    montant_total_remboursement = 0
    montant_total_interet = 0
    for row in cursor.fetchall():
        montant_total_credit = row[0]
        montant_total_remboursement = row[1]
        montant_total_interet = row[2]

    #---------------fin-modification---------------------

    
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
    membre_obj=Membre.objects.get(admin_id=request.user.id)
    return render(request, "membre_template/statistique_credit_template.html", {"membre_obj":membre_obj, "montant_total_credit":montant_total_credit, "montant_total_remboursement":montant_total_remboursement, "montant_total_interet":montant_total_interet,  "credit_info":credit_info, "interet_anticipe":interet_anticipe })


def membre_apply_leave(request):
    current_user = request.user
    membre_obj=Membre.objects.get(admin=request.user.id, admin__muso=current_user.muso)
    leave_data=LeaveReportMembre.objects.filter(code_membre=membre_obj)
    return render(request, "membre_template/membre_apply_leave.html", {"membre_obj":membre_obj, "leave_data":leave_data})

def membre_apply_leave_save(request):
    
    if request.method!="POST":
        return HttpResponseRedirect(reverse("membre_apply_leave"))
    else:
        leave_date=request.POST.get("leave_date")
        leave_msg=request.POST.get("leave_msg")

        membre_obj=Membre.objects.get(admin=request.user.id)
        try:
            leave_report=LeaveReportMembre(code_membre=membre_obj, leave_date=leave_date,leave_message=leave_msg,leave_status=0)
            leave_report.save()
            messages.success(request,"Successfully Applied for Leave")
            return HttpResponseRedirect(reverse("membre_apply_leave")) 
        except Exception as e:
            messages.error(request,traceback.format_exc())
            return HttpResponseRedirect(reverse("membre_apply_leave"))

def membre_feedback(request):
    current_user = request.user
    membre_id=Membre.objects.get(admin=request.user.id)
    feedback_data=FeedBackMembre.objects.filter(code_membre=membre_id)
    membre_obj=Membre.objects.get(admin=request.user.id, admin__muso=current_user.muso)
    return render(request, "membre_template/membre_feedback.html", {"membre_obj":membre_obj, "membre_data":feedback_data})

def membre_feedback_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("membre_feedback_save"))
    else:
        feedback_msg=request.POST.get("feedback_msg")
        membre_obj=Membre.objects.get(admin=request.user.id)
        try:
            feedback=FeedBackMembre(code_membre=membre_obj, feedback=feedback_msg, feedback_reply="")
            feedback.save()
            messages.success(request,"Successfully Sent Feedback")
            return HttpResponseRedirect(reverse("membre_feedback")) 
        except Exception as e:
            messages.error(request,traceback.format_exc())
            return HttpResponseRedirect(reverse("membre_feedback"))

def membre_profile(request):
    current_user = request.user
    user=CustomUser.objects.get(id=request.user.id)
    membre=Membre.objects.get(admin=user)
    membre_obj=Membre.objects.get(admin=request.user.id, admin__muso=current_user.muso)
    return render(request,"membre_template/membre_profile.html",{"membre_obj":membre_obj, "user":user, "membre":membre})

def membre_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("membre_profile"))
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

        membre=Membre.objects.get(admin=customuser.id)
        membre.save()
        messages.success(request,"Successfully Update Profile")
        return HttpResponseRedirect(reverse("membre_profile"))
    except:
        messages.success(request,"Failed Update Profile")
        return HttpResponseRedirect(reverse("membre_profile"))

def add_mcomments_save(request):
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
            return HttpResponseRedirect(reverse("profile_mview")) 
        except Exception as e:
            traceback.print_exc() 
            return HttpResponseRedirect(reverse("profile_mview"))
        
def profile_mview(request):
    current_user = request.user
    muso_id = current_user.muso
    # Logic for the profile view
    comments = Comment.objects.filter(author_id=F('author_id__id'), muso_id_id=muso_id).order_by('-created_at').values('id', 'text', 'created_at', 'author_id__profile_pic', 'author_id__nomp', 'author_id__prenomp')
    membre_obj=Membre.objects.get(admin=request.user.id, admin__muso=current_user.muso)
    today_date = datetime.now().date()

    for comment in comments:
        created_at_date = comment['created_at'].date()
        difference = today_date - created_at_date
        comment['difference_in_days'] = difference.days

    return render(request, 'membre_template/commentaire.html', {"membre_obj":membre_obj, 'comments': comments})

def user_info(request):
    # Récupérer l'ID de l'utilisateur connecté
    user_id = request.user.id
   
    user_type = request.user.username  
    
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
    
    return render(request, 'membre_template/user_info.html', context)