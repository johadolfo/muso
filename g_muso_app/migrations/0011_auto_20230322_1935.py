# Generated by Django 3.2.18 on 2023-03-22 23:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('g_muso_app', '0010_auto_20230320_1552'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adminhod',
            name='muso_hod',
        ),
        migrations.RemoveField(
            model_name='membre',
            name='muso',
        ),
        migrations.AddField(
            model_name='customuser',
            name='muso',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='g_muso_app.tbmuso'),
        ),
        migrations.AlterField(
            model_name='tbcotisation',
            name='typecotisation',
            field=models.CharField(blank=True, choices=[('Fonds Urgences', 'Fonds Urgences'), ('Fonds de Fonctionnement', 'Fonds de Fonctionnement'), ('Fonds de Credit', 'Fonds de Credit')], max_length=50, null=True, verbose_name='Type de Cotisation'),
        ),
    ]
