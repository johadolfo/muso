from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
import traceback
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from g_muso_app.models import CustomUser, Membre, tbcotisation, tbcredit,tbremboursement,FeedBackMembre,LeaveReportMembre,CustomUser
from .forms import AddMembreForm, EditMembreForm
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.core.paginator import Paginator
from django.db.models import Max

def admin_home(request):
    membre_count=Membre.objects.all().count()
    cotisation_info=tbcotisation.objects.all()
    montant_tot = sum(cotisation_info.values_list('montant', flat=True))
    credit_info = tbcredit.objects.all()
    montant_credit = sum(credit_info.values_list('montant_credit', flat=True))
    remb_info = tbremboursement.objects.all()
    montant_rembourse = sum(remb_info.values_list('capital_remb', flat=True))
    #staff_count=Staffs.objects.all().count()
    # subject_count=Subjects.objects.all().count()
    # course_count=Courses.objects.all().count()

    # course_all=Courses.objects.all()
    # course_name_list=[]
    # subject_count_list=[]
    # student_count_list_in_course=[]
    # for course in course_all:
    #     subjects=Subjects.objects.filter(course_id=course.id).count()
    #     students=Students.objects.filter(course_id=course.id).count()
    #     course_name_list.append(course.course_name)
    #     subject_count_list.append(subjects)
    #     student_count_list_in_course.append(students)

    # subjects_all=Subjects.objects.all()
    # subject_list=[]
    # student_count_list_in_subject=[]
    # for subject in subjects_all:
    #     coure=Courses.objects.get(id=subject.course_id.id)
    #     student_course=Students.objects.filter(course_id=course.id).count()
    #     subject_list.append(subject.subject_name)
    #     student_count_list_in_subject.append(student_count)
    return render(request, "hod_template/home_content.html",{"membre_count":membre_count, "montant_tot":montant_tot, "montant_credit":montant_credit,"montant_rembourse":montant_rembourse })
    #return render(request, "hod_template/home_content.html", {"student_count":student_count,"staff_count":staff_count, "subject_count":subject_count, "course_count":course_count, "course_name_list":course_name_list, "subject_count_list":subject_count_list, "student_count_list_in_course":student_count_list_in_course,"student_count_list_in_subject":student_count_list_in_subject,"subject_list":subject_list})

def add_personne(request):
    pass

def add_membre(request):
    form = AddMembreForm()
    return render(request, "hod_template/add_membre_template.html",{"form":form})
   
# def add_membre_save(request):
#     form = MembreCreateForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#         messages.success(request, 'Successfully Saved')
#         return redirect('/liste_membre')
#     context = {
#         "form" : form,
#         "title" : "AJOUTER UN MEMBRE",
#     }
#     return HttpResponseRedirect(reverse("add_membre"))  
    #return render(request, "add_membre.html", context)

def add_membre_save(request):
    if request.method !="POST":
        return HttpResponse("Method Not Allowed")
    else:
        form=AddMembreForm(request.POST,request.FILES)
        if form.is_valid():
            prenomp = form.cleaned_data["prenomp"]
            nomp = form.cleaned_data["nomp"]
            codep = form.cleaned_data["codep"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            adressep = form.cleaned_data["adressep"]
            sexep = form.cleaned_data["sexep"]

            datenaissancep = form.cleaned_data["datenaissancep"]
            villep = form.cleaned_data["villep"]
            communep = form.cleaned_data["communep"]
            departementp = form.cleaned_data["departementp"]
            paysp = form.cleaned_data["paysp"]
            nifp = form.cleaned_data["nifp"]

            telephone1p = form.cleaned_data["telephone1p"]
            telephone2p = form.cleaned_data["telephone2p"]
            activiteprofessionp = form.cleaned_data["activiteprofessionp"]
            referencep = form.cleaned_data["referencep"]
            lieunaissancep = form.cleaned_data["lieunaissancep"]
        
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)

            try:
                user=CustomUser.objects.create_user(username=prenomp +' '+ nomp, password=password, email=email, last_name=nomp, first_name=prenomp, user_type=2)
                # user.save()
                # user_id = CustomUser.objects.all()
                # #admin_id = max(user_id.values_list('id', flat=True))
                # #CustomUser.objects.order_by('id').first()
                # membre = Membre(CustomUser.objects.aggregate(Max('id')), codep=codep, nomp=nomp, prenomp=prenomp, sexep=sexep, datenaissancep=datenaissancep,lieunaissancep=lieunaissancep, adressep=adressep, villep=villep,communep=communep, departementp=departementp,paysp=paysp, nifp=nifp,telephone1p=telephone1p, telephone2p=telephone2p,activiteprofessionp=activiteprofessionp, referencep=referencep, profile_pic=profile_pic_url)
                # membre.save()
                user.membre.codep=codep
                user.membre.nomp = nomp
                user.membre.prenomp=prenomp
                user.membre.sexep = sexep
                user.membre.datenaissancep = datenaissancep
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
                user.save()
           
                messages.success(request,"Successfully Added Membre")
                return HttpResponseRedirect(reverse("add_membre")) 
            except Exception as e:
                    #messages=traceback.format_exc()
                messages.error(request,traceback.format_exc())
                #messages.error(request,type(e))
                    #messages.error(request,"Failed to Add Staff")
                return HttpResponseRedirect(reverse("add_membre"))
        else:
            form.AddMembreForm(request.POST)
            return render("hod_template/add_membre_template.html", {"form":form})


