from django.db import models
from django.db.models import F  
from django.core.exceptions import ValidationError
import datetime
# Create your models here.

class User_Manager(models.Manager):
    def create_User(self, _username, _password, _email, _name, _role):
        book = self.create(username = _username, password = _password, email = _email, name=_name, role=_role)
        book.save()
        return book

class User(models.Model):
    role_choice = [('SM', 'Scrum Master'), ('PO', 'Product Owner'), ('D', 'Developer')]

    user_id = models.AutoField(primary_key = True)
    username = models.CharField(max_length = 30, default = " ", unique = True)
    password = models.CharField(max_length = 20, default = " ")
    email = models.EmailField(default = " ")
    name = models.CharField(max_length = 50, default = " ") 
    role = models.CharField(max_length = 30, choices = role_choice, default = 'D')
    objects = User_Manager()

    def simple_serialise(self):
        data = {}
        data["user_id"] = self.user_id
        data["username"] = self.username
        data["password"] = self.password
        data["email"] = self.email if self.email == None else self.email
        data["name"] = self.name if self.name == None else self.name
        data["role"] = self.role if self.role == None else self.role
        return data

    def __str__ (self):
        return f'User_id: {self.user_id}, Name: {self.name}'

class Project(models.Model):
    status_choice = [('Progress', 'In progress') ,('Done', 'Completed')]
    project_id = models.AutoField(primary_key = True)
    project_name = models.CharField(max_length = 100, default = " ")
    project_description = models.TextField(default = " ")
    status = models.CharField(max_length = 50, choices = status_choice, default = 'Progress')

    def simple_serialise(self):
        data = {}
        data["project_id"] = self.project_id
        data["project_name"] = self.project_name if self.project_name == None else self.project_name
        data["project_description"] = self.project_description if self.project_description == None else self.project_description
        return data

    def __str__(self):
        return f'Project_id: {self.project_id}, Project_name: {self.project_name}'

class Sprint(models.Model):
    status_choice = [('Progress', 'In progress') ,('Done', 'Completed')]

    sprint_id = models.AutoField(primary_key =  True)
    sprint_number = models.IntegerField(default = 1, null = True, blank=True)
    project_id = models.ForeignKey(Project, on_delete = models.CASCADE)
    start_date = models.DateField(default = None, null = True, blank = True)
    end_date = models.DateField(null = True, blank = True)
    status = models.CharField(max_length = 50, choices = status_choice, default = 'Progress')
    max_effort_hour = models.IntegerField(default = 0)
    
    def simple_serialise(self):
        data = {}
        data["sprint_id"] = self.sprint_id
        data["sprint_number"] = self.sprint_number
        data["project_id"] = self.project_id if self.project_id == None else self.project_id.pk
        data["start_date"] = self.start_date if self.start_date == None else self.start_date.strftime("%Y-%m-%d")
        data["end_date"] = self.end_date if self.end_date == None else self.end_date.strftime("%Y-%m-%d")
        return data

    def __str__(self):
        return f'Project_id {self.project_id}, Sprint {self.sprint_number}'

class PBI_Manager(models.Manager):
    def create_pbi(self, _user_story, _sprint, _project_id, _story_point, _priority):
        book = self.create(user_story = _user_story, sprint_number = _sprint, project_id = _project_id, story_point = _story_point, priority = _priority)
        book.save()
        return book

class PBI(models.Model):
    status_choice = [('New', 'Not yet started'), ('Progress', 'In progress'), ('Not', 'Unfinished') ,('Done', 'Completed')]

    pbi_id = models.AutoField(primary_key = True)
    project_id = models.ForeignKey(Project, on_delete = models.CASCADE)
    sprint_number = models.ForeignKey(Sprint, on_delete = models.CASCADE, null = True, default = None, blank = True)
    epic = models.TextField(default = " ", blank = True)
    user_story = models.TextField(default = " ")
    story_point = models.IntegerField(default = 0)
    status = models.CharField(max_length = 50, choices = status_choice, default = 'New')
    objects = PBI_Manager()

    def simple_serialise(self):
        data = {}
        data["pbi_id"] = self.pbi_id
        data["project_id"] = self.project_id if self.project_id == None else self.project_id.pk
        data["sprint"] = self.sprint_number if self.sprint_number == None else self.sprint_number.sprint_number
        data["user_story"] = self.user_story
        data["story_point"] = self.story_point
        data["status"] = self.getStatus()
        data["can_remove_from_sprint"] = self.canRemoveFromSprint()
        return data

    def getNumOfPbi():
        return PBI.objects.all().count() + 1

    priority = models.IntegerField(null = True , default = getNumOfPbi, blank = True)

    def __str__(self):
        return f'PBI_id:{self.pbi_id}, Story: {self.user_story}, story_point: {self.story_point}, sprint_id: {self.sprint_number}, status: {self.status}'

    def getStatus(self):
        if self.status == "Done":
            return "Completed"
        pbiTask = Task.objects.all().filter(pbi_id = self.pbi_id)
        pbiTask = pbiTask.exclude(effort_hour = 0)
        pbiTaskCount = pbiTask.count()
        notYetStarted = 0
        completed = 0
        unfinished = 0
        if (pbiTaskCount == 0):
            if self.status == "Not":
                return "Unfinished"
            else:
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
                return "Completed"
            else:
                self.status = 'Progress'
                self.save()
                return "In progress"

    def setStatus(self, status):
        self.status = status
        self.save()

    def canRemoveFromSprint(self):
        if self.status == "Done":
            return 0
        pbiTask = Task.objects.all().filter(pbi_id = self.pbi_id)
        # print (self.pbi_id)
        # print (pbiTask)
        pbiTask = pbiTask.exclude(effort_hour = 0)
        pbiTask = pbiTask.filter(status = "Done")
        if (pbiTask.count() == 0):
            return 1
        return 0

    def getCumulativeSP(self):
        # pbiList = PBI.objects.filter(project_id = project_id).order_by('priority').exclude(story_point = 0)
        pbiList = PBI.objects.filter(project_id = self.project_id.pk).order_by('priority')
        # print(self.project_id.pk)
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

    def getNewTaskTotalEH(self):
        total = 0
        taskList = Task.objects.filter(pbi_id = self.pbi_id, status = 'New')
        for task1 in taskList:
            total += task1.effort_hour
        
        return total

    def getInProgressTaskTotalEH(self):
        total = 0
        taskList = Task.objects.filter(pbi_id = self.pbi_id, status = 'Progress')
        for task1 in taskList:
            total += task1.effort_hour
        
        return total

    def getCompletedTaskTotalEH(self):
        total = 0
        taskList = Task.objects.filter(pbi_id = self.pbi_id, status = 'Done')
        for task1 in taskList:
            total += task1.effort_hour
        
        return total


class Task_Manager(models.Manager):
    def create_task(self, _pbi_id, _task_description, _task_effort_hour):
        book = self.create(pbi_id = _pbi_id, task_description = _task_description, effort_hour = _task_effort_hour, status= 'New')
        book.save()
        return book

class Task(models.Model):
    status_choice = [('New','Not yet started'), ('Progress', 'In progress'), ('Not' , 'Unfinished') ,('Done', 'Completed')]

    task_id = models.AutoField(primary_key = True)
    pbi_id = models.ForeignKey(PBI, on_delete = models.CASCADE)
    task_description = models.TextField(default = " ")
    effort_hour = models.IntegerField(default = 0)
    status = models.CharField(max_length = 50, choices = status_choice, default = 'New')
    objects = Task_Manager()

    def simple_serialise(self):
        data = {}
        data["task_id"] = self.task_id
        data["pbi_id"] = self.pbi_id if self.pbi_id == None else self.pbi_id.pk
        data["task_description"] = self.task_description if self.task_description == None else self.task_description
        data["effort_hour"] = self.effort_hour if self.effort_hour == None else self.effort_hour
        data["status"] = self.status if self.status == None else self.status
        return data

    def __str__(self):
        return f'Task_id: {self.task_id}, Description: {self.task_description}'

class WorksOnProject_Manager(models.Manager):
    def create_WorksOnProject(self, _user_id, _project_id):
        book = self.create(user_id = _user_id, project_id = _project_id)
        book.save()
        return book

class WorksOnProject(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    project_id = models.ForeignKey(Project, on_delete = models.CASCADE, default = 0)
    objects = WorksOnProject_Manager()
    def __str__(self):
        return f'User: {self.user_id}, Project_ID: ({self.project_id})'


class WorksOnTask_Manager(models.Manager):
    def create_WorksOnTask(self, _user_id, _task_id):
        book = self.create(user_id = _user_id, task_id=_task_id)
        book.save()
        return book

class WorksOnTask(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    task_id = models.ForeignKey(Task, on_delete = models.CASCADE)
    objects = WorksOnTask_Manager()
    def __str__(self):
        return f'User: {self.user_id}, Task: {self.task_id}'


class Notification_Manager(models.Manager):
    def create_Notification(self, _user_id, _project, _messages):
        book = self.create(user_id = _user_id, project_id = _project, messages = _messages)
        book.save()
        return book

class Notification(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    project_id = models.ForeignKey(Project, on_delete = models.CASCADE)
    messages = models.TextField(default = " ")
    objects = Notification_Manager()
    def __str__(self):
        return f'User: {self.user_id}, Message: {self.messages}'
