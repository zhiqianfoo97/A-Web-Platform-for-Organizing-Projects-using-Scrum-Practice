# Generated by Django 2.2.6 on 2019-12-05 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sprint',
            name='sprint_number',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