def add_cotisation(request):
    cotisations = tbcotisation.objects.all()
    membre_info = Membre.objects.all()
    membres = CustomUser.objects.filter(user_type=2)
    return render(request, "hod_template/add_cotisation_template.html", {"membres":membres, "cotisations":cotisations, "membre_info":membre_info})

def add_cotisation_save(request):
  
    if request.method !="POST":
        return HttpResponse("Method Not Allowed")
    else:
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
            return HttpResponseRedirect(reverse("add_cotisation")) 
        except Exception as e:
            messages.error(request,traceback.format_exc())
            return HttpResponseRedirect(reverse("add_cotisation"))
        # except:
        #     messages.error(request,"Failed to Add cotisation")
        #     return HttpResponseRedirect(reverse("add_cotisation")) 

def add_credit(request):
    credits = tbcredit.objects.all()
    membre_info = Membre.objects.all()
    membres = CustomUser.objects.filter(user_type=2)
    return render(request, "hod_template/add_credit_template.html", {"membres":membres, "credits":credits, "membre_info":membre_info})

def add_credit_save(request):
    if request.method !="POST":
        return HttpResponse("Method Not Allowed")
    else:
        code_membres = request.POST.get("membre")
        code_membre=Membre.objects.get(id=code_membres)
        #cotisation.code_membre=code_membre
        numero_credit = request.POST.get("numero")
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
    remboursements = tbremboursement.objects.all()
    credits=tbcredit.objects.all()
    membre_info = Membre.objects.all()
    membres = CustomUser.objects.filter(user_type=2)
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
            messages.success(request,"Successfully Added remboursement")
            return HttpResponseRedirect(reverse("add_remboursement")) 
        except Exception as e:
            messages.error(request,traceback.format_exc())
            return HttpResponseRedirect(reverse("add_remboursement"))

def manage_membre(request):
    membres = Membre.objects.all()
    return render(request, "hod_template/manage_membre_template.html", { "membres": membres })

def manage_cotisation(request):
    cotisations = tbcotisation.objects.all()

    if 'q' in request.GET:
        q = request.GET['q']
        all_cotisation_list = tbcotisation.objects.filter( Q(typecotisation__icontains=q) | Q(date_fait__icontains=q))
    else:
        all_cotisation_list = tbcotisation.objects.all()
    paginator = Paginator(all_cotisation_list,5)
    page = request.GET.get('page')
    cotisations = paginator.get_page(page)
    return render(request, "hod_template/manage_cotisation_template.html", { "cotisations":cotisations })

def manage_credit(request):
    credits = tbcredit.objects.all()
    return render(request, "hod_template/manage_credit_template.html", { "credits":credits })

def manage_remboursement(request):
    rembs = tbremboursement.objects.all()
    return render(request, "hod_template/manage_remboursement_template.html", { "rembs":rembs })

