from django.db import models

# Create your models here.

class User(models.Model):
    user_id = models.AutoField(primary_key = True)
    username = models.CharField(max_length = 30, default = " ", unique = True)
    password = models.CharField(max_length = 20, default = " ")
    email = models.EmailField(default = " ")
    name = models.CharField(max_length = 50, default = " ")
    role_choice = [('SM', 'Scrum Master'), ('PO', 'Product Owner'), ('D', 'Developer')]
    role = models.CharField(max_length = 30, choices = role_choice, default = 'D')
    def __str__ (self):
        return f'User_id: {self.user_id} Username: {self.username}'

class Project(models.Model):
    project_id = models.AutoField(primary_key = True)
    project_name = models.CharField(max_length = 100, default = " ")
    project_description = models.TextField(default = " ")
    def __str__(self):
        return f'Project_id: {self.project_id} Project_name: {self.project_name}'

class Sprint(models.Model):
    sprint_id = models.AutoField(primary_key =  True)
    sprint_number = models.IntegerField(default = 1, null = True, blank=True, unique = True)
    project_id = models.ForeignKey(Project, on_delete = models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    def __str__(self):
        return f'Sprint {self.sprint_number}'

class PBI(models.Model):
    pbi_id = models.AutoField(primary_key = True)
    project_id = models.ForeignKey(Project, on_delete = models.CASCADE)
    sprint_number = models.ForeignKey(Sprint, on_delete = models.CASCADE, null = True, default = None, blank = True)
    epic = models.TextField(default = " ", blank = True)
    user_story = models.TextField(default = " ")
    story_point = models.IntegerField(default = 0)
    priority = models.IntegerField(default = 0)
    def __str__(self):
        return f'PBI_id:{self.pbi_id} Story: {self.user_story}'

class Task(models.Model):
    task_id = models.AutoField(primary_key = True)
    pbi_id = models.ForeignKey(PBI, on_delete = models.CASCADE)
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    task_description = models.TextField(default = " ")
    effort_hour = models.IntegerField(default = 0)
    status_choice = [('New','Not yet started'), ('Progress', 'In progress'), ('Done', 'Completed')]
    status = models.CharField(max_length = 50, choices = status_choice, default = 'New')
    def __str__(self):
        return f'Task_id: {self.task_id} Description: {self.task_description}'

class WorksOn(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    project_id = models.ForeignKey(Project, on_delete = models.CASCADE, default = 0)
    def __str__(self):
        return f'User: + {self.user_id} Project_ID: ({self.project_id})'




