# Generated by Django 4.2.3 on 2023-07-07 16:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('g_muso_app', '0022_auto_20230625_0912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tbcotisation',
            name='typecotisation',
            field=models.CharField(blank=True, choices=[('Fonds de Fonctionnement', 'Fonds de Fonctionnement'), ('Fonds de Credit', 'Fonds de Credit'), ('Fonds Urgences', 'Fonds Urgences')], max_length=50, null=True, verbose_name='Type de Cotisation'),
        ),
        migrations.CreateModel(
            name='tbtypecotisation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_cotisation', models.CharField(blank=True, max_length=50, verbose_name='Libelle ')),
                ('cotisation_muso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='g_muso_app.tbmuso')),
            ],
        ),
    ]