def edit_membre(request, membre_id):
    request.session['membre_id']=membre_id
    membre_info=Membre.objects.get(admin=membre_id)
    form=AddMembreForm()
   
    form.fields['prenomp'].initial=membre_info.admin.first_name
    form.fields['nomp'].initial=membre_info.admin.last_name
    form.fields['codep'].initial=membre_info.codep
    form.fields['sexep'].initial=membre_info.sexep

    form.fields['datenaissancep'].initial=membre_info.datenaissancep
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
            nomp=form.cleaned_data["nomp"]
            codep=form.cleaned_data["codep"]
            # email=form.cleaned_data["email"]
            # password=form.cleaned_data["password"]
            adressep=form.cleaned_data["adressep"]
            sexep = form.cleaned_data["sexep"]

            datenaissancep=form.cleaned_data["datenaissancep"]
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
            else:
                profile_pic_url = None

            try:
                user=CustomUser.objects.get(id=membre_id)
                user.first_name = prenomp
                user.last_name = nomp
                # user.username = username
                # user.email=email
                user.save()

                membre=Membre.objects.get(admin=membre_id)
                membre.adressep=adressep
                membre.sexep = sexep
                membre.codep=codep
                membre.nomp = nomp
                membre.prenomp=prenomp
                membre.datenaissancep = datenaissancep
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
    membre_info = Membre.objects.all()
    remboursements = tbremboursement.objects.get(id=remboursement_id)
    membres = CustomUser.objects.filter(user_type=2)
    return render(request, "hod_template/edit_remboursement_template.html", {"remboursements":remboursements, "membres":membres,"membre_info":membre_info})

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



def manage_session(request):
    return render(request, "hod_template/manage_session_template.html")

def add_session_save(request):
    if request.method !="POST":
        return HttpResponseRedirect(reverse("manage_session"))
    else:
        session_start_year = request.POST.get("session_start")
        session_end_year = request.POST.get("session_end")
        try:
            sessionyear=SessionYearModel(session_start_year=session_start_year, session_end_year=session_end_year)
            sessionyear.save()
            messages.success(request,"Successfully Added Session")
            return HttpResponseRedirect(reverse("manage_session"))
        except:
            messages.error(request,traceback.format_exc())
            return HttpResponseRedirect(reverse("manage_session"))

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

# @csrf_exempt
# def check_codecredit_exist(request):
#     codecredit=request.POST.get("numero_credit")
#     user_obj=tbcredit.objects.filter(numero=codecredit).exists()
#     if user_obj:
#         return HttpResponse(True)

#     else:
#         return HttpResponse(False)



def membre_feedback_message(request):
    feedbacks=FeedBackMembre.objects.all()
    return render(request, "hod_template/membre_feedback_template.html", {"feedbacks":feedbacks})

@csrf_exempt
def membre_feedback_message_replied(request):
    feedback_id=request.POST.get("id")
    feedback_message=request.POST.get("message")
    try:
        feedback=FeedBackMembre.objects,get(id=feedback_id)
        feedback.feedback_reply=feedback_message
        feedback.save()
        return HttpResponse(True)
    except:
        return HttpResponse(False)



def membre_leave_view(request):
    leaves =LeaveReportMembre.objects.all()
    return render(request, "hod_template/membre_leave_view.html",{"leaves":leaves})

def membre_approve_leave(request, leave_id):
    leave=LeaveReportMembre.objects.get(id=leave_id)
    leave.leave_status=1
    leave.save()
    return HttpResponseRedirect(reverse("membre_leave_view"))

def membre_disapprove_leave(request, leave_id):
    #return HttpResponse("ID : "+leave_id)
    leave=LeaveReportMembre.objects.get(id=leave_id)
    leave.leave_status=2
    leave.save()
    return HttpResponseRedirect(reverse("membre_leave_view"))

## on termine dans la video 18 (10:37)

def admin_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
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
        if password!= None and password !="":
            customuser.set_password(password)
        customuser.save()
        messages.success(request,"Successfully Update Profile")
        return HttpResponseRedirect(reverse("admin_profile"))
    except:
        messages.success(request,"Failed Update Profile")
        return HttpResponseRedirect(reverse("admin_profile"))

# class MembreAdmin(admin.ModelAdmin):
#     list_display=['Prenom', 'Nom', 'Adresse', 'Telephone', 'Reference']
#     search_fields = ['nomp', 'prenomp', 'codep', 'telephone1p']
#     list_filter = ['gender']
#     list_per_page = 2


def backend(request):
    if 'q' in request.GET:
        q = request.GET['q']
        all_membre_list = Membre.objects.filter(
            Q(nomp_incontains=q | Q(prenomp_incontains=q) | Q(codep_incontains=q) | Q(telephone1p_incontains=q))
        )
    else:
        all_membre_list = Membre.objects.all()
    paginator = Paginator(all_membre_list,5)
    page = request.GET.get('page')
    membres = paginator.get_page(page)

    return render(request, "hod_template/manage_membre_template.html", {"membres":membres})