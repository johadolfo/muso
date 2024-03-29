# Generated by Django 4.2.3 on 2023-07-08 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('g_muso_app', '0023_alter_tbcotisation_typecotisation_tbtypecotisation'),
    ]

    operations = [
        migrations.AddField(
            model_name='tbtypecotisation',
            name='reference',
            field=models.CharField(blank=True, max_length=50, verbose_name='Reference Caisse '),
        ),
        migrations.AlterField(
            model_name='membre',
            name='sexep',
            field=models.CharField(blank=True, choices=[('F', 'Feminin'), ('M', 'Masculin')], max_length=50, null=True, verbose_name='SEXE MEMBRE '),
        ),
    ]
