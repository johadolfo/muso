from django.shortcuts import render
from g_muso_app.models import  CustomUser, Membre,FeedBackMembre,LeaveReportMembre, tbcotisation, tbcredit, tbremboursement, Comment
from django.http import HttpResponse
import datetime
from django.urls import reverse
from django.contrib import messages
import traceback
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from django.db.models import Q
from django.core.paginator import Paginator
from django.db.models import Max, Sum, Count
from django.db import connection
from django.db.models.functions import Coalesce
from django.db.models import F

def membre_home(request):
    has_permission = request.user.has_perm('g_muso_app.add_depense')
    current_user = request.user
    muso_id = current_user.muso
    membre_count=Membre.objects.filter(membre_actif='True', admin__muso=current_user.muso).count()
    membre_obj=Membre.objects.get(admin_id=request.user.id)
    #cotisation_info=tbcotisation.objects.filter(code_membre_id=membre_obj).filter( typecotisation="Fond de Credit")
    cotisation_info=tbcotisation.objects.filter(code_membre_id=membre_obj, typecotisation="Fond de Credit", code_membre__admin__muso=current_user.muso,code_membre__membre_actif='True')
    cotisation_FU=tbcotisation.objects.filter(code_membre_id=membre_obj, typecotisation="Fond d'Urgence", code_membre__admin__muso=current_user.muso,code_membre__membre_actif='True')
    interet_membre = sum(tbremboursement.objects.filter(faites_par__admin__muso=current_user.muso).values_list('interet_remb', flat=True))
    #montant_tot = format((sum(cotisation_info.values_list('montant', flat=True))+ (interet_membre / membre_count)),'.2f')
    montant_tot = format((sum(cotisation_info.values_list('montant', flat=True))+ sum(cotisation_info.values_list('interet', flat=True))+ sum(cotisation_FU.values_list('montant', flat=True))),'.2f')
    valeur2 = tbremboursement.objects.filter(faites_par__admin__muso=current_user.muso).values('date_remb').order_by('date_remb').annotate(sum=Sum('interet_remb'))

    _credit  =tbcotisation.objects.filter(code_membre_id=membre_obj, typecotisation__icontains='Fond de Credit',code_membre__admin__muso=current_user.muso)
    montant_ccredit = sum(_credit.values_list('montant', flat=True))

    _ijans  =tbcotisation.objects.filter(code_membre_id=membre_obj, typecotisation__icontains="Fond d'Urgence",code_membre__admin__muso=current_user.muso)
    montant_ijans = sum(_ijans.values_list('montant', flat=True))

    _fonctionnement  =tbcotisation.objects.filter(code_membre_id=membre_obj, typecotisation__icontains='Fond de Fonctionnement',code_membre__admin__muso=current_user.muso)
    montant_fonk = sum(_fonctionnement.values_list('montant', flat=True))
    valeur2 = tbremboursement.objects.filter(faites_par__admin__muso=current_user.muso).values('date_remb').order_by('date_remb').annotate(sum=Sum('interet_remb'))
   
    credit_info = tbcredit.objects.filter(credit_status__icontains="En cour", code_membre__admin__muso=current_user.muso)
    montant_credit = sum(credit_info.values_list('montant_credit', flat=True))
    #remb_info = tbremboursement.objects.all()
    remb_info = tbremboursement.objects.filter(faites_par__admin__muso=current_user.muso).values('codecredit_id').order_by('codecredit_id').annotate(capital_remb=Sum('capital_remb'))
    montant_rembourse = format(sum(remb_info.values_list('capital_remb', flat=True)),'.2f')
    
 
    montant_rembourse = format(sum(remb_info.values_list('capital_remb', flat=True)),'.2f')
    return render(request, "membre_template/membre_home_template.html",{"has_permission":has_permission, "membre_obj": membre_obj, "credit_info":credit_info, "membre_count":membre_count, "montant_tot":montant_tot, "montant_credit":montant_credit,"montant_rembourse":montant_rembourse, "remb_info":remb_info, "montant_ccredit":montant_ccredit, "montant_ijans":montant_ijans, "montant_fonk":montant_fonk , "valeur2":valeur2})
   

    #return render(request, "membre_template/membre_home_template.html",{"montant_total":montant_total,"montant_penalite":montant_penalite, "montant_interet":montant_interet, "montant_credit":montant_credit })
def interet_ajoute(request):
    current_user = request.user
    muso_id = current_user.muso
    qte_membre=Membre.objects.filter(membre_actif='True',admin__muso=current_user.muso).count()
    valeur2 = tbremboursement.objects.filter(faites_par__admin__muso=current_user.muso).values('date_remb').order_by('date_remb').annotate(sum=Sum('interet_remb'), sum2=Count('interet_remb')).order_by('-date_remb')
    return render(request, "membre_template/interets_ajoutes.html", { "valeur2":valeur2, "qte_membre":qte_membre })

