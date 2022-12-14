# Generated by Django 4.0.6 on 2022-07-29 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charity_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='zip_code',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='institution',
            name='type',
            field=models.IntegerField(choices=[(1, 'fundacja'), (3, 'zbiórka lokalna'), (2, 'organizacja pozarządowa')], default=1),
        ),
    ]
