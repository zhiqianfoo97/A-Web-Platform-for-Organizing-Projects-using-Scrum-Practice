from django.db import models
from django.db.models import F  
from django.core.exceptions import ValidationError

# Create your models here.

class User(models.Model):
    role_choice = [('SM', 'Scrum Master'), ('PO', 'Product Owner'), ('D', 'Developer')]

    user_id = models.AutoField(primary_key = True)
    username = models.CharField(max_length = 30, default = " ", unique = True)
    password = models.CharField(max_length = 20, default = " ")
    email = models.EmailField(default = " ")
    name = models.CharField(max_length = 50, default = " ") 
    role = models.CharField(max_length = 30, choices = role_choice, default = 'D')
    def __str__ (self):
        return f'User_id: {self.user_id}, Name: {self.name}'

class Project(models.Model):
    project_id = models.AutoField(primary_key = True)
    project_name = models.CharField(max_length = 100, default = " ")
    project_description = models.TextField(default = " ")
    def __str__(self):
        return f'Project_id: {self.project_id}, Project_name: {self.project_name}'

class Sprint(models.Model):
    sprint_id = models.AutoField(primary_key =  True)
    sprint_number = models.IntegerField(default = 1, null = True, blank=True, unique = True)
    project_id = models.ForeignKey(Project, on_delete = models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    def __str__(self):
        return f'Sprint {self.sprint_number}'

class PBI_Manager(models.Manager):
    def create_pbi(self, _user_story, _sprint, _project_id, _story_point, _priority):
        book = self.create(user_story = _user_story, sprint_number = _sprint, project_id = _project_id, story_point = _story_point, priority = _priority)
        book.save()
        return book

class PBI(models.Model):
    pbi_id = models.AutoField(primary_key = True)
    project_id = models.ForeignKey(Project, on_delete = models.CASCADE)
    sprint_number = models.ForeignKey(Sprint, on_delete = models.CASCADE, null = True, default = None, blank = True)
    epic = models.TextField(default = " ", blank = True)
    user_story = models.TextField(default = " ")
    story_point = models.IntegerField(default = 0)
    objects = PBI_Manager()

    def getNumOfPbi():
        return PBI.objects.all().count() + 1

    priority = models.IntegerField(null = True , default = getNumOfPbi, blank = True)

    def __str__(self):
        return f'PBI_id:{self.pbi_id}, Story: {self.user_story}'

    def getStatus(self):
        
        pbiTask = Task.objects.all().filter(pbi_id = self.pbi_id)
        pbiTaskCount = pbiTask.count()
        notYetStarted = 0
        completed = 0
        if (pbiTaskCount == 0):
            return "Not yet started"

        else:
            for _task in pbiTask:
                if (_task.status == 'New'):
                    notYetStarted += 1
                elif(_task.status == 'Done'):
                    completed +=1
            
            if(notYetStarted == pbiTaskCount):
                return "Not yet started"
            elif(completed == pbiTaskCount):
                self.story_point = 0
                self.priority = None
                self.save()
                return "Completed"
            else:
                return "In progress"

    def getCumulativeSP(self):
        pbiList = PBI.objects.order_by('priority').exclude(story_point = 0)
        # pbiList = PBI.objects.order_by('priority')
        cumulativeSP = 0
        for pbi1 in pbiList:
            cumulativeSP += pbi1.story_point
            if (pbi1.pbi_id == self.pbi_id):
                break
            
        return cumulativeSP

    def getTaskTotalEH(self):
        total = 0
        taskList = Task.objects.filter(pbi_id = self.pbi_id)

        for task1 in taskList:
            total += task1.effort_hour
        
        return total

class Task_Manager(models.Manager):
    def create_task(self, _pbi_id, _task_description, _task_effort_hour):
        book = self.create(pbi_id = _pbi_id, task_description = _task_description, effort_hour = _task_effort_hour, status= 'New')
        book.save()
        return book

class Task(models.Model):
    status_choice = [('New','Not yet started'), ('Progress', 'In progress'), ('Done', 'Completed')]

    task_id = models.AutoField(primary_key = True)
    pbi_id = models.ForeignKey(PBI, on_delete = models.CASCADE)
    task_description = models.TextField(default = " ")
    effort_hour = models.IntegerField(default = 0)
    status = models.CharField(max_length = 50, choices = status_choice, default = 'New')
    objects = Task_Manager()
    def __str__(self):
        return f'Task_id: {self.task_id}, Description: {self.task_description}'
    
class WorksOnProject(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    project_id = models.ForeignKey(Project, on_delete = models.CASCADE, default = 0)
    def __str__(self):
        return f'User: {self.user_id}, Project_ID: ({self.project_id})'

class WorksOnTask(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    task_id = models.ForeignKey(Task, on_delete = models.CASCADE)
    def __str__(self):
        return f'User: {self.user_id}, Task: {self.task_id}'




