# Generated by Django 3.2.18 on 2023-06-05 19:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('g_muso_app', '0012_auto_20230601_1956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tbcotisation',
            name='typecotisation',
            field=models.CharField(blank=True, choices=[('Fonds Urgences', 'Fonds Urgences'), ('Fonds de Fonctionnement', 'Fonds de Fonctionnement'), ('Fonds de Credit', 'Fonds de Credit')], max_length=50, null=True, verbose_name='Type de Cotisation'),
        ),
        migrations.CreateModel(
            name='tbdetailcredit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_pret', models.DateField(blank=True, verbose_name='Date (YYYY-MM-DD)')),
                ('montant_pret', models.FloatField(blank=True, default='0.0', null=True, verbose_name='Montant Credit')),
                ('montant_capital', models.FloatField(blank=True, default='0.0', null=True, verbose_name='Capital ')),
                ('montant_interet', models.FloatField(blank=True, default='0.0', null=True, verbose_name='Montant Interet')),
                ('total_montant_jr', models.FloatField(blank=True, default='0.0', null=True, verbose_name='Total Montant journalier')),
                ('total_montant_rest', models.FloatField(blank=True, default='0.0', null=True, verbose_name='Total Montant Reste')),
                ('codecredit', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='g_muso_app.tbcredit')),
            ],
        ),
    ]
