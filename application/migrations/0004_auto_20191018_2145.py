# Generated by Django 2.2.5 on 2019-10-18 13:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0003_auto_20191018_2048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pbi',
            name='epic',
            field=models.TextField(blank=True, default=' '),
        ),
        migrations.AlterField(
            model_name='pbi',
            name='sprint_number',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='application.Sprint'),
        ),
        migrations.AlterField(
            model_name='sprint',
            name='sprint_number',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
