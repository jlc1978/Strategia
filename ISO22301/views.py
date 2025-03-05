from django.shortcuts import render, redirect
from .models import Answer, Comment, Question, Area, Analysis_Final, Area_Header, Column_Header, Dashboard, Project, Area_Topic,Outcome_Colors, Surveys, Introduction, Final_Result,Respondent, Final_Result_Question
from collections import defaultdict, Counter
from django.contrib.auth import authenticate, login, logout 
from .forms import  LoginForm, LogoutForm
from django.contrib import messages
import datetime
from django.contrib.auth.decorators import login_required
import openai
import json

OPENAI_API_KEY = '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'

# Create your views here.
@login_required(login_url='login')
def introduction(request,id): #id is the chsend survey's svg pth to be used to include outcome color
    current_path=id #get id in forma#path_xx where xx is survey
    context_path={
        'current_path': current_path        
    }

    create_context=createheader(0,id) #pass starting values to use to extract desired text, get tuple
    context = create_context[0] #get context to pass n is the value to use in lists, convert tuple to dict
    context = context | context_path #add current path to context
    survey_id=Surveys.objects.filter(context=id).values_list("id", flat=True) #Get survey id for path
    survey_id_int=survey_id.first() #extract integer value
    intro_text_list=list(Introduction.objects.filter(survey_id =  survey_id_int).values_list('intro', flat=True)) #Get survey titleintro text and convert Query Set to list for path
    intro_text=intro_text_list[0]#Get text from list as flat text file for use in HTML rendering by reemoving [' '] from text
    context_survey={
        'current_path': current_path,
        'intro_text': intro_text,
    } # pass survey specific path, title and text for introduction 

    context = context | context_survey #add current path and text to context
    return render(request, "ISO22301/introduction.html",context)

@login_required(login_url='login')
def results(request,id):
    user_id=request.user.id #Get current user
    group=request.user.groups.all()# Get company for user logged in
    company=group.values_list('name', flat = True)
    user_name=request.user #Get username value as integer id NEW
    respondent=Respondent.objects.filter(respondent=user_name)#Get user_name if in db
    if not respondent: #if not in db add to Respondent
        Respondent.objects.create(company=company, respondent=user_name, user_id=user_id) #Create entreis with user_id FK to user
    else:
        pass
    context_path={
        'current_path': id # get path for selected button and pass it via context     
    }
    create_context=createheader(0,id) #pass starting values to use to extract desired text, get tuple
    survey = create_context[2] #get id of current survey from unction create_context as integer
    survey_text = Surveys.objects.filter(id=survey).values_list('survey', flat=True) #Get name of survey
    area_text = Question.objects.filter(survey_id=survey).values_list('area_id__area', flat=True)#Get text names for area by getting it via pk aread_id__area using __ to gt value ratehr than pk

    context = create_context[0] #get context to pass n is the value to use in lists, convert tuple to dict
    context = context | context_path # merge context values
