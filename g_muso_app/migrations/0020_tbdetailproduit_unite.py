# Generated by Django 3.2.18 on 2023-06-16 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('g_muso_app', '0019_auto_20230616_1214'),
    ]

    operations = [
        migrations.AddField(
            model_name='tbdetailproduit',
            name='unite',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Unite '),
        ),
    ]