def membre_cotisation(request):
    current_user = request.user
    muso_id = current_user.muso
    #request.session['membre_id']=request.user.id
    membre_obj=Membre.objects.get(admin=request.user.id ,admin__muso=current_user.muso)

    
    _credit  =tbcotisation.objects.filter(code_membre_id=membre_obj, typecotisation__icontains='Fond de Credit', code_membre__admin__muso=current_user.muso)
    qtite_cotcredit = (_credit.values_list('montant', flat=True)).count()

    _ijans  =tbcotisation.objects.filter(code_membre_id=membre_obj,typecotisation__icontains="Fond d'Urgence", code_membre__admin__muso=current_user.muso)
    qtite_cotijans = (_ijans.values_list('montant', flat=True)).count()

    _fonctionnement  =tbcotisation.objects.filter(code_membre_id=membre_obj,typecotisation__icontains='Fond de Fonctionnement', code_membre__admin__muso=current_user.muso)
    qtite_cotfonk = (_fonctionnement.values_list('montant', flat=True)).count()


    cotisations = tbcotisation.objects.filter(code_membre_id=membre_obj, code_membre__admin__muso=current_user.muso).order_by('-date_fait')
    return render(request, "membre_template/membre_cotisation.html", { "cotisations":cotisations, "qtite_cotcredit":qtite_cotcredit, "qtite_cotijans":qtite_cotijans, "qtite_cotfonk":qtite_cotfonk })

def membre_credit(request):
    current_user = request.user
    muso_id = current_user.muso
    #request.session['membre_id']=request.user.id
    membre_obj=Membre.objects.get(admin=request.user.id,admin__muso=current_user.muso)
    credits = tbcredit.objects.filter(code_membre_id=membre_obj, code_membre__admin__muso=current_user.muso).order_by('-date_credit')
    return render(request, "membre_template/membre_credit.html", { "credits":credits })

def membre_remboursement(request):
    current_user = request.user
    muso_id = current_user.muso
    #request.session['membre_id']=request.user.id
    membre_obj=Membre.objects.get(admin=request.user.id, admin__muso=current_user.muso)
    rembous = tbremboursement.objects.filter(faites_par_id=membre_obj, faites_par__admin__muso=current_user.muso).order_by('-date_remb')
    return render(request, "membre_template/membre_remboursement.html", { "rembous":rembous })

def Lesinterets_membre_ajoutes(request):
    current_user = request.user
    muso_id = current_user.muso
    qte_membre=Membre.objects.filter(membre_actif=1, admin__muso=current_user.muso).count()
    valeur2 = tbremboursement.objects.filter( faites_par__admin__muso=current_user.muso).values('date_remb').order_by('date_remb').annotate(sum=Sum('interet_remb')/qte_membre, sum2=Count('interet_remb')).order_by('-date_remb')
 
    if 'q' in request.GET:
        q = request.GET['q']
        #all_remboursement_info = tbremboursement.objects.filter(  Q(codecredit_id=q) ).values('codecredit_id').annotate(total=Count('codecredit_id'),faites_par__admin__muso = muso_id, sum=Sum('capital_remb')).order_by('-codecredit_id')
        qte_membre=Membre.objects.filter(membre_actif=1, admin__muso=current_user.muso).count()
        valeur2 = tbremboursement.objects.filter(  Q(date_remb__year=q) | Q(codecredit=q), Q(faites_par__admin__muso=current_user.muso) ).values('date_remb').order_by('-date_remb').annotate(sum=Sum('interet_remb')/qte_membre, sum2=Count('interet_remb'))
    else:
        qte_membre=Membre.objects.filter(membre_actif=1, admin__muso=current_user.muso).count()
        valeur2 = tbremboursement.objects.filter( faites_par__admin__muso=current_user.muso).values('date_remb').order_by('-date_remb').annotate(sum=Sum('interet_remb')/qte_membre, sum2=Count('interet_remb'))
        #all_remboursement_info = tbremboursement.objects.filter(faites_par__admin__muso = muso_id).select_related("tbcredit").values('codecredit_id').annotate(total=Count('codecredit_id'), sum=Sum('capital_remb')).order_by('-codecredit_id')
    paginator = Paginator(valeur2,15)
    page = request.GET.get('page')
    rembs = paginator.get_page(page)
    #qte_membre=Membre.objects.filter(membre_actif=1, admin__muso=current_user.muso | Q(date_remb__year=q) | Q(codecredit_id=q)).count()
    return render(request, "membre_template/Lesinterets_membre_ajoutes.html", { "valeur2":valeur2, "qte_membre":qte_membre })


def membre_apply_leave(request):
    current_user = request.user
    muso_id = current_user.muso
    membre_obj=Membre.objects.get(admin=request.user.id, admin__muso=current_user.muso)
    leave_data=LeaveReportMembre.objects.filter(code_membre=membre_obj)
    return render(request, "membre_template/membre_apply_leave.html", {"leave_data":leave_data})

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
    
    membre_id=Membre.objects.get(admin=request.user.id)
    feedback_data=FeedBackMembre.objects.filter(code_membre=membre_id)
    return render(request, "membre_template/membre_feedback.html", {"membre_data":feedback_data})

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
    user=CustomUser.objects.get(id=request.user.id)
    membre=Membre.objects.get(admin=user)
    return render(request,"membre_template/membre_profile.html",{"user":user, "membre":membre})

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
            #messages.error(request.traceback.format_exc())
            return HttpResponseRedirect(reverse("profile_mview"))
        
def profile_mview(request):
    current_user = request.user
    muso_id = current_user.muso
    # Logic for the profile view
    comments = Comment.objects.filter(author_id=F('author_id__id'), muso_id_id=muso_id).order_by('-created_at').values('id', 'text', 'created_at', 'author_id__nomp', 'author_id__prenomp')
    #comments = Comment.objects.filter(muso_id=muso_id).order_by('-created_at')
    return render(request, 'membre_template/commentaire.html', {'comments': comments})

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
    
    return render(request, 'membre_template/user_info.html', context)