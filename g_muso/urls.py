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
from g_muso_app import views, HodViews, MembreViews, ADMViews
from g_muso import settings

urlpatterns = [

    path('demo', views.showDemoPage),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.ShowLoginPage, name="show_login"),
    path('get_user_details', views.GetUserDetails),
    path('logout_user', views.logout_user, name="logout"),
    path('doLogin', views.doLogin, name="do_login"),

    #adm home
    path('manage_user', ADMViews.manage_user, name="manage_user"),
    path('add_muso', ADMViews.add_muso, name="add_muso"),
    path('add_muso_save', ADMViews.add_muso_save, name="add_muso_save"),
    path('manage_muso', ADMViews.manage_muso, name="manage_muso"),
    path('adm_home', ADMViews.adm_home, name="adm_home"),
    path('edit_muso/<str:muso_id>', ADMViews.edit_muso, name="edit_muso"),
    path('edit_muso_save', ADMViews.edit_muso_save, name="edit_muso_save"),
    path('edit_user/<str:user_id>', ADMViews.edit_user, name="edit_user"),
    path('edit_user_save', ADMViews.edit_user_save, name="edit_user_save"),
    path('export_csv',ADMViews.export_csv, name="export_csv"),
    path('export_users_csv',ADMViews.export_users_csv, name="export_users_csv"),
    path('add_new_user',ADMViews.add_new_user, name="add_new_user"),
    path('add_customuser_save',ADMViews.add_customuser_save, name="add_customuser_save"),
    path('show_aceess',ADMViews.show_aceess, name="show_aceess"),
    path('load_more_data',ADMViews.load_more_data, name="load_more_data"),

    #admin home
    path('admin_home', HodViews.admin_home, name="admin_home"),
    path('add_membre', HodViews.add_membre, name="add_membre"),
    path('add_personne', HodViews.add_membre, name="add_personne"),
    path('add_membre_save', HodViews.add_membre_save, name="add_membre_save"),
    path('add_tbcotisation', HodViews.add_tbcotisation, name="add_tbcotisation"),
    path('add_cotisation_save', HodViews.add_cotisation_save, name="add_cotisation_save"),
    path('add_cotisationnouveauMEMBRE_save', HodViews.add_cotisationnouveauMEMBRE_save, name="add_cotisationnouveauMEMBRE_save"),
    path('add_cotisationRemplacerMEMBRE_save', HodViews.add_cotisationRemplacerMEMBRE_save, name="add_cotisationRemplacerMEMBRE_save"),
    path('add_credit', HodViews.add_credit, name="add_credit"),
    path('add_credit_save', HodViews.add_credit_save, name="add_credit_save"),
    path('CalculateurPretView', HodViews.CalculateurPretView, name="CalculateurPretView"),
    path('add_remboursement', HodViews.add_remboursement, name="add_remboursement"),
    path('add_remboursement_save', HodViews.add_remboursement_save, name="add_remboursement_save"),
    path('add_detailalimentaire', HodViews.add_detailalimentaire, name="add_detailalimentaire"),
    path('add_detailalimentaire_save', HodViews.add_detailalimentaire_save, name="add_detailalimentaire_save"),
    path('get_credit_data', HodViews.get_credit_data, name="get_credit_data"),
    path('get_credit_info', HodViews.get_credit_info, name="get_credit_info"),
    path('manage_membre', HodViews.manage_membre, name="manage_membre"),
    path('view_tbcotisation', HodViews.view_tbcotisation, name="view_tbcotisation"),
    path('manage_credit', HodViews.manage_credit, name="manage_credit"),
    path('liste_credit_encour', HodViews.liste_credit_encour, name="liste_credit_encour"),
    path('manage_creditalimentaire', HodViews.manage_creditalimentaire, name="manage_creditalimentaire"),
    path('comiteSMS_feedback', HodViews.comiteSMS_feedback, name="comiteSMS_feedback"),
    path('comiteSMS_feedback_save', HodViews.comiteSMS_feedback_save, name="comiteSMS_feedback_save"),
    path('manage_detailalimentaire', HodViews.manage_detailalimentaire, name='manage_detailalimentaire'),

    path('manage_remboursement', HodViews.manage_remboursement, name="manage_remboursement"),
    path('liste_credit', HodViews.liste_credit, name="liste_credit"),
    path('edit_membre/<str:membre_id>', HodViews.edit_membre, name="edit_membre"),
    path('edit_membre_save', HodViews.edit_membre_save, name="edit_membre_save"),
    path('edit_cotisation/<str:cotisation_id>', HodViews.edit_cotisation, name="edit_cotisation"),
    path('edit_cotisation_save', HodViews.edit_cotisation_save, name="edit_cotisation_save"),
    path('edit_credit/<str:credit_id>', HodViews.edit_credit, name="edit_credit"),
    path('edit_credit_save', HodViews.edit_credit_save, name="edit_credit_save"),
    path('edit_remboursement/<str:remboursement_id>', HodViews.edit_remboursement, name="edit_remboursement"),
    path('edit_remboursement_save', HodViews.edit_remboursement_save, name="edit_remboursement_save"),
    path('edit_detailproduct/<str:detailproduct_id>', HodViews.edit_detailproduct, name="edit_detailproduct"),
    path('edit_detailproduct_save', HodViews.edit_detailproduct_save, name="edit_detailproduct_save"),

    #path('edit_tbmuso', HodViews.edit_tbmuso, name="edit_tbmuso"),
    #path('edit_tbmuso_save<int:tbmuso_id>/', HodViews.edit_tbmuso_save, name='edit_tbmuso_save'),

    path('edit_muso', HodViews.edit_muso, name="edit_muso"),
    path('edit_muso_save', HodViews.edit_muso_save, name="edit_muso_save"),

    path('check_email_exist', HodViews.check_email_exist, name="check_email_exist"),
    path('check_codep_exist', HodViews.check_codep_exist, name="check_codep_exist"),
    path('membre_feedback_message', HodViews.membre_feedback_message, name="membre_feedback_message"),
    path('membre_feedback_message_replied', HodViews.membre_feedback_message_replied, name="membre_feedback_message_replied"),
    path('statistique_cotisation', HodViews.statistique_cotisation, name="statistique_cotisation"),
    path('statistique_remboursement', HodViews.statistique_remboursement, name="statistique_remboursement"),
    path('statistique_credit', HodViews.statistique_credit, name="statistique_credit"),
    path('interets_ajoutes', HodViews.interets_ajoutes, name="interets_ajoutes"),
    path('membre_leave_view', HodViews.membre_leave_view, name="membre_leave_view"),
    path('membre_approve_leave/<str:leave_id>', HodViews.membre_approve_leave, name="membre_approve_leave"),
    path('membre_disapprove_leave/<str:leave_id>', HodViews.membre_disapprove_leave, name="membre_disapprove_leave"),

    path('admin_profile', HodViews.admin_profile, name="admin_profile"),
    path('admin_profile_save', HodViews.admin_profile_save, name="admin_profile_save"),

    path('add_depense', HodViews.add_depense, name="add_depense"),
    path('add_depense_save', HodViews.add_depense_save, name="add_depense_save"),
    path('manage_depense', HodViews.manage_depense, name="manage_depense"),
    path('edit_depense/<str:depense_id>', HodViews.edit_depense, name="edit_depense"),
    path('edit_depense_save', HodViews.edit_depense_save, name="edit_depense_save"),
    #export des donnees
    path('export_membres_csv', HodViews.export_membres_csv, name="export_membres_csv"),
    path('export_cotisation_csv',HodViews.export_cotisation_csv, name="export_cotisation_csv"),
    path('export_credit_csv',HodViews.export_credit_csv, name="export_credit_csv"),
    path('export_remboursement_csv', HodViews.export_remboursement_csv, name="export_remboursement_csv"),
    path('export_depense_csv',HodViews.export_depense_csv, name="export_depense_csv"),
    path('export_detailalimentaire_csv',HodViews.export_detailalimentaire_csv, name="export_detailalimentaire_csv"),
    path('export_statistique_cotisation_csv',HodViews.export_statistique_cotisation_csv, name="export_statistique_cotisation_csv"),
    path('export_statistique_remboursement_csv',HodViews.export_statistique_remboursement_csv, name="export_statistique_remboursement_csv"),
    path('export_statistique_credit_csv',HodViews.export_statistique_credit_csv, name="export_statistique_credit_csv"),
    path('export_detailcredit_csv',HodViews.export_detailcredit_csv, name="export_detailcredit_csv"),
    
    #import des donnees
    path('import_datadepense_csv', HodViews.import_datadepense_csv, name="import_datadepense_csv"),

    #path('add_comments', HodViews.add_comments, name="add_comments"),
    path('add_comments_save', HodViews.add_comments_save, name="add_comments_save"),
    path('profile_view', HodViews.profile_view, name="profile_view"),
    path('user_info', HodViews.user_info, name="user_info"),
    path('user_access', HodViews.user_access, name="user_access"),
    path('user_groups', HodViews.user_groups, name="user_groups"),
    

    #membre home
    path('membre_home', MembreViews.membre_home, name="membre_home"),
    path('membre_cotisation', MembreViews.membre_cotisation, name="membre_cotisation"),
    path('membre_remboursement', MembreViews.membre_remboursement, name="membre_remboursement"),
    path('membre_credit', MembreViews.membre_credit, name="membre_credit"),
    path('Lesinterets_membre_ajoutes', MembreViews.Lesinterets_membre_ajoutes, name="Lesinterets_membre_ajoutes"),
    path('membre_apply_leave', MembreViews.membre_apply_leave, name="membre_apply_leave"),
    path('membre_apply_leave_save', MembreViews.membre_apply_leave_save, name="membre_apply_leave_save"),
    path('membre_feedback', MembreViews.membre_feedback, name="membre_feedback"),
    path('membre_feedback_save', MembreViews.membre_feedback_save, name="membre_feedback_save"),
    path('membre_profile', MembreViews.membre_profile, name="membre_profile"),
    path('membre_profile_save', MembreViews.membre_profile_save, name="membre_profile_save"),

   

    path('add_mcomments_save', MembreViews.add_mcomments_save, name="add_mcomments_save"),
    path('profile_mview', MembreViews.profile_mview, name="profile_mview"),
    path('user_info', MembreViews.user_info, name="user_info"),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


