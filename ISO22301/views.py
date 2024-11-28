from django.shortcuts import render, redirect
from .models import Answer, Comment, Question, Area, Topic, Area_Header, Column_Header, Dashboard, Project, Area_Topic,Outcome_Colors, Surveys
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


def introduction(request,id): #id is the chsend survey's svg pth to be used to include outcome color
    current_path=id
    context_path={
        'current_path': current_path        
    }
    create_context=createheader(0,id) #pass starting values to use to extract desired text, get tuple
    context = create_context[0] #get context to pass n is the value to use in lists, convert tuple to dict
    context = context | context_path
    return render(request, "ISO22301/introduction.html",context)

def generic(request):
    return render(request, "ISO22301/generic.html",)


def results(request,id):
    user_id=request.user.id
    company = request.user.groups.values_list('name',flat = True)# Get company for user logged in
    user_name=request.user #Get username value as integer id NEW
    context_path={
        'current_path': id # get path for selected button and pass it via context     
    }
    create_context=createheader(0,id) #pass starting values to use to extract desired text, get tuple
    survey = create_context[2]
    context = create_context[0] #get context to pass n is the value to use in lists, convert tuple to dict
    context = context | context_path
# Identify whether the survey has been taken by seeing if a color has been provided
    colors=Outcome_Colors.objects.filter(user=user_id, path=id) #get QuerySet for Outcome colors
    if not colors:
        Outcome_Colors.objects.create(path=id, color='Blue', company=company, user_id=user_id, username=user_name, opacity= 0.0) #Default new entry for survey
    else:
        pass

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
        #user_id=request.user.id
        Comment.objects.create(comments = results_comments, user_id = user_id, company = company, username=user_name, survey_id=survey)
       # entry_time = datetime.datetime.now() #set time for data entry
   
        for i in range(len(keys_values)):#fill in answers to SQL table

            Answer.objects.create(question_id = keys_values_int[i],value = answers_values_int[i], area_id = questionareas_area_id[i], user_id=user_id, company=company, username=user_name)
        #results= Answer.objects.filter(respondent=respondent_id).values_list('area_id','value').order_by('-id')[:19] # get last 19 values for respondent to get current answers

        choices = create_context[1] #get list of choices to pass from create_context
        divcontext = Area.objects.values_list('divcontext', flat=True) #Get the divcontext values for each item in the results to align color with boxes
        area_and_overall_colors = determine_score(questionareas_area_id,answers_values_int,choices) #Get backgroundcolors for areas based on results
        area_colors = list(area_and_overall_colors[0]) ## get colors for context for radar plot and flowchart
        overall_color = area_and_overall_colors[1] # get colors for context for flowchart
        # Create data for radar plot and set display order to colockwide
        radar_data = radarplot(area_and_overall_colors)
        area_name = radar_data[0]
        area_scores = radar_data[1]
        max_scores = radar_data[2]
        print(area_name, area_scores)
        opacity= 1 # Set opacity to show outcome color on wheel
        #oc=Surveys.objects.filter(context=id).update(color=overall_color, opacity=opacity)
        oc_user=Outcome_Colors.objects.filter(user=user_id).filter(path=id).update(color=overall_color, opacity=opacity)
        divcontext_colors_zip = list(zip(divcontext,area_colors))# great tuple with divconetxt and color to use in results css 

       
       # Context for flow digram
        context_results ={
            "respondent_id": user_name,
            "comment": results_comments,
            #"color": area_colors,
            "divcontext_colors_zip": divcontext_colors_zip, #new
            "overallcolor": overall_color, # new
        }

        #Context for radar plot
        context_radar = {
            'area_colors': area_colors,
            'area_scores': area_scores,
            'area_name': area_name,
            'max': max_scores,



        }
        context = context_results | context | context_radar #combine context variables into one context to pass
        return render(request, "ISO22301/results.html",context)


    else:

        return render(request, "ISO22301/survey.html",context)


def wheel(request):
    user_id=request.user.id
    print(user_id)
    #Need to filter by user id
    #outcomecolors=list(Outcome_Colors.objects.values_list('path','color'))
    oc=Outcome_Colors.objects.filter(user=user_id).values_list('color', flat=True) #Get the colors for the wheel
    path=Outcome_Colors.objects.filter(user=user_id).values_list('path', flat=True) #get the paths to color
    opacity=Outcome_Colors.objects.filter(user=user_id).values_list('opacity', flat=True) #get the paths to color
    outcomecolors = list(zip(path,oc,opacity)) # create list of colors for each item
    context = {
       'wheelcolors': outcomecolors
    }
    return render(request, "ISO22301/wheel.html",context)


def createheader(n,id): # n is the value to use in lists created here, refers to teh ISO being generated Id is survey
    survey_id=Surveys.objects.filter(context=id).values_list("id", flat=True) #Get survey id for path
    survey_id_int=survey_id.first() # extract integer value
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
    #areaheader=Area_Header.objects.all() # get names of areas for header
    column_header=Column_Header.objects.all() #headers for table columns
    num_choices=list(Column_Header.objects.values_list('colcount',flat=True)) #h number of unique valoes0 to n
    num_choices_total=num_choices.count(1)
    nchoices = []
    for n in range(num_choices_total):
        nchoices.append(n)
    surveytopics = Area.objects.filter(survey=survey_id_int).all() #used in layout to enter topics in flexbox
    areas =  Area.objects.filter(survey=survey_id_int).all().prefetch_related('question_set') #Get list of areas tied to question set
    #areatopics = Surveys.objects.filter(context=id)
    #areaheader = Area.objects.values_list('area', flat=True)
    textname= ["Text"] #Comment feild text
    context_header = {
        "textname": textname,
        "area": areas,
        "surveytopics": surveytopics,
        #"areaheader": areaheader,
        "browsertab": browsertab,
        "dashboard_title": dashboard_title,
        "project": project,
        "projecttext": projecttext,
        "outcome": outcome,
        "outcometext": outcometext,
        "nchoices": nchoices,
        "columnheader": column_header,
        }
    return context_header, nchoices, survey_id_int


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
        area_scores.append(round(average_score * max_score,1)) # Create list of average scores for radar plot, convert to 0 to 5 scale, rounded to 1 decimal place
    score_ave_overall = aggregate_score / (area_total * max_score) # number of questions time max value of each question converted to 0 -1 scale
    overall_color = score_color_overall(score_ave_overall)
    #score_result.append(color)
    return score_result, overall_color, area_scores, max_score
    
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

def radarplot(area_and_overall_colors):
    #create data and names for radar plot to display in clockwise order
    area_scores = list(area_and_overall_colors[2]) # get scores for context for radar plot, convert to list to allow JSON to work properly
    top_value = area_scores.pop(0) #Get value to be on top of plot
    area_scores.append(top_value) # Add top value to end of list so it will be on top of plot when reversed
    area_scores.reverse() # Reverse list to display clockwise on radar plot
    max_scores = int(area_and_overall_colors[3]) # get max score value for context for radar plot
    area_name_qs = Area_Topic.objects.values_list('areatopic', flat=True) #Get the area name for radar chart as Query Set
    area_name =list(area_name_qs) # convert Query Set to list for use in tempalte js
    top_label = area_name.pop(0) #Get value to be on top of plot
    area_name.append(top_label) # Add top value to to end of list so it will be on top of plot when reversed
    area_name.reverse()# Reverse list to disply clockwise on radar plot

    return area_name, area_scores, max_scores