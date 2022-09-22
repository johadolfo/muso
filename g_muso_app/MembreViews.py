from django.shortcuts import render
from g_muso_app.models import  CustomUser, Membre,FeedBackMembre,LeaveReportMembre, tbcotisation, tbcredit, tbremboursement
from django.http import HttpResponse
import datetime
from django.urls import reverse
from django.contrib import messages
import traceback
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect

def membre_home(request):
   
    membre_obj=Membre.objects.get(admin=request.user.id)
    cotisation_inf=tbcotisation.objects.filter(code_membre=membre_obj)
    montant_total  = sum(cotisation_inf.values_list('montant', flat=True))
    montant_penalite  = sum(cotisation_inf.values_list('penalite', flat=True))
    montant_interet  = sum(cotisation_inf.values_list('interet', flat=True))

    credit_info =tbcredit.objects.filter(code_membre=membre_obj, credit_status="En cour")
    montant_credit = sum(credit_info.values_list('montant_credit', flat=True))

    #remboursement_info =tbremboursement.objects.filter(code_membre=membre_obj, codecredit_id=credit_info.numero)
    #remboursement_du = montant_credit -(sum(remboursement_info.values_list('capital_remb', flat=True)) + sum(remboursement_info.values_list('interet_remb', flat=True)))
    # attendance_present=AttendanceReport.objects.filter(student_id=student_obj, status=True).count()
    # attendance_absent=AttendanceReport.objects.filter(student_id=student_obj, status=False).count()
    # course=Courses.objects.get(id=student_obj.course_id.id)
    # subjects=Subjects.objects.filter(course_id=course).count()

    # subject_name=[]
    # data_present=[]
    # data_absent=[]
    # subject_data=Subjects.objects.filter(course_id=student_obj.course_id)
    # for subject in subject_data:
    #     attendance=Attendance.objects.filter(subject_id=subject.id)
    #     attendance_present_count=AttendanceReport.objects.filter(attendance_id__in=attendance, status=True, student_id=student_obj.id).count()
    #     attendance_absent_count=AttendanceReport.objects.filter(attendance_id__in=attendance, status=False, student_id=student_obj.id).count()
    #     subject_name.append(subject.subject_name)
    #     data_present.append(attendance_present_count)
    #     data_absent.append(attendance_absent_count)

    #return render(request, "student_template/student_home_template.html",{"attendance_total":attendance_total, "attendance_present":attendance_present, "attendance_absent":attendance_absent, "subjects":subjects, "data_name":subject_name, "data1":data_present, "data2":data_absent})
    return render(request, "membre_template/membre_home_template.html",{"montant_total":montant_total,"montant_penalite":montant_penalite, "montant_interet":montant_interet, "montant_credit":montant_credit })


def membre_apply_leave(request):
    membre_obj=Membre.objects.get(admin=request.user.id)
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
        adress=request.POST.get("adress")
        username=request.POST.get("username")
    try:
        customuser=CustomUser.objects.get(id=request.user.id)
        customuser.first_name=first_name
        customuser.set_username(username)
        customuser.last_name=last_name
        if password!= None and password !="":
            customuser.set_password(password)
        customuser.save()

        membre=Membre.objects.get(admin=customuser.id)
        membre.save()
        messages.success(request,"Successfully Update Profile")
        return HttpResponseRedirect(reverse("membre_profile"))
    except:
        messages.success(request,"Failed Update Profile")
        return HttpResponseRedirect(reverse("membre_profile"))