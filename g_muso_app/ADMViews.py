from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
import traceback
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from g_muso_app.models import CustomUser, Membre, tbcotisation, tbcredit,tbremboursement,FeedBackMembre,LeaveReportMembre,CustomUser, tbdepense, tbmuso, CustomUserPermission, tbtypecotisation
from .forms import AddMembreForm,EditMembreForm, EditMusoForm, AddMusoForm
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.core.paginator import Paginator
from django.db.models import Max, Sum, Count
from django.db import connection
from django.db.models.functions import Coalesce
import csv
from django.contrib.auth.models import Permission
from django.core import serializers
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

def adm_home(request):
    nombre_muso = tbmuso.objects.all().count()
    membre_count=Membre.objects.filter(membre_actif='True').count()
    #membre_count_par_muso=Membre.objects.filter(membre_actif='True').group_by('admin__muso').count()
    membre_count_par_muso=Membre.objects.values('admin__muso', 'admin__muso__nom_muso').annotate(dcount=Count('id')).order_by()
    #membre_count_par_muso = Membre.objects.values('admin__muso').annotate(dcount=Count('admin__muso')).order_by()
    #muso_infoo = tbmuso.object.filter(id=membre_count_par_muso.admin__muso)
    cotisation_info=tbcotisation.objects.all()
    montant_tot = sum(cotisation_info.values_list('montant', flat=True))
    
    _credit  =tbcotisation.objects.filter(typecotisation__icontains='Fond de Credit')
    montant_ccredit = sum(_credit.values_list('montant', flat=True))

    _ijans  =tbcotisation.objects.filter(typecotisation__icontains="Fond d'Urgence")
    montant_ijans = sum(_ijans.values_list('montant', flat=True))

    _fonctionnement  =tbcotisation.objects.filter(typecotisation__icontains='Fond de Fonctionnement')
    montant_fonk = sum(_fonctionnement.values_list('montant', flat=True))

    rembourseent_infor=tbremboursement.objects.all()
    interet_tot = format(sum(rembourseent_infor.values_list('interet_remb', flat=True)),'.2f')

    valeur2 = tbremboursement.objects.filter().values('date_remb').order_by('date_remb').annotate(sum=Sum('interet_remb'))
    
    credit_info = tbcredit.objects.filter(credit_status__icontains="En cour")
    montant_credit = sum(credit_info.values_list('montant_credit', flat=True))
    remb_info = tbremboursement.objects.filter().values('codecredit_id').order_by('codecredit_id').annotate(capital_remb=Sum('capital_remb'))
    montant_rembourse = format(sum(remb_info.values_list('capital_remb', flat=True)),'.2f')
    
    return render(request, "adm_template/home_content.html",{ "credit_info":credit_info,  "membre_count_par_muso":membre_count_par_muso, "membre_count":membre_count, "nombre_muso":nombre_muso, "montant_tot":montant_tot, "montant_credit":montant_credit,"montant_rembourse":montant_rembourse, "remb_info":remb_info, "montant_ccredit":montant_ccredit, "montant_ijans":montant_ijans, "montant_fonk":montant_fonk , "valeur2":valeur2, "interet_tot":interet_tot})
   
def add_personne(request):
    pass

def add_muso1(request):
    muso = tbmuso.objects.all()
    return render(request, "adm_template/add_muso1_template.html",{"muso":muso})

