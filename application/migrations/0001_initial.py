# Generated by Django 2.2.5 on 2019-10-17 16:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PBI',
            fields=[
                ('pbi_id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('project_id', models.AutoField(primary_key=True, serialize=False)),
                ('project_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('role_id', models.AutoField(primary_key=True, serialize=False)),
                ('role_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('status_id', models.AutoField(primary_key=True, serialize=False)),
                ('status_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=50)),
                ('role_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.Role')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('task_id', models.AutoField(primary_key=True, serialize=False)),
                ('pbi_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.PBI')),
                ('status_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.Status')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.User')),
            ],
        ),
        migrations.CreateModel(
            name='Sprint',
            fields=[
                ('sprint_id', models.AutoField(primary_key=True, serialize=False)),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.Project')),
            ],
        ),
        migrations.AddField(
            model_name='pbi',
            name='project_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.Project'),
        ),
        migrations.AddField(
            model_name='pbi',
            name='sprint_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.Sprint'),
        ),
    ]
