from django.shortcuts import render, redirect
from .models import Answer, Comment, Question, Area, Topic, Area_Header, Column_Header, Dashboard, Project, Area_Topic
from collections import defaultdict, Counter
from django.contrib.auth import authenticate, login, logout 
from .forms import  LoginForm, LogoutForm
from django.contrib import messages
import datetime
from django.contrib.auth.decorators import login_required

# Create your views here.
"""def survey(request):
    create_context=createheader(0) #pass starting values to use to extract desired text, get tuple

    context = create_context[0] #get context to pass n is the value to use in lists, convert tuple to dict
    return render(request,"ISO22301/survey.html", context)"""

def layout(request):
    create_context=createheader(0) #pass starting values to use to extract desired text, get tuple
    context = create_context[0] #get context to pass n is the value to use in lists, convert tuple to dict
    return render(request, 'ISO22301/layout.html', context)


def introduction(request):
    create_context=createheader(0) #pass starting values to use to extract desired text, get tuple
    context = create_context[0] #get context to pass n is the value to use in lists, convert tuple to dict
    return render(request, "ISO22301/introduction.html",context)

def generic(request):
    return render(request, "ISO22301/generic.html",)


def results(request):
    create_context=createheader(0) #pass starting values to use to extract desired text, get tuple
    context = create_context[0] #get context to pass n is the value to use in lists, convert tuple to dict
    if request.method == "POST":                         
        keys_values=list(request.POST.keys()) #extract keys = questions are keys
        answers_values=list(request.POST.values())
        results_comments = answers_values.pop() #  Get comments from list

        keys_values.pop(0)# remove token so not part of list of values
        keys_values.pop() # remove comments so not part of list of values
        keys_values_int=[eval(i) for i in keys_values]
        answers_values.pop(0)# remove token
        answers_values_int=[eval(i) for i in answers_values] #ietrate to create list
        questionareas_area_id = Question.objects.values_list('area_id', flat=True) # get area names, Flat retuns just the text list of areas
        user_name=request.user #Get username value as integer id NEW
        user_id=request.user.id
        company = request.user.groups.values_list('name',flat = True)# Get company for user logged in
        Comment.objects.create(comments = results_comments, user_id = user_id, company = company, username=user_name)
       # entry_time = datetime.datetime.now() #set time for data entry
   
        for i in range(len(keys_values)):#fill in answers to SQL table

            Answer.objects.create(question_id = keys_values_int[i],value = answers_values_int[i], area_id = questionareas_area_id[i], user_id=user_id, company=company, username=user_name)
        #results= Answer.objects.filter(respondent=respondent_id).values_list('area_id','value').order_by('-id')[:19] # get last 19 values for respondent to get current answers

        choices = create_context[1] #get list of choices to pass from create_context
        divcontext = Area.objects.values_list('divcontext', flat=True) #Get the divcontext values for each item in the results to align color with boxes
        area_and_overall_colors = determine_score(questionareas_area_id,answers_values_int,choices) #Get backgroundcolors for areas based on results
        area_colors = area_and_overall_colors[0] #new
        overall_color = area_and_overall_colors[1] #new
        divcontext_colors_zip = list(zip(divcontext,area_colors))# great tuple with divconetxt and color to use in results css
        context_results ={
            "respondent_id": user_name,
            "comment": results_comments,
            #"color": area_colors,
            "divcontext_colors_zip": divcontext_colors_zip, #new
            "overallcolor": overall_color, # new

        }
        context = context_results | context #combine context variables into one context to pass
        
        return render(request, "ISO22301/results.html",context)


    else:

        return render(request, "ISO22301/survey.html",context)


def wheel(request):
    return render(request, "ISO22301/wheel.html",)


def createheader(n): # n is the value to use in lists created here, refers to teh ISO being generated

    #Name of browser tab
    browsertab=list(Dashboard.objects.values_list('company', flat=True))
    browsertab=browsertab[n]
        #Name of dashboard
    dashboard_title=list(Dashboard.objects.values_list('dashboard', flat=True))
    dashboard_title=dashboard_title[n]
    # names and text for both ends of LoO to extract value for current project
    project=list(Project.objects.values_list('project', flat=True))
    projecttext=list(Project.objects.values_list('project_text', flat=True))
    outcome=list(Project.objects.values_list('outcome', flat=True))
    outcometext=list(Project.objects.values_list('outcome_text', flat=True))
    # Used to identify specific text for ISO
    project=project[n]
    projecttext=projecttext[n]
    outcome=outcome[n]
    outcometext=outcometext[n]
    #layout data
    areaheader=Area_Header.objects.all() # get names of areas for header
    column_header=Column_Header.objects.all() #headers for table columns
    num_choices=list(Column_Header.objects.values_list('colcount',flat=True)) #h number of unique valoes0 to n
    num_choices_total=num_choices.count(1)
    nchoices = []
    for n in range(num_choices_total):
        nchoices.append(n)
    areatopics = Area.objects.all() #used in layout to enter topics in flexbox
    areas =  Area.objects.all().prefetch_related('question_set') #Get list of areas tied to question set
    areaheader = Area.objects.values_list('area', flat=True)
    textname= ["Text"] #Comment feild text
    context_header = {
        "textname": textname,
        "area": areas,
        "areatopics": areatopics,
        "areaheader": areaheader,
        "browsertab": browsertab,
        "dashboard_title": dashboard_title,
        "project": project,
        "projecttext": projecttext,
        "outcome": outcome,
        "outcometext": outcometext,
        "nchoices": nchoices,
        "columnheader": column_header,
        }
    return context_header, nchoices


def determine_score(area, values,choices):
    area_frequency = list(Counter(area).values()) # count frequency of questions in each areas convereted to list to 
    # be used to determine how often to iterate each area when determining the area's score
    area_total = sum(area_frequency) # get total number of questions
    num_areas = len(Counter(area)) #determine number of areas via couter()
    aggregate_score = 0 #total score
    area_scores = [] #list of the score for each area
    score_result = []
    max_score = choices.pop() # remove "Not Sure" zero value from calculation of max score
    start=0 #set start location of loop
    for n in range(num_areas): #loop through all areas to create list of values and compute score
        score = 0
        ai = start+area_frequency[n] # return number of question in each area and add to strat to get number of loops
  
        for x in range(start,ai):
            score+=values[x] #sume questions choices for area
       
        aggregate_score+=score # increment score by teh question results
        average_score = score / (area_frequency[n] * max_score)
        color = score_color(average_score)
        score_result.append(color)
        start += area_frequency[n] # Start at next area - move counter by number of questions in previous area
        area_scores.append(score)
    score_ave_overall = aggregate_score / (area_total * max_score)
    overall_color = score_color_overall(score_ave_overall)
    #score_result.append(color)
    return score_result, overall_color
    
def score_color(score): #Determine what color to shade scored area
    if score >= .8:
        color = "Green"
    elif score <= .2:
        color = "Red"
    else:
        color = "Yellow"
    return color

def score_color_overall(score): #Determine what color to shade scored area
    if score >= .8:
        color = "Green"
    elif score <= .2:
        color = "Red"
    else:
        color = "Yellow"
    return color




def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)   
                current_time = datetime.datetime.now()
                return redirect('wheel')
            else:
                return redirect('login')
    else:
        form = LoginForm()
    return render(request,'ISO22301/login.html', {'form': form},)


def user_logout(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            logout(request)
    #return redirect('logout')
    return render(request,'ISO22301/goodbye.html',)
