# Generated by Django 3.2.18 on 2023-03-20 11:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('g_muso_app', '0008_auto_20230316_0603'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='muso',
        ),
        migrations.AddField(
            model_name='membre',
            name='muso',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='g_muso_app.tbmuso'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[(1, 'HOD'), (2, 'Membre'), (3, 'SUPHOD')], default=1, max_length=10),
        ),
        migrations.AlterField(
            model_name='membre',
            name='sexep',
            field=models.CharField(blank=True, choices=[('M', 'Masculin'), ('F', 'Feminin')], max_length=50, null=True, verbose_name='SEXE MEMBRE '),
        ),
        migrations.AlterField(
            model_name='tbcotisation',
            name='typecotisation',
            field=models.CharField(blank=True, choices=[('Fonds Urgences', 'Fonds Urgences'), ('Fonds de Fonctionnement', 'Fonds de Fonctionnement'), ('Fonds de Credit', 'Fonds de Credit')], max_length=50, null=True, verbose_name='Type de Cotisation'),
        ),
        migrations.AlterField(
            model_name='tbmuso',
            name='email_muso',
            field=models.CharField(blank=True, max_length=50, verbose_name='EMAIL '),
        ),
        migrations.AlterField(
            model_name='tbmuso',
            name='site_muso',
            field=models.CharField(blank=True, max_length=50, verbose_name='SITE '),
        ),
    ]
