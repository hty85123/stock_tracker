# Generated by Django 4.2.18 on 2025-02-02 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='ma20',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='record',
            name='ma5',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