def add_muso1_save(request):
    if request.method !="POST":
        return HttpResponse("Method Not Allowed")
    else:
        code_muso = request.POST.get("numero_credit")
        sigle = request.POST.get("sigle")
        nom_muso = request.POST.get("nom_muso")
        adresse_muso = request.POST.get("adresse_muso")
        telephone_muso = request.POST.get("telephone_muso")
        email_muso = request.POST.get("email_muso")
        site_muso = request.POST.get("site_muso")
        date_creation = request.POST.get("date_creation")
        couleur_menu = request.POST.get("couleur_preferee")
        taux_interet = request.POST.get("taux_interet")
        couleur_text_menu = request.POST.get("couleur_text_menu")

        logo_pic = request.FILES['logo_muso']
        fs = FileSystemStorage()
        filename = fs.save(logo_pic.name, logo_pic)
        logo_pic_url = fs.url(filename)

        try:
            muso=tbmuso(codemuso=code_muso, sigle=sigle, nom_muso=nom_muso, adresse_muso=adresse_muso, telephone_muso=telephone_muso, email_muso=email_muso, site_muso=site_muso, logo_muso=logo_pic_url, date_creation=date_creation, couleur_preferee=couleur_menu, taux_interet=taux_interet, couleur_text_menu=couleur_text_menu)
            muso.save()
           
            muso_id = tbmuso.objects.aggregate(max_valeur=Max('id'))['max_valeur']

            valeur1 = request.POST.get("cotisation_1")
            valeurr1 = request.POST.get("reference1")
            valeur2 = request.POST.get("cotisation_2")
            valeurr2 = request.POST.get("reference2")
            valeur3 = request.POST.get("cotisation_3")
            valeurr3 = request.POST.get("reference3")
            typecotisation = tbtypecotisation(nom_cotisation=valeur1, cotisation_muso_id=muso_id, reference=valeurr1)
            typecotisation1 = tbtypecotisation(nom_cotisation=valeur2, cotisation_muso_id=muso_id, reference=valeurr2)
            typecotisation2 = tbtypecotisation(nom_cotisation=valeur3, cotisation_muso_id=muso_id, reference=valeurr3)
            typecotisation.save()
            typecotisation1.save()
            typecotisation2.save()
        
            messages.success(request,"Successfully Added MUSO")
            return HttpResponseRedirect(reverse("add_muso1")) 
        except Exception as e:
            messages.error(request,traceback.format_exc())
            return HttpResponseRedirect(reverse("add_muso1"))



def add_muso(request):
    form = AddMusoForm()
    return render(request, "adm_template/add_muso_template.html",{"form":form})

def add_muso_save(request):
    
    if request.method !="POST":
        return HttpResponse("Method Not Allowed")
    else:
        form=AddMusoForm(request.POST,request.FILES)
        if form.is_valid():
            code_muso = form.cleaned_data["codemuso"]
            sigle = form.cleaned_data["sigle"]
            nom_muso = form.cleaned_data["nom_muso"]
            adresse_muso = form.cleaned_data["adresse_muso"]
            telephone_muso = form.cleaned_data["telephone_muso"]
            email_muso = form.cleaned_data["email_muso"]
            site_muso = form.cleaned_data["site_muso"]
            date_creation = form.cleaned_data["date_creation"]
            couleur_menu = form.cleaned_data["couleur_preferee"]
            taux_interet = form.cleaned_data["taux_interet"]
            couleur_text_menu = form.cleaned_data["couleur_text_menu"]

            logo_pic = request.FILES['logo_muso']
            fs = FileSystemStorage()
            filename = fs.save(logo_pic.name, logo_pic)
            logo_pic_url = fs.url(filename)

            try:
                muso=tbmuso(codemuso=code_muso, sigle=sigle, nom_muso=nom_muso, adresse_muso=adresse_muso, telephone_muso=telephone_muso, email_muso=email_muso, site_muso=site_muso, logo_muso=logo_pic_url, date_creation=date_creation, couleur_preferee=couleur_menu, taux_interet=taux_interet, couleur_text_menu=couleur_text_menu)
                #muso=tbmuso(codemuso=code_muso, sigle=sigle, nom_muso=nom, adresse_muso=adresse, telephone_muso=telephone, email_muso=email, site_muso=site_web, logo_muso=logo_pic_url, date_creation=date_creation)
                muso.save()

                messages.success(request,"Successfully Added Muso")
                return HttpResponseRedirect(reverse("add_muso")) 
            except Exception as e:
                messages.error(request,traceback.format_exc())
                return HttpResponseRedirect(reverse("add_muso"))
        else:
                form.AddMusoForm(request.POST)
                return render("adm_template/add_muso_template.html", {"form":form})

def add_depenseAH(request):
    depenses = tbdepense.objects.all()
    return render(request, "adm_template/add_depense_template.html", {"depenses":depenses})