# Identify whether the survey has been taken by seeing if a color has been provided
    colors=Outcome_Colors.objects.filter(user=user_id, path=id) #get QuerySet for Outcome colors

    if not colors: #Check to see if already outcome colors determined
        Outcome_Colors.objects.create(path=id, color='Blue', company=company, user_id=user_id, username=user_name, opacity= 0.0, survey_id=survey) #Default new entry for survey
    else:
        pass

    if request.method == "POST":                         
        keys_values=list(request.POST.keys()) #extract keys = questions are keys
        answers_values=list(request.POST.values())
   
        #results_comments = answers_values.pop() #  Get comments from list need to uncomment when commnets added back to template
        keys_values.pop(0)# remove token so not part of list of values
        keys_values.pop() # remove comments so not part of list of values

        keys_values_int=[eval(i) for i in keys_values]
        answers_values.pop(0)# remove token

        answers_values_int=[eval(i) for i in answers_values] #ietrate to create list

        questionareas_area_id = Question.objects.filter(survey_id = survey).values_list('area_id', flat=True) # get area names, Flat retuns just the text list of areas
        questions_text = Question.objects.filter(survey_id = survey).values_list('question', flat=True) # Get question text for final result table
        #user_id=request.user.id
        #Comment.objects.create(comments = results_comments, user_id = user_id, company = company, username=user_name, survey_id=survey) # Add back in when comments added in
       # entry_time = datetime.datetime.now() #set time for data entry
   
        for i in range(len(keys_values)):#fill in answers to SQL table

            Answer.objects.create(question_id = keys_values_int[i],value = answers_values_int[i], area_id = questionareas_area_id[i], user_id=user_id, company=company, username=user_name)
        #results= Answer.objects.filter(respondent=respondent_id).values_list('area_id','value').order_by('-id')[:19] # get last 19 values for respondent to get current answers

        # Create list of final answers for analysis
        
        user = Final_Result_Question.objects.filter(user_id=user_id,survey = survey) #get QuerySet for user to see if data already exists
        if not user: # if no data exists in Final_Results create data entry
            for j in range(len(keys_values)):#fill in answers to SQL table
                Final_Result_Question.objects.create(area = area_text[j],question = questions_text[j],scores = answers_values_int[j], max_scores = 5, area_id = questionareas_area_id[j], user_id=user_id, company=company, respondent=user_name, survey=survey,survey_name=survey_text)
 
            else: #If data exists update to latets answers from user
                for i in range(len(keys_values)):#fill in answers to SQL table
                   Final_Result_Question.objects.filter(user_id = user_id,survey=survey,area = questionareas_area_id[j]).update(scores = answers_values_int[j])


        choices = create_context[1] #get list of choices to pass from create_context
        divcontext = Area.objects.values_list('divcontext', flat=True) #Get the divcontext values for each item in the results to align color with boxes
        area_and_overall_colors = determine_score(questionareas_area_id,answers_values_int,choices) #Get backgroundcolors for areas based on results
        area_colors = list(area_and_overall_colors[0]) ## get colors for context for radar plot and flowchart
        overall_color = area_and_overall_colors[1] # get colors for context for flowchart
        project = create_context[3] #Get project (survey) name to pass to radarplot store in Final_Result
    
        radar_data = radarplot(area_and_overall_colors,survey,user_id,company,project)
        area_name = radar_data[0]
        area_scores = radar_data[1]
        max_scores = radar_data[2]
        opacity= 1 # Set opacity to show outcome color on wheel
        #oc=Surveys.objects.filter(context=id).update(color=overall_color, opacity=opacity)
        oc_user=Outcome_Colors.objects.filter(user=user_id).filter(path=id).update(color=overall_color, opacity=opacity)
        divcontext_colors_zip = list(zip(divcontext,area_colors))# great tuple with divconetxt and color to use in results css 
       # Context for flow digram
        context_results ={
            "respondent_id": user_name,
            #"comment": results_comments, #Add in when comments added back
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


@login_required(login_url='login')
def wheel(request):
    return render(request,'ISO22301/wheel.html')


def createheader(n,id): # n is the value to use in lists created here, refers to teh ISO being generated Id is survey
    survey_id=Surveys.objects.filter(context=id).values_list("id", flat=True) #Get survey id for path
    survey_title_list=list(Surveys.objects.filter(context=id).values_list("survey", flat=True)) #Getlist of surveys
    survey_title=survey_title_list[0]#Get text from list as flat text file for use in HTML rendering by reemoving [' '] from text
    survey_id_int=survey_id.first() #extract integer value
    #Name of browser tab
    browsertab=list(Dashboard.objects.values_list('company', flat=True))
    browsertab=browsertab[n]
        #Name of dashboard
    dashboard_title=list(Dashboard.objects.values_list('dashboard', flat=True))
    dashboard_title=dashboard_title[n]
    # names and text for both ends of LoO to extract value for current project
    project=list(Project.objects.filter(survey_id=survey_id_int).values_list('project', flat=True))  #new
    projecttext=list(Project.objects.filter(survey_id=survey_id_int).values_list('project_text', flat=True))
    outcome=list(Project.objects.filter(survey_id=survey_id_int).values_list('outcome', flat=True))
    outcometext=list(Project.objects.filter(survey_id=survey_id_int).values_list('outcome_text', flat=True))
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
    column_header=column_header[1:] #Remove Not Sure form column header list by slicing list
    nchoices = []
    for n in range(num_choices_total):
        nchoices.append(n)
    surveytopics = Area.objects.filter(survey=survey_id_int).all() #used in layout to enter topics in flexbox
    areas =  Area.objects.filter(survey=survey_id_int).all().prefetch_related('question_set') #Get list of areas tied to question set
    textname= ["Enter comments here"] #Comment feild text
    context_header = {
        "textname": textname,
        "area": areas,
        "surveytopics": surveytopics,
        "browsertab": browsertab,
        "dashboard_title": dashboard_title,
        "project": project,
        "projecttext": projecttext,
        "outcome": outcome,
        "outcometext": outcometext,
        "nchoices": nchoices,
        "columnheader": column_header,
        "surveytitle": survey_title
        }
    return context_header, nchoices, survey_id_int, project


def determine_score(area, values, choices): 
 
    area_frequency = list(Counter(area).values()) # count frequency of questions in each areas convereted to list to 
    # be used to determine how often to iterate each area when determining the area's score
    area_total = sum(area_frequency) # get total number of questions
    num_areas = len(Counter(area)) #determine number of areas via counter()
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

    return score_result, overall_color, area_scores, max_score
    
def score_color(score): #Determine what color to shade scored area

    if score > .7:
        color = "Green"
    elif score < .3:
        color = "Red"
    else:
        color = "Yellow"
    return color

def score_color_overall(score): #Determine what color to shade survey overall

    if score > .7:
        color = "Green"
    elif score < .3:
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
                return redirect('wheel')
            else:
                form = LoginForm()
                messages.error(request,'Please enter a valid username and password')
                return render(request,'ISO22301/login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request,'ISO22301/login.html', {'form': form},)

@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return render(request,'ISO22301/logout.html',)

def radarplot(area_and_overall_colors,survey,user_id,company,project): #Create final radar plot

    #create data and names for radar plot to display in clockwise order
    area_scores = list(area_and_overall_colors[2]) # get scores for context for radar plot, convert to list to allow JSON to work properly
    #Order scores for graph to appear clockwise
    top_value = area_scores.pop(0) #Get value to be on top of plot
    area_scores.append(top_value) # Add top value to end of list so it will be on top of plot when reversed
    area_scores.reverse() # Reverse list to display clockwise on radar plot
    max_scores = int(area_and_overall_colors[3]) # get max score value for context for radar plot
    area_name_qs = Area.objects.filter(survey_id = survey).values_list('area', flat=True) #Get the area name for radar chart as Query Set
    area_name =list(area_name_qs) # convert Query Set to list for use in tempalte js
    #Order labels for graph so names appear clockwise
    top_label = area_name.pop(0) #Get value to be on top of plot
    area_name.append(top_label) # Add top value to to end of list so it will be on top of plot when reversed
    area_name.reverse()# Reverse list to disply clockwise on radar plot
    n = len(area_name) # determine area length to use in for loop
    overall_color=area_and_overall_colors[1] # Get color for survey
    area_colors = area_and_overall_colors[0] # Get color for each area
    # Order colors for grah so to appear clockwise
    top_value = area_colors.pop(0) #Get value to be on top of plot
    area_colors.append(top_value) # Add top value to end of list so it will be on top of plot when reversed
    area_colors.reverse() # Reverse list to display clockwise on radar plot

    respondent=Respondent.objects.filter(user_id=user_id).values_list('respondent', flat=True)# get name of person taking survey to put in final_result
    user = Final_Result.objects.filter(user_id=user_id,survey = survey) #get QuerySet for user to see if data already exists
    if not user: # if no data exists in Final_Results create data entry
        for x in range(n):
            area_id=Area.objects.filter(survey = survey, area = area_name[x]).values_list('id', flat=True) #Get Arear_id to add to data for later analysis by area using integer valeu of id ratehr than name
            data=Final_Result(user_id = user_id,area = area_name[x],scores = area_scores[x],area_color = area_colors[x],max_scores = max_scores, survey = survey, company = company, area_id=area_id, survey_name = project, overall_color = overall_color, length = n, respondent=respondent)
            data.save()
    else: #If data exists update to latets answers from user
       for x in range(n):
            data=Final_Result.objects.filter(user_id = user_id,survey=survey,area = area_name[x]).update(scores = area_scores[x],area_color = area_colors[x], overall_color = overall_color)

    return area_name, area_scores, max_scores

@login_required(login_url='login')
def results_overall(request):
    #Generate 3 results graphs
    user_id=request.user.id #get current user to identify data to use
    browsertaball= Final_Result.objects.filter(user_id = user_id).all().values_list('company', flat =  True)
    browsertab = browsertaball[0]
    dashboard_title=list(Dashboard.objects.values_list('dashboard', flat=True))
    dashboard_title=dashboard_title[0]
    survey = Surveys.objects.all() #get all survey names
    survey_results = Final_Result.objects.filter(user_id = user_id).all().order_by('survey') #Get all tle results for a particular user, ordered by survey ascending

    survey_results_survey = survey_results.values_list('survey', flat=True) #Get list of survey to get unique results set to plot
    survey_results_max = list(set(survey_results.values_list('max_scores', flat=True))) #Get max value
    unique_surveys = list(set(survey_results_survey)) #Create list with only unique survey id by removing duplicates and use to create data sets for echarts
   
    survey=[*survey.values_list('survey',flat=True)] # gets list in format ['value0','value1'...]
    #get unique set of values for each plot
    survey_results_area1 = list(survey_results.filter(survey=unique_surveys[0]).values_list('area', flat=True))
    survey_results_area2 = list(survey_results.filter(survey=unique_surveys[1]).values_list('area', flat=True))
    survey_results_area3 = list(survey_results.filter(survey=unique_surveys[2]).values_list('area', flat=True))
    survey_results_scores1 = list(survey_results.filter(survey=unique_surveys[0]).values_list('scores', flat=True))
    survey_results_scores2 = list(survey_results.filter(survey=unique_surveys[1]).values_list('scores', flat=True))
    survey_results_scores3 = list(survey_results.filter(survey=unique_surveys[2]).values_list('scores', flat=True))
    survey_results_colors1 = list(survey_results.filter(survey=unique_surveys[0]).values_list('area_color', flat=True))
    survey_results_colors2 = list(survey_results.filter(survey=unique_surveys[1]).values_list('area_color', flat=True))
    survey_results_colors3 = list(survey_results.filter(survey=unique_surveys[2]).values_list('area_color', flat=True))
 
    # Get survey lengths for use in for loops in echart 
    survey_length = []
    length=len(survey_results_area1)
    survey_length.append(length)
    length=len(survey_results_area2)
    survey_length.append(length)
    length=len(survey_results_area3)
    survey_length.append(length)

    #create list of outcome colors
    outcomecolorvalue1 = list(set(survey_results.filter(survey=unique_surveys[0]).values_list('overall_color', flat=True)))
    outcomecolorvalue2 = list(set(survey_results.filter(survey=unique_surveys[1]).values_list('overall_color', flat=True)))
    outcomecolorvalue3 = list(set(survey_results.filter(survey=unique_surveys[2]).values_list('overall_color', flat=True)))

    outcome_color=outcomecolorvalue1+outcomecolorvalue2+outcomecolorvalue3 # Combine into one list in proper order

    #Create text columns for display under graphs
    table_header = [('Area', 'Value', 'Status')] # Create header for each table

    results_text1 = [(x, y, z) for x, y, z in zip (survey_results_area1, survey_results_scores1, survey_results_colors1)]
    top=results_text1.pop(0) # Remove first set of values to get list in proper display order
    results_text1.append(top) # Add to end; list will be dispalyed in resed order in HTML Template

    results_text2 = [(x, y, z) for x, y, z in zip (survey_results_area2, survey_results_scores2, survey_results_colors2)]
    top=results_text2.pop(0) # Remove first set of values to get list in proper display order
    results_text2.append(top) # Add to end; list will be dispalyed in resed order in HTML Template

    results_text3 = [(x, y, z) for x, y, z in zip (survey_results_area3, survey_results_scores3, survey_results_colors3)]
    top=results_text3.pop(0) # Remove first set of values to get list in proper display order
    results_text3.append(top) # Add to end; list will be dispalyed in resed order in HTML Template
 
    #add headers to each table
    #results_text1 = results_text1 + table_header
    #results_text2 = results_text2 + table_header
    #results_text3 = results_text3 + table_header
    analysis_raw= chatgpt_analysis(user_id) #Get analysis results
    analysis_raw1=analysis_raw.replace("**","")
    analysis_raw2=analysis_raw1.replace("Key Strengths","<strong>Relative Strengths: </strong>")
    analysis_raw3=analysis_raw2.replace("Summary of Results","<strong>Overall Results: </strong>")
    analysis_raw4=analysis_raw3.replace("Summary of","")
    analysis=analysis_raw4.replace("Key Weaknesses","<strong>Relative Weaknesses: </strong>")
    analysis_data = Analysis_Final(user_id = user_id, analysis = analysis)
    analysis_data.save()
    context = {
        'area_name1': survey_results_area1,
        'area_scores1': survey_results_scores1,
        'survey_length': survey_length,
        'survey_max': survey_results_max,
        'area_name2': survey_results_area2,
        'area_scores2': survey_results_scores2,
        'area_name3': survey_results_area3,
        'area_scores3': survey_results_scores3,
        'browsertab': browsertab,
        'dashboard_title': dashboard_title,
        'survey_name': survey,
        'outcome_color':outcome_color,
        'results_text1': results_text1,
        'results_text2': results_text2,
        'results_text3': results_text3,
        'table_header': table_header,
        'analysis': analysis,



        }
    return render(request,'ISO22301/results_overall.html', context)

def chatgpt_analysis(user_id): #Send data to analyze_results to get ChatGPT analaysis
    results_dict={} #create dictionary of results
    results_dict=Final_Result_Question.objects.filter(user_id = user_id).values_list('area','question', 'scores')

    analysis = analyze_results(results_dict)
    return analysis

def analyze_results(results_dict): # Use Chat GPT to summarize results
    #prompt = f"provide a one paragraph summary of the results, a one paragraph summary of the key strengths and a one paragraph summary of the key weaknesses for  ISO survey results: {results_dict}" #Set prompt from user
    #Pass data and prompt to chatGPT
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    prompt = f"provide a two paragraph summary of the results,a two paragraph summary  of key strengths, and a  two paragraph summary summary of key weaknesses  based on ISO survey results where the maximum possible score is 5: Please return your answer with <br></br> bewteen each summary items, bold the title Do not use the words ISO, survey, proactively, or proactive, do not give score values in output{results_dict}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # or "gpt-3.5-turbo"
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2000
    )
    results = response.choices[0].message.content # Get results
    
    return results
