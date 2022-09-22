"""student_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from g_muso_app import views, HodViews, MembreViews, StaffViews, StudentViews
from g_muso import settings

urlpatterns = [
    path('demo', views.showDemoPage),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.ShowLoginPage, name="show_login"),
    path('get_user_details', views.GetUserDetails),
    path('logout_user', views.logout_user, name="logout"),
    path('doLogin', views.doLogin, name="do_login"),
    path('admin_home', HodViews.admin_home, name="admin_home"),
    path('add_membre', HodViews.add_membre, name="add_membre"),
    path('add_personne', HodViews.add_membre, name="add_personne"),
    path('add_membre_save', HodViews.add_membre_save, name="add_membre_save"),
    path('add_cotisation', HodViews.add_cotisation, name="add_cotisation"),
    path('add_cotisation_save', HodViews.add_cotisation_save, name="add_cotisation_save"),
    path('add_credit', HodViews.add_credit, name="add_credit"),
    path('add_credit_save', HodViews.add_credit_save, name="add_credit_save"),
    path('add_remboursement', HodViews.add_remboursement, name="add_remboursement"),
    path('add_remboursement_save', HodViews.add_remboursement_save, name="add_remboursement_save"),
    path('manage_membre', HodViews.manage_membre, name="manage_membre"),
     path('backend', HodViews.backend, name="backend"),
    path('manage_cotisation', HodViews.manage_cotisation, name="manage_cotisation"),
    path('manage_credit', HodViews.manage_credit, name="manage_credit"),
    path('manage_remboursement', HodViews.manage_remboursement, name="manage_remboursement"),

    path('edit_membre/<str:membre_id>', HodViews.edit_membre, name="edit_membre"),
    path('edit_membre_save', HodViews.edit_membre_save, name="edit_membre_save"),
    path('edit_cotisation/<str:cotisation_id>', HodViews.edit_cotisation, name="edit_cotisation"),
    path('edit_cotisation_save', HodViews.edit_cotisation_save, name="edit_cotisation_save"),
    path('edit_credit/<str:credit_id>', HodViews.edit_credit, name="edit_credit"),
    path('edit_credit_save', HodViews.edit_credit_save, name="edit_credit_save"),
    path('edit_remboursement/<str:remboursement_id>', HodViews.edit_remboursement, name="edit_remboursement"),
    path('edit_remboursement_save', HodViews.edit_remboursement_save, name="edit_remboursement_save"),
    
    path('manage_session', HodViews.manage_session, name="manage_session"),
    path('add_session_save', HodViews.add_session_save, name="add_session_save"),
    path('check_email_exist', HodViews.check_email_exist, name="check_email_exist"),
    path('check_codep_exist', HodViews.check_codep_exist, name="check_codep_exist"),
    path('membre_feedback_message', HodViews.membre_feedback_message, name="membre_feedback_message"),
    path('membre_feedback_message_replied', HodViews.membre_feedback_message_replied, name="membre_feedback_message_replied"),
   
    path('membre_leave_view', HodViews.membre_leave_view, name="membre_leave_view"),
    
    path('membre_approve_leave/<str:leave_id>', HodViews.membre_approve_leave, name="membre_approve_leave"),
    path('membre_disapprove_leave/<str:leave_id>', HodViews.membre_disapprove_leave, name="membre_disapprove_leave"),
    
    
    path('admin_profile', HodViews.admin_profile, name="admin_profile"),
    path('admin_profile_save', HodViews.admin_profile_save, name="admin_profile_save"),
  

    path('membre_home', MembreViews.membre_home, name="membre_home"),
    path('student_view_attendance', StudentViews.student_view_attendance, name="student_view_attendance"),
    path('student_view_attendance_post', StudentViews.student_view_attendance_post, name="student_view_attendance_post"),
    path('membre_apply_leave', MembreViews.membre_apply_leave, name="membre_apply_leave"),
    path('membre_apply_leave_save', MembreViews.membre_apply_leave_save, name="membre_apply_leave_save"),
    path('membre_feedback', MembreViews.membre_feedback, name="membre_feedback"),
    path('membre_feedback_save', MembreViews.membre_feedback_save, name="membre_feedback_save"),
    path('membre_profile', MembreViews.membre_profile, name="membre_profile"),
    path('membre_profile_save', MembreViews.membre_profile_save, name="membre_profile_save"),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