def add_depense_saveAH(request):
 
    if request.method !="POST":
        return HttpResponse("Method Not Allowed")
    else:
        date_depense = request.POST.get("date_depense")
        description = request.POST.get("description")
        depense_unit = request.POST.get("depense_unit")
        quantite_dep = request.POST.get("quantite_dep")

        try:
            depense=tbdepense(date_depense=date_depense,  description=description, depense_unit=float(depense_unit), quantite_dep=float(quantite_dep))
            depense.save()
        
            messages.success(request,"Successfully Added Depense")
            return HttpResponseRedirect(reverse("add_depense")) 
        except Exception as e:
            messages.error(request,traceback.format_exc())
            return HttpResponseRedirect(reverse("add_depense"))

def manage_muso(request):
    muso = tbmuso.objects.all()
    if 'q' in request.GET:
        q = request.GET['q']
        
        all_muso_list = tbmuso.objects.filter( Q(nom_muso=q) | Q(codemuso__icontains=q) | Q(sigle__icontains=q))
    else:
        all_muso_list = tbmuso.objects.all()
    paginator = Paginator(all_muso_list,10)
    page = request.GET.get('page')
    musos = paginator.get_page(page)
    return render(request, "adm_template/manage_muso_template.html", { "musos": musos })

def manage_user(request):
    muso = CustomUser.objects.all()
    if 'q' in request.GET:
        q = request.GET['q']
        
        all_user_list = CustomUser.objects.filter( Q(username__icontains=q) | Q(email__icontains=q))
    else:
        all_user_list = CustomUser.objects.all()
    paginator = Paginator(all_user_list,10)
    page = request.GET.get('page')
    musos = paginator.get_page(page)
    return render(request, "adm_template/manage_user_template.html", { "musos": musos })

def statistique_remboursementAH(request):
    #remboursement_info = tbremboursement.objects.all()
    remboursement_info = tbremboursement.objects.all().select_related("tbcredit").values('codecredit_id').annotate(total=Count('codecredit_id'), sum=Sum('capital_remb')).order_by('-codecredit_id')
    #remboursement_info = tbremboursement.objects.select_related("tbcredit").values_list('codecredit_id', 'nbre_de_mois','date_debut','capital_remb','interet_remb')
    
    if 'q' in request.GET:
        q = request.GET['q']
        all_remboursement_info = tbremboursement.objects.filter(  Q(codecredit_id=q) ).values('codecredit_id').annotate(total=Count('codecredit_id'), sum=Sum('capital_remb')).order_by('-codecredit_id')
    else:
        all_remboursement_info = tbremboursement.objects.all().select_related("tbcredit").values('codecredit_id').annotate(total=Count('codecredit_id'), sum=Sum('capital_remb')).order_by('-codecredit_id')
    paginator = Paginator(all_remboursement_info,15)
    page = request.GET.get('page')
    rembs = paginator.get_page(page)
    return render(request, "adm_template/statistique_remboursement_template.html", { "remboursement_info":remboursement_info })

def interets_ajoutesAH(request):
    qte_membre=Membre.objects.all().count()
    rembourseent_info=tbremboursement.objects.all()
    interet_total = sum(rembourseent_info.values_list('interet_remb', flat=True))
    penalite_total = sum(rembourseent_info.values_list('penalite', flat=True))
    #valeur2 = tbremboursement.objects.filter().values('date_remb').order_by('date_remb').annotate(sum=Sum('interet_remb')/qte_membre, sum2=Count('interet_remb'))
    valeur2 = tbremboursement.objects.filter().values('date_remb').order_by('date_remb').annotate(sum=Sum('interet_remb'), sum2=Count('interet_remb'), sum3=Sum('montant_a_remb'), sum4=Sum('penalite'))
    return render(request, "adm_template/Lesinterets_ajoutes.html", { "valeur2":valeur2, "qte_membre":qte_membre, "interet_total":interet_total, "penalite_total":penalite_total})

