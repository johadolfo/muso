from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib import messages
from g_muso_app.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from g_muso_app.models import  Membre

from g_muso_app.models import tbmuso


# Create your views here.
def showDemoPage(request):
    return render(request, "demo.html")
#def home(request):
    #return render(request, "site_johnado/index.html")
    
def ShowLoginPage(request):
    return render(request, "login_page.html")

#def login(request):
    #return render(request, "site_johnado/login_page.html")



def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get("email"), password=request.POST.get("password"))
        if user is not None:
            membre_actif = Membre.objects.filter(admin_id=user.id, membre_actif=1)
            if membre_actif.exists():
                login(request, user)
                if user.user_type == "1":
                    return HttpResponseRedirect('/admin_home')
                elif user.user_type == "3":
                    return HttpResponseRedirect(reverse("adm_home"))
                elif user.user_type == "2":
                    return HttpResponseRedirect(reverse("membre_home"))
            else:
                login(request, user)
                if user.user_type == "1":
                    return HttpResponseRedirect('/admin_home')
                elif user.user_type == "3":
                    return HttpResponseRedirect(reverse("adm_home"))

        messages.error(request, "Invalid Login Details")
        return HttpResponseRedirect("/")
    
'''def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get("email"), password=request.POST.get("password"))
        membre_actif = Membre.objects.filter(admin_id=user.id, membre_actif=1)
        if user is not None and membre_actif.exists():
            login(request, user)
            if user.user_type == "1":
                return HttpResponseRedirect('/admin_home')
            elif user.user_type == "3":
                return HttpResponseRedirect(reverse("adm_home"))
            elif user.user_type == "2":
                return HttpResponseRedirect(reverse("membre_home"))
        else:
            messages.error(request, "Invalid Login Details")
            return HttpResponseRedirect("/")
    muso_use = Membre.objects.filter(id=user.id)'''

'''def doLogin(request):
    if request.method!="POST":
        return HttpResponse("<h2> Methode Not Allowed </h2)")
    else:
        user=EmailBackEnd.authenticate(request, username=request.POST.get("email"), password=request.POST.get("password"))
        membre_actif = Membre.objects.filter(admin_id=request.user.id, membre_actif=1)
        if user!=None and membre_actif!=None:
            login(request,user)
            if user.user_type=="1":
                #muso_use = request.POST.get("muso")
                #muso_use = Membre.object.filter(id=user.id)
                return HttpResponseRedirect('/admin_home')
            elif user.user_type=="3":
                #muso_use = request.POST.get("muso")
                return HttpResponseRedirect(reverse("adm_home"))
            elif user.user_type=="2":
                #muso_use = request.POST.get("muso")
                return HttpResponseRedirect(reverse("membre_home"))
            #return HttpResponse("Email : "+request.POST.get("email")+" Password : "+request.POST.get("password"))
        else:
            messages.error(request, "Invalid Login Details")
            return HttpResponseRedirect("/")
    muso_use = Membre.objects.filter(id=user.id)'''


def GetUserDetails(request):
    if request.use!=None:
        return HttpResponse("User : "+request.user.email+" usertype : "+request.user.user_type)
    else:
        return HttpResponse("Please Login First")

def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")
