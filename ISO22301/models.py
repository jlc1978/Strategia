from django.db import models

# Create your models here.

class Dashboard(models.Model):
    dashboard = models.CharField(max_length=50)
    company = models.CharField(max_length=150, default="None")
   

    def __str__(self):
        return f"Company: {self.company} Dashboard: {self.dashboard}"
    
class Project(models.Model):
    project = models.CharField(max_length=30)
    project_text = models.CharField(max_length=150)
    outcome = models.CharField(max_length=30)
    outcome_text = models.CharField(max_length=150)
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.project} purpose {self.project_text}, {self.outcome} desired is {self.outcome_text}"


class Area(models.Model):
    area = models.CharField(max_length=30)
    areatext = models.CharField(max_length=400)

    def __str__(self):
        return f"{self.area} Purpose: {self.areatext}"

class Area_Topic(models.Model):
    areatopic = models.CharField(max_length=400)
    context = models.CharField(max_length=400)
    divcontext = models.CharField(max_length=400)
    area = models.ForeignKey(
        Area, on_delete=models.CASCADE, null = True
    )

    def __str__(self):
        return f"{self.areatopic}"
    
class Area_Header(models.Model):
    areaheader = models.CharField(max_length=400)
    area = models.ForeignKey(
        Area, on_delete=models.CASCADE, null = True
    )

    def __str__(self):
        return f"{self.areaheader}"

class Respondent(models.Model):
    first_name = models.CharField(max_length=30, null=True,)
    last_name = models.CharField(max_length=30, null=True,)
    company = models.CharField(max_length=75, null=True,)
    email = models.EmailField(max_length=256, null=False,)
    password = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.first_name} {self.last_name} Company: {self.company} Email: {self.email} "

class Topic(models.Model):
    topic = models.CharField(max_length=30)
    area = models.ForeignKey(
        Area, on_delete=models.CASCADE, null=True
    )

    def __str__(self):
        return f"{self.topic}"


class Question(models.Model):
    question = models.CharField(max_length=200)
    topic = models.ForeignKey(
        Topic, on_delete=models.CASCADE, null=True
    )
    area = models.ForeignKey(
        Area, on_delete=models.CASCADE, null=True
    ) # Django will store this as area_id on database


    def __str__(self):
        return self.question

class Answer(models.Model):
    area = models.ForeignKey(
        Area, on_delete=models.CASCADE, null  = True 
    )
    value = models.IntegerField(null = True, blank=False)
    company=models.CharField(max_length=250, null = True)
    timestamp= models.TimeField(auto_now = True)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, null  = True, unique=False
    )

    respondent = models.IntegerField(null = True, blank=False)
    
    
    

    def __str__(self):
        return f"{self.timestamp} {self.respondent} answer to {self.question} is {self.value}"


class Comment(models.Model):
    respondent = models.CharField(max_length=20)
    company = models.CharField(max_length=75, null=True,)
    comments = models.CharField(max_length=1000, default="No comment")
    timestamp= models.TimeField(auto_now = True)
    area = models.ForeignKey(
        Area, on_delete=models.CASCADE, null = True, blank=True
    )

    def __str__(self):
        return f"{self.respondent} comments are {self.comments}"

class ISO(models.Model):
    name=models.CharField(max_length=100)
    number=models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name}"
      
class Column_Header(models.Model):
    colhead = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.colhead}"
    
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    choice = models.IntegerField(default=0)