def edit_muso(request, muso_id):
    request.session['muso_id']=muso_id
    muso_info=tbmuso.objects.get(id=muso_id)
    form=EditMusoForm()
   
    form.fields['codemuso'].initial=muso_info.codemuso
    form.fields['sigle'].initial=muso_info.sigle
    form.fields['nom_muso'].initial=muso_info.nom_muso
    form.fields['adresse_muso'].initial=muso_info.adresse_muso
    form.fields['telephone_muso'].initial=muso_info.telephone_muso
    form.fields['email_muso'].initial=muso_info.email_muso
    form.fields['site_muso'].initial=muso_info.site_muso
    form.fields['logo_muso'].initial=muso_info.logo_muso
    form.fields['date_creation'].initial=muso_info.date_creation
    
    return render(request, "adm_template/edit_muso_template.html",{"form":form,"muso_info":muso_info, "id":muso_id})

def edit_muso_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed </h2>")
    else:
        muso_id = request.session.get("muso_id")
        if muso_id == None:
            return HttpResponseRedirect(reverse("manage_muso"))

        form = EditMembreForm(request.POST, request.FILES)
        if form.is_valid():
            # email=form.cleaned_data["email"]
            codemuso=form.cleaned_data["codemuso"]
            sigle=form.cleaned_data["sigle"]
            nom_muso=form.cleaned_data["nom_muso"]
            adresse_muso=form.cleaned_data["adresse_muso"]
            telephone_muso = form.cleaned_data["telephone_muso"]
            email_muso = form.cleaned_data["email_muso"]
            site_muso=form.cleaned_data["site_muso"]
            date_creation=form.cleaned_data["date_creation"]
           
            if request.FILES.get('logo_pic', False):
                logo_pic = request.FILES['logo_pic']
                fs = FileSystemStorage()
                filename=fs.save(logo_pic.name, logo_pic)
                logo_pic_url=fs.url(filename)
            else:
                logo_pic_url = None

            try:
               
                muso=tbmuso.objects.get(id=muso_id)
                muso.codemuso=codemuso
                muso.sigle = sigle
                muso.nom_muso=nom_muso
                muso.adresse_muso = adresse_muso
                muso.telephone_muso=telephone_muso
                muso.email_muso=email_muso
                muso.site_muso=site_muso
                muso.date_creation=date_creation
                
                muso.logo_pic=logo_pic_url  
                if logo_pic_url != None:
                    muso.logo_pic=logo_pic_url
                muso.save()
                del request.session['muso_id']
                messages.success(request,"Successfully Edited muso")
                return HttpResponseRedirect(reverse("edit_muso", kwargs={"muso_id":muso_id})) 
            except Exception as e:
                messages.error(request,traceback.format_exc())
                return HttpResponseRedirect(reverse("edit_muso", kwargs={"muso_id":muso_id}))
        else:
            form=EditMusoForm(request.POST)
            muso = tbmuso.objects.get(id=muso_id)
            return render(request, "adm_template/edit_muso_template.html", {"form":form, "id":muso_id, "nom":muso.nom_muso})
    



def edit_depenseAH(request, depense_id):
    depenses = tbdepense.objects.get(id=depense_id)
    return render(request, "adm_template/edit_depense_template.html", {"depenses":depenses})

def edit_depense_saveAH(request):

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
        
def edit_user(request, user_id):
    muso_info = tbmuso.objects.all()
    user = CustomUser.objects.get(id=user_id)
    membres = CustomUser.objects.filter(user_type=2)
    return render(request, "adm_template/edit_user_template.html", {"user":user, "membres":membres,"membre_info":muso_info})

def edit_user_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("manage_user"))
    else:
        id = request.POST.get("id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")
        is_superuser =request.POST.get("is_superuser")
        username =request.POST.get("username")
        email=request.POST.get("password")
        is_staff=request.POST.get("is_staff")
        is_active =request.POST.get("is_active")
        user_type =request.POST.get("user_type")
       
    try:
        customuser=CustomUser.objects.get(id=id)
        #customuser.first_name=first_name
        #customuser.last_name=last_name
        customuser.is_superuser =is_superuser
        #customuser.username = username
        #customuser.email = email
        customuser.is_staff = is_staff
        customuser.is_active = is_active
        customuser.user_type = user_type
        customuser.save()
        messages.success(request,"Successfully Update User")
        return HttpResponseRedirect(reverse("manage_user"))
    except:
        messages.success(request,"Failed Update User")
        return HttpResponseRedirect(reverse("manage_user"))

