from django import forms

from g_muso_app.models import CustomUser

class DateInput(forms.DateInput):
    input_type = "date"

class AddMembreForm(forms.Form):
    gender_choice=(
        ("Masculin", "Masculin"),
        ("Feminin", "Feminin")
    )
    email=forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control", "autocomplete":"off"}))
    password=forms.CharField(label="Password", max_length=50, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    codep =  forms.CharField(label="CODE MEMBRE ",max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    prenomp=forms.CharField(label="Prenom", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    nomp=forms.CharField(label="Nom", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    sexep=forms.ChoiceField(label="Sexe", choices=gender_choice, widget=forms.Select(attrs={"class":"form-control"}))
    datenaissancep =  forms.DateField(label="DATE DE NAISSANCE (YYYY-MM-DD)", widget=DateInput(format=('%d/%m/%Y'),attrs={"class":"form-control"}),initial="2022-08-22")
    lieunaissancep=forms.CharField(label="Lieu de Naissance", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}),initial="Zone1")
    adressep=forms.CharField(label="Adresse", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}),initial="07,Santo 9 prolonge")
    villep =  forms.CharField(label="VILLE ",max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}), initial="Port-au-Prince")
    communep =  forms.CharField(label="COMMUNE ",max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}),initial="Croix-des-Bouquets")
    departementp =  forms.CharField(label="DEPARTEMENT ",max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}), initial="OUEST")
    paysp =  forms.CharField(label="PAYS ",max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}),initial="HAITI")
    nifp =  forms.CharField(label="NIF/CIN ",max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}),initial="00-00-000-0")
    telephone1p =  forms.CharField(label="TELEPHONE 1 ",max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}),initial="0000-0000")
    telephone2p =  forms.CharField(label="TELEPHONE 2 ",max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}), initial="0000-0000")
    activiteprofessionp =  forms.CharField(label="ACTIVITE / PROFESSION ",max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}),initial="Biznisman")
    referencep =  forms.CharField(label="REFERENCE ",max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}), initial="President")
    profile_pic=forms.FileField(label="Profile Pic", max_length=50, widget=forms.FileInput(attrs={"class":"form-control"}))


class EditMembreForm(forms.Form):
    gender_choice=(
        ("Masculin", "Masculin"),
        ("Feminin", "Feminin")
    )
    
    codep =  forms.CharField(label="CODE MEMBRE ",max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    prenomp=forms.CharField(label="Prenom", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    nomp=forms.CharField(label="Nom", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    sexep=forms.ChoiceField(label="Sexe", choices=gender_choice, widget=forms.Select(attrs={"class":"form-control"}))
    datenaissancep =  forms.DateField(label="DATE DE NAISSANCE (YYYY-MM-DD)", widget=DateInput(format=('%d/%m/%Y'),attrs={"class":"form-control"}),initial="2022-08-22")
    lieunaissancep=forms.CharField(label="Lieu de Naissance", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}),initial="Zone1")
    adressep=forms.CharField(label="Adresse", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}),initial="07,Santo 9 prolonge")
    villep =  forms.CharField(label="VILLE ",max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}), initial="Port-au-Prince")
    communep =  forms.CharField(label="COMMUNE ",max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}),initial="Croix-des-Bouquets")
    departementp =  forms.CharField(label="DEPARTEMENT ",max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}), initial="OUEST")
    paysp =  forms.CharField(label="PAYS ",max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}),initial="HAITI")
    nifp =  forms.CharField(label="NIF/CIN ",max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}),initial="00-00-000-0")
    telephone1p =  forms.CharField(label="TELEPHONE 1 ",max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}),initial="0000-0000")
    telephone2p =  forms.CharField(label="TELEPHONE 2 ",max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}), initial="0000-0000")
    activiteprofessionp =  forms.CharField(label="ACTIVITE / PROFESSION ",max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}),initial="Biznisman")
    referencep =  forms.CharField(label="REFERENCE ",max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}), initial="President")
    profile_pic=forms.FileField(label="Profile Pic", max_length=50, widget=forms.FileInput(attrs={"class":"form-control"}))

