from django.db import models

# Create your models here.

class Status(models.Model):
    status_id = models.AutoField(primary_key = True)
    status_name = models.CharField(max_length = 30, default = " ")
    def __str__(self):
        return f'{self.status_id} ({self.status_name})'

class Role(models.Model):
    role_id = models.AutoField(primary_key = True)
    role_name = models.CharField(max_length = 20, default = " ")
    def __str__(self):
        return f'{self.role_id} ({self.role_name})'

class User(models.Model):
    user_id = models.AutoField(primary_key = True)
    username = models.CharField(max_length = 30, default = " ")
    password = models.CharField(max_length = 20, default = " ")
    email = models.EmailField(default = " ")
    name = models.CharField(max_length = 50, default = " ")
    role_id = models.ForeignKey(Role, on_delete= models.CASCADE)
    def __str__ (self):
        return f'{self.user_id} ({self.username})'

class Project(models.Model):
    project_id = models.AutoField(primary_key = True)
    project_name = models.CharField(max_length = 100, default = " ")
    project_description = models.TextField(default = " ")
    def __str__(self):
        return f'{self.project_id} ({self.project_name})'

class Sprint(models.Model):
    sprint_id = models.AutoField(primary_key = True)
    project_id = models.ForeignKey(Project, on_delete = models.CASCADE)
    start_date = models.DateField(auto_now= True)
    end_date = models.DateField(auto_now = True)
    def __str__(self):
        return f'{self.sprint_id} ({self.project_id})'

class PBI(models.Model):
    pbi_id = models.AutoField(primary_key = True)
    project_id = models.ForeignKey(Project, on_delete = models.CASCADE)
    sprint_id = models.ForeignKey(Sprint, on_delete = models.CASCADE, default = 0)
    epic = models.TextField(default = " ")
    user_story = models.TextField(default = " ")
    story_point = models.IntegerField(default = 0)
    priority = models.IntegerField(default = 0)
    def __str__(self):
        return f'{self.pbi_id} ({self.user_story})'

class Task(models.Model):
    task_id = models.AutoField(primary_key = True)
    pbi_id = models.ForeignKey(PBI, on_delete = models.CASCADE)
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    status_id = models.ForeignKey(Status, on_delete = models.CASCADE)
    task_description = models.TextField(default = " ")
    effort_hour = models.IntegerField(default = 0)
    def __str__(self):
        return f'{self.task_id} ({self.task_description})'

class WorksOn(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    project_id = models.ForeignKey(Project, on_delete = models.CASCADE, default = 0)
    def __str__(self):
        return f'{self.user_id} ({self.project_id})'