# export tous les muso       
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="mydata.csv"'

    writer = csv.writer(response)
    writer.writerow(['Code Muso', 'sigle', 'Nom Muso', 'Adresse', 'Telephone', 'Email', 'Site', 'Logo', 'date_creation']) # Add column headers

    my_data = tbmuso.objects.all()
    for item in my_data:
        writer.writerow([item.codemuso, item.sigle, item.nom_muso, item.adresse_muso, item.telephone_muso, item.email_muso, item.site_muso, item.logo_muso, item.date_creation]) # Add data rows
    return response

# export tous les users       
def export_users_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Liste_User.csv"'

    writer = csv.writer(response)
    writer.writerow(['Code User', 'Username', 'Prenom', 'Nom', 'Email', 'Staff', 'Actif', 'Date Ajout',  'MUSO']) # Add column headers

    my_data = CustomUser.objects.all()
    for item in my_data:
        writer.writerow([item.id, item.username, item.first_name, item.last_name, item.email, item.is_staff, item.is_active, item.date_joined, item.muso.nom_muso]) # Add data rows
    return response

def add_new_user(request):
    muso = tbmuso.objects.all()
    #muso_info = tbmuso.objects.all()
    return render(request, "adm_template/add_customeruser_template.html", {"muso":muso})

def add_customuser_save(request):
    if request.method !="POST":
        return HttpResponse("Method Not Allowed")
    else:
        username = request.POST.get("username")
        password=request.POST.get("password")
        lastname = request.POST.get("lastname")
        firstname = request.POST.get("firstname")
        email=request.POST.get("email")
        muso_id = request.POST.get("muso")
        type_utilisateur = request.POST.get("type_utilisateur")
        # Récupérer l'instance de tbmuso correspondant à muso_id
        muso_instance = tbmuso.objects.get(id=muso_id)          

        try:
            user=CustomUser.objects.create_user(username=username , password=password, email=email, last_name=lastname, first_name=firstname, user_type=type_utilisateur, muso=muso_instance )
            #user.save()
            messages.success(request,"Successfully Added USER")
            return HttpResponseRedirect(reverse("add_new_user")) 
        except Exception as e:
            messages.error(request,traceback.format_exc())
            return HttpResponseRedirect(reverse("add_new_user"))
    
'''def muso_view(request):
    muso = tbmuso.objects.all()
    context = {
        'muso': muso
    }
    return render(request, 'add_customeruser_template.html', context)'''

def show_aceess(request):
    current_user = request.user
    muso_id = current_user.muso
    #initial_data = Permission.objects.all()[:10]  # Retrieve initial data (e.g., first 10 items)
    membre_info = Membre.objects.filter(admin__muso=current_user.muso)
    membres = CustomUser.objects.filter(user_type=1,muso=current_user.muso)
    initial_data = Permission.objects.all()
    return render(request, 'adm_template/access_user_template.html', {'initial_data': initial_data, 'membre_info':membre_info, 'membres':membres })


def save_access_to_user(request):
    if request.method == 'POST':
        selected_user_id = request.POST.get('user')
        selected_permissions = request.POST.getlist('permissions')
        
        user = CustomUser.objects.get(id=selected_user_id)
        user.user_permissions.clear()
        try:
            for permission_id in selected_permissions:
                permission = Permission.objects.get(id=permission_id)
                user.user_permissions.add(permission)
            messages.success(request, "Successfully Modify Access")
            return HttpResponseRedirect(reverse("show_aceess")) 
        except Exception as e:
            messages.error(request, traceback.format_exc())
            return HttpResponseRedirect(reverse("show_aceess"))
  

def load_more_data(request):
    offset = int(request.GET.get('offset', 0))
    limit = int(request.GET.get('limit', 10))

    additional_data = Permission.objects.all()[offset:offset+limit].values()

    return JsonResponse({'items': list(additional_data)})