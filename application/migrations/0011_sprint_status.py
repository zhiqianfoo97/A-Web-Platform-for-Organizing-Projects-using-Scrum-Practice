# Generated by Django 2.2.5 on 2019-11-08 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0010_auto_20191107_2230'),
    ]

    operations = [
        migrations.AddField(
            model_name='sprint',
            name='status',
            field=models.CharField(choices=[('Progress', 'In progress'), ('Done', 'Completed')], default='New', max_length=50),
        ),
    ]