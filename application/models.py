from django.db import models

# Create your models here.

class Status(models.Model):
    status_id = models.AutoField(primary_key = True)
    status_name = models.CharField(max_length = 30)
    def __str__(self):
        return f'{self.status_id} ({self.name})'

class Role(models.Model):
    role_id = models.AutoField(primary_key = True)
    role_name = models.CharField(max_length = 20)
    def __str__(self):
        return self.role_id

class User(models.Model):
    user_id = models.AutoField(primary_key = True)
    username = models.CharField(max_length = 30)
    password = models.CharField(max_length = 20)
    email = models.EmailField
    name = models.CharField(max_length = 50)
    role_id = models.ForeignKey(Role, on_delete= models.CASCADE)
    def __str__ (self):
        return self.user_id

class Project(models.Model):
    project_id = models.AutoField(primary_key = True)
    project_name = models.CharField(max_length = 100)
    project_description = models.TextField
    def __str__(self):
        return f'{self.project_id} ({self.project_name})'

class Sprint(models.Model):
    sprint_id = models.AutoField(primary_key = True)
    project_id = models.ForeignKey(Project, on_delete = models.CASCADE)
    start_date = models.DateField
    end_date = models.DateField
    def __str__(self):
        return f'{self.sprint_id} ({self.project_id})'

class PBI(models.Model):
    pbi_id = models.AutoField(primary_key = True)
    project_id = models.ForeignKey(Project, on_delete = models.CASCADE)
    sprint_id = models.ForeignKey(Sprint, on_delete = models.CASCADE)
    epic = models.TextField
    user_story = models.TextField
    story_point = models.IntegerField
    priority = models.IntegerField
    def __str__(self):
        return self.pbi_id

class Task(models.Model):
    task_id = models.AutoField(primary_key = True)
    pbi_id = models.ForeignKey(PBI, on_delete = models.CASCADE)
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    status_id = models.ForeignKey(Status, on_delete = models.CASCADE)
    task_description = models.TextField
    effort_hour = models.IntegerField
    def __str__(self):
        return self.task_id

class WorksOn(models.Model):
    user_id = models.ManyToManyField(User)
    project_id = models.ManyToManyField(Project)
    def __str__(self):
        return f'{self.user_id} ({self.project_id})'





