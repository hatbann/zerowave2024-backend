# Generated by Django 4.2.13 on 2024-07-05 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_boardmodel_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='boardmodel',
            name='address',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
