# Generated by Django 3.2.18 on 2023-03-11 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('g_muso_app', '0005_auto_20230309_0813'),
    ]

    operations = [
        migrations.AddField(
            model_name='membre',
            name='membre_actif',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='tbcotisation',
            name='typecotisation',
            field=models.CharField(blank=True, choices=[('Fonds de Fonctionnement', 'Fonds de Fonctionnement'), ('Fonds de Credit', 'Fonds de Credit'), ('Fonds Urgences', 'Fonds Urgences')], max_length=50, null=True, verbose_name='Type de Cotisation'),
        ),
    ]
