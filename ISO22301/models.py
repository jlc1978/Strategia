from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.

class Surveys(models.Model):
    survey = models.CharField(max_length=200)
    context = models.CharField(max_length=400) #identify survey css to use to set fill colors for visisted and results
    color = models.CharField(max_length=400) #set results color
    opacity = models.DecimalField(max_digits=2, decimal_places=1, blank = True) #Uset opacity for fill color for visited or results
    taken = models.IntegerField(blank = True) #Identify if survey taken: 0 = not taken, 1 = taken
    
    
    def __str__(self):
        return f"{self.survey} context is {self.context}"

class Area(models.Model):
    area = models.CharField(max_length=300)
    areatext = models.CharField(max_length=400)
    context = models.CharField(max_length=400)
    divcontext = models.CharField(max_length=400)
    survey = models.ForeignKey(
        Surveys, on_delete=models.CASCADE, null = True)


    def __str__(self):
        return f"{self.area} Purpose: {self.areatext}"

class Area_Topic(models.Model):
    areatopic = models.CharField(max_length=400)
    context = models.CharField(max_length=400)
    divcontext = models.CharField(max_length=400)
    survey = models.ForeignKey(
        Surveys, on_delete=models.CASCADE, null = True
    )
    area = models.ForeignKey(
        Area, on_delete=models.CASCADE, null = True
    )

    def __str__(self):
        return f"{self.area} {self.context}: {self.areatopic}"
    
class Area_Header(models.Model):
    areaheader = models.CharField(max_length=400)
    area = models.ForeignKey(
        Area, on_delete=models.CASCADE, null = True
    )

    def __str__(self):
        return f"{self.areaheader}"



class Comment(models.Model):
    company = models.CharField(max_length=75, null=True,)
    comments = models.CharField(max_length=1000, default="No comment")
    timestamp = models.TimeField(auto_now = True)
    area = models.ForeignKey(
        Area, on_delete=models.CASCADE, null = True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=75, null=True,)
    survey = models.ForeignKey(
        Surveys, on_delete=models.CASCADE, null = True)

    

    def __str__(self):
        return f"{self.user} {self.username} comments are {self.comments}"
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
    survey = models.ForeignKey(
        Surveys, on_delete=models.CASCADE, null = True)

    def __str__(self):
        return f"{self.project} purpose {self.project_text}, {self.outcome} desired is {self.outcome_text}"



class Topic(models.Model):
    topic = models.CharField(max_length=30)
    area = models.ForeignKey(
        Area, on_delete=models.CASCADE, null=True
    )

    def __str__(self):
        return f"{self.topic}"


class Question(models.Model):
    question = models.CharField(max_length=200)
    survey = models.ForeignKey(
        Surveys, on_delete=models.CASCADE, null=True
    )
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=75, null=True,)

    def __str__(self):
        return f"{self.user}  {self.username} answer to {self.question} is {self.value} at {self.timestamp}"

class ISO(models.Model):
    name=models.CharField(max_length=100)
    number=models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name}"
      
class Column_Header(models.Model):
    colhead = models.CharField(max_length=30)
    colcount = models.IntegerField(blank = True) #Used to determine number of radio buttons to render
    def __str__(self):
        return f"{self.colhead}"
    
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    choice = models.IntegerField(default=0)

class Outcome_Colors(models.Model):
    color=models.CharField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=75, null=True,)
    company=models.CharField(max_length=250, null = True)
    timestamp= models.TimeField(auto_now = True)
    path=models.CharField(max_length=20)
    opacity = models.DecimalField(max_digits=2, decimal_places=1, null = True) #Uset opacity for fill color for visited or results
    survey = models.ForeignKey(
        Surveys, on_delete=models.CASCADE, null = True)

    def __str__(self):
        return f"{self.user}  {self.username} path {self.path} is {self.color} at {self.timestamp}"

class Introduction(models.Model):
    intro=models.CharField(max_length=2000)
    survey = models.ForeignKey(
        Surveys, on_delete=models.CASCADE, null = True)
    
    def __str__(self):
        return f"{self.survey}: {self.intro}"
    
class Final_Result(models.Model):
    user_id = models.IntegerField(null = True, blank=False)
    area = models.CharField(max_length=300)
    scores = models.DecimalField(max_digits=2, decimal_places=1)
    max_scores=models.IntegerField(blank = True)
    survey = models.IntegerField(blank = True)
    company = models.CharField(max_length=250, null = True)
    area_id = models.IntegerField(null = True, blank=False)
    overall_color = models.CharField(max_length=20, null = True)
    survey_name = models.CharField(max_length=40, null = True)
    length = models.IntegerField(blank = True)
    respondent = models.CharField(max_length=250, null = True)
    area_color = models.CharField(max_length=20, null = True)

    def __str__(self):
        return f"{self.user_id} {self.respondent} company {self.company} survey {self.survey} area {self.area} score {self.scores} max {self.max_scores} "
    
class Respondent(models.Model):
    respondent = models.CharField(max_length=250, null = True)
    company=models.CharField(max_length=250, null = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Respondent {self.respondent} Company {self.company}"
    
class Final_Result_Question(models.Model):
    user_id = models.IntegerField(null = True, blank=False)
    area = models.CharField(max_length=300)
    question = models.CharField(max_length=250, null = True)
    scores = models.DecimalField(max_digits=2, decimal_places=1)
    max_scores=models.IntegerField(blank = True)
    survey = models.IntegerField(blank = True)
    company = models.CharField(max_length=250, null = True)
    area_id = models.IntegerField(null = True, blank=False)
    survey_name = models.CharField(max_length=40, null = True)
    respondent = models.CharField(max_length=250, null = True)

    def __str__(self):
        return f"{self.user_id} {self.respondent} company {self.company} survey {self.survey} area {self.area} score {self.scores} max {self.max_scores} "
    