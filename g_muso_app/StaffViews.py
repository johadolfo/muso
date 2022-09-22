from django.shortcuts import render
from g_muso_app.models import CustomUser
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.contrib import messages
import traceback

def staff_home(request):
    pass
    # #For Fetch All Student Under Staff
    # subjects=Subjects.objects.filter(staff_id=request.user.id)
    # course_id_list=[]
    # for subject in subjects:
    #     course=Courses.objects.get(id=subject.course_id.id)
    #     course_id_list.append(course.id)
    
    # final_course=[]
    # #removing Duplicate Course ID
    # for course_id in course_id_list:
    #     if course_id not in final_course:
    #         final_course.append(course_id)

    # students_count=Students.objects.filter(course_id__in=final_course).count()

    # #Fetch All Attendance Count
    # attendance_count=Attendance.objects.filter(subject_id__in=subjects).count()

    # #Fetch All Approve leave
    # staff=Staffs.objects.get(admin=request.user.id)
    # leave_count=LeaveReportStaff.objects.filter(staff_id=staff.id, leave_status=1).count()
    # subject_count=subjects.count()

    # #fetch attendance data by subject
    # subject_list=[]
    # attendance_list=[]
    # for subject in subjects:
    #     attendaance_count1=Attendance.objects.filter(subject_id=subject.id).count()
    #     subject_list.append(subject.subject_name)
    #     attendance_list.append(attendaance_count1)
    # return render(request, "staff_template/staff_home_template.html", {"students_count":students_count, "attendance_count":attendance_count, "leave_count":leave_count, "subject_count":subject_count, "subject_list":subject_list, "attendance_list":attendance_list})

def staff_take_attendance(request):
    pass
#     subjects=Subjects.objects.filter(staff_id=request.user.id)
#     session_years=SessionYearModel.objects.all()
#     return render(request, "staff_template/staff_take_attendance.html",{"subjects":subjects, "session_years":session_years})
# # la video partie 21, ne se termine pas, on arive a 12:24.

@csrf_exempt
def get_students(request):
    pass
    # subject_id = request_POST.get("subject")
    # session_year = request.POST.get("session_year")
    # subject=Subjects.objects.get(id=subject_id)
    # session_model = SessionYearModel.object.get(id=session_year)
    # students=Students.onjects.filter(course_id=subject.course_id,session_year_id=session_model)
    
    # student_date=serializers.serialize("python", students)
    # list_data=[]

    # for student in students:
    #     data_small={"id":student.admin.id,"name":student.admin.first_name+" "+student.admin.last_name}
    #     list_data.append(data_small)
    # return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False) 

def staff_apply_leave(request):
    pass
    # staff_obj=Staffs.objects.get(admin=request.user.id)
    # leave_data=LeaveReportStaff.objects.filter(staff_id=staff_obj)
    # return render(request, "staff_template/staff_apply_leave.html", {"leave_data":leave_data})

def staff_apply_leave_save(request):
    pass
    # if request.method!="POST":
    #     return HttpResponseRedirect(reverse("staff_apply_leave"))
    # else:
    #     leave_date=request.POST.get("leave_date")
    #     leave_msg=request.POST.get("leave_msg")

    #     staff_obj=Staffs.objects.get(admin=request.user.id)
    #     try:
    #         leave_report=LeaveReportStaff(staff_id=staff_obj, leave_date=leave_date,leave_message=leave_msg,leave_status=0)
    #         leave_report.save()
    #         messages.success(request,"Successfully Applied for Leave")
    #         return HttpResponseRedirect(reverse("staff_apply_leave")) 
    #     except Exception as e:
    #         messages.error(request,traceback.format_exc())
    #         return HttpResponseRedirect(reverse("staff_apply_leave"))


def staff_feedback(request):
    pass
    # staff_id=Staffs.objects.get(admin=request.user.id)
    # feedback_data=FeedBackStaffs.objects.filter(staff_id=staff_id)
    # return render(request, "staff_template/staff_feedback.html", {"feedback_data":feedback_data})

def staff_feedback_save(request):
    pass
    # if request.method!="POST":
    #     return HttpResponseRedirect(reverse("staff_feedback_save"))
    # else:
    #     feedback_msg=request.POST.get("feedback_msg")
    #     staff_obj=Staffs.objects.get(admin=request.user.id)
    #     try:
    #         feedback=FeedBackStaffs(staff_id=staff_obj, feedback=feedback_msg, feedback_reply="")
    #         feedback.save()
    #         messages.success(request,"Successfully Sent Feedback")
    #         return HttpResponseRedirect(reverse("staff_feedback")) 
    #     except Exception as e:
    #         messages.error(request,traceback.format_exc())
    #         return HttpResponseRedirect(reverse("staff_feedback"))
        
def staff_profile(request):
    pass
    # user=CustomUser.objects.get(id=request.user.id)
    # staff=Staffs.objects.get(admin=user)
    # return render(request,"staff_template/staff_profile.html",{"user":user, "staff":staff})

def staff_profile_save(request):
    pass
    # if request.method!="POST":
    #     return HttpResponseRedirect(reverse("staff_profile"))
    # else:
    #     first_name = request.POST.get("first_name")
    #     last_name = request.POST.get("last_name")
    #     adress=request.POST.get("adress")
    #     password = request.POST.get("password")
    # try:
    #     customuser=CustomUser.objects.get(id=request.user.id)
    #     customuser.first_name=first_name
    #     customuser.last_name=last_name
    #     if password!= None and password !="":
    #         customuser.set_password(password)
    #     customuser.save()

    #     staff=Staffs.objects.get(admin=customuser.id)
    #     staff.adress=adress
    #     staff.save()
    #     messages.success(request,"Successfully Update Profile")
    #     return HttpResponseRedirect(reverse("staff_profile"))
    # except:
    #     messages.success(request,"Failed Update Profile")
    #     return HttpResponseRedirect(reverse("staff_profile"))