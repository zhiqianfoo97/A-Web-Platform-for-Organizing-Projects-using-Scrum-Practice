from django.test import TestCase
from datetime import datetime

from .models import *
userData = {
    "username": "John_Dalton",
    "password": "1234",
    "email": "john@gmail.com",
    "name": "John Dalton",
    "role": "SM"
}

projectData = {
    "project_name": "backtrack",
    "project_description": "course project"
}

sprintData = {
    "sprint_number": 1,
    "start_date": datetime(2019, 10, 20),
    "end_date": datetime(2019, 10, 24)
}

pbiData = {
    "epic": "",
    "user_story": "",
    "story_point": 12,
    "priority": 3
}

taskData = {
    "task_description": "design the UI",
    "effort_hour": 10,
    "status": "New"
}

class UserModelTestCase(TestCase):
    def createUser(self):
        user = User(
            username=userData["username"], 
            password=userData["password"],
            email=userData["email"],
            name=userData["name"],
            role=userData["role"]
        )
        return user
    
    def checkUserDataEqual(self, user):
        if user.username != userData["username"] :
            return False
        if user.password != userData["password"] :
            return False
        if user.email != userData["email"] :
            return False
        if user.name != userData["name"] :
            return False
        if user.role != userData["role"] :
            return False
        return True

    def test_valid_creation(self):
        # print (self.userData)
        user = self.createUser()
        self.assertIs(self.checkUserDataEqual(user), True)

class ProjectModelTest(TestCase):
    def createProject(self):
        project = Project(project_name=projectData["project_name"], 
                          project_description=projectData["project_description"])
        return project
    
    def createProject(self):
        project = Project(
            project_name=projectData["project_name"], 
            project_description=projectData["project_description"]
        )
        return project

    def checkProjectDataEqual(self, project):
        if project.project_name != projectData["project_name"] :
            return False
        if project.project_description != projectData["project_description"] :
            return False
        return True

    def test_valid_creation(self):
        project = self.createProject()
        self.assertIs(self.checkProjectDataEqual(project), True)

    def test_link_with_sprint(self):
        project = self.createProject()
        project.save()
        project.sprint_set.create(
            sprint_number=sprintData["sprint_number"], 
            start_date=sprintData["start_date"],
            end_date=sprintData["end_date"]
        )
        sprint = project.sprint_set.all()[0]
        self.assertIs(sprint.project_id, project)
    
    def test_link_with_pbi(self):
        project = self.createProject()
        project.save()
        project.pbi_set.create(
            epic = pbiData["epic"],
            user_story = pbiData["user_story"],
            story_point = pbiData["story_point"],
            priority = pbiData["priority"]
        )
        pbi = project.pbi_set.all()[0]
        self.assertIs(pbi.project_id, project)

class SprintModelTest(TestCase):
    def createSprint(self):
        sprint = Sprint(
            sprint_number=sprintData["sprint_number"], 
            start_date=sprintData["start_date"],
            end_date=sprintData["end_date"]
        )
        return sprint
    
    def createProject(self):
        project = Project(project_name=projectData["project_name"], 
                          project_description=projectData["project_description"])
        return project

    def checkSprintDataEqual(self, sprint):
        if sprint.sprint_number != sprintData["sprint_number"] :
            return False
        if sprint.start_date != sprintData["start_date"] :
            return False
        if sprint.end_date != sprintData["end_date"] :
            return False
        return True

    def test_valid_creation(self):
        sprint = self.createSprint()
        self.assertIs(self.checkSprintDataEqual(sprint), True)
    
    def test_link_with_pbi(self):
        project = Project(
            project_name=projectData["project_name"], 
            project_description=projectData["project_description"]
        )
        project.save()
        project.pbi_set.create(
            epic = pbiData["epic"],
            user_story = pbiData["user_story"],
            story_point = pbiData["story_point"],
            priority = pbiData["priority"]
        )
        pbi = project.pbi_set.all()[0]
        project.sprint_set.create(
            sprint_number=sprintData["sprint_number"], 
            start_date=sprintData["start_date"],
            end_date=sprintData["end_date"]
        )
        sprint = project.sprint_set.all()[0]
        pbi.sprint_number = sprint
        pbi.save()
        self.assertIs(project.pbi_set.all()[0].sprint_number.pk, sprint.pk)


class PbiModelTest(TestCase):
    def createPbi(self):
        pbi = PBI(
            epic = pbiData["epic"],
            user_story = pbiData["user_story"],
            story_point = pbiData["story_point"],
            priority = pbiData["priority"]
        )
        return pbi

    def checkPbiDataEqual(self, pbi):
        if pbi.epic != pbiData["epic"] :
            return False
        if pbi.user_story != pbiData["user_story"] :
            return False
        if pbi.story_point != pbiData["story_point"] :
            return False
        if pbi.priority != pbiData["priority"] :
            return False
        return True

    def test_valid_creation(self):
        pbi = self.createPbi()
        self.assertIs(self.checkPbiDataEqual(pbi), True)  

class TaskModelTest(TestCase):
    def createTask(self):
        task = Task(
            task_description = taskData["task_description"],
            effort_hour = taskData["effort_hour"],
            status = taskData["status"]
        )
        return task

    def checkTaskDataEqual(self, task):
        if task.task_description != taskData["task_description"] :
            return False
        if task.effort_hour != taskData["effort_hour"] :
            return False
        if task.status != taskData["status"] :
            return False
        return True

    def test_valid_creation(self):
        task = self.createTask()
        self.assertIs(self.checkTaskDataEqual(task), True)  

class WorksOnProjectModelTest(TestCase):
    pass

class WorksOnTaskModelTest(TestCase):
    pass