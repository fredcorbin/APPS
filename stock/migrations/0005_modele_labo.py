# Generated by Django 5.1.5 on 2025-02-03 10:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0004_remove_famille_pref_remove_modele_pref'),
    ]

    operations = [
        migrations.AddField(
            model_name='modele',
            name='labo',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='stock.labo'),
            preserve_default=False,
        ),
    ]
