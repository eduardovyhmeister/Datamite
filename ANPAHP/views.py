from django.shortcuts import render, redirect
# Create your views here.
import calendar
from calendar import HTMLCalendar
from datetime import datetime as my_datetime
from .models import *
from .forms import *

from django.http import HttpResponseRedirect, FileResponse # this is to redirect to a specific page after submission
from django.http import HttpResponse # create different responses.

from django.contrib import messages #this allows to create one time messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required #this settle wat pagges are required to be loggin in order to access it .. use "@login_required(login_urls='name_of_url')
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
import base64
from django.forms import modelformset_factory, inlineformset_factory
import pandas as pd
import io
import itertools
import numpy as np
import json

from itertools import combinations
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from pyanp import limitmatrix as lm

########################### auxiliar functions ######################

def get_graph(): #this is a function to embed views with grapbhs automatically from database.
    buffer = BytesIO()
    plt.savefig(buffer,format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def transform_list(original_list): 
    ''' Create a mapping from original number to the new smallest unique number'''
    unique_numbers = sorted(set(num for sublist in original_list for num in sublist))
    num_mapping = {num: i + 1 for i, num in enumerate(unique_numbers)}
    transformed_list = [[num_mapping[num] for num in sublist] for sublist in original_list]
    return transformed_list

def generate_pairs_as_lists(data):
    result = {}
    for key, value in data.items():
        result[key] = []
        for sublist in value:
            if len(sublist) > 1:
                pairs = list(combinations(sublist, 2))
                result[key].extend(list(pair) for pair in pairs)
            else:
                result[key].append(sublist)
    return result

def merge_unique_values(data):
    result = {}
    for key, value in data.items():
        unique_elements = set()
        for sublist in value:
            unique_elements.update(sublist)
        result[key] = [list(unique_elements)]
    return result

def ponder_and_normalize(list_of_lists, weighting_factors):
    # Initialize a list to store the pondered values
    pondered_values = []

    # Ponder each sublist by the corresponding weighting factor
    for sublist, weight in zip(list_of_lists, weighting_factors):
        pondered_sublist = [element * weight for element in sublist]
        pondered_values.append(pondered_sublist)

    # Calculate the total sum of all pondered values
    total_sum = sum(sum(sublist) for sublist in pondered_values)

    # Normalize the pondered values
    normalized_values = []
    for pondered_sublist in pondered_values:
        if total_sum == 0:
            normalized_values.append(pondered_sublist)  # Preserve the pondered values if total sum is zero
        else:
            normalized_values.append([element / total_sum for element in pondered_sublist])

    return normalized_values


def numerate_names(data):
    name_to_number = {}  # Dictionary to store name-number mapping
    next_number = 1  # Initial number to assign
    numerated_data = []  # List to store numerated lists
    for sublist in data:
        numerated_sublist = []  # List to store numerated sublist
        for name in sublist:
            if name not in name_to_number:
                name_to_number[name] = next_number
                next_number += 1
            numerated_sublist.append(name_to_number[name])
        numerated_data.append(numerated_sublist)
    return numerated_data

def make_radar_chart(stats,labels,plot_markers = None):
    plt.switch_backend('AGG')
    fig=plt.figure(figsize=(5,5))
    attribute_labels=labels #List of names
    if plot_markers == None:
        plot_markers =[0,.2,0.4,0.6,0.8,1,]
    plot_str_markers=['0','0.2','0.4','0.6','0.8','1']
    angles = np.linspace(0, 2*np.pi, len(attribute_labels), endpoint=False)
    ax = fig.add_subplot(111, polar=True)
    ax.plot(angles, stats, 'o-', linewidth=2)
    ax.fill(angles, stats, alpha=0.25)
    ax.set_thetagrids(angles * 180/np.pi, attribute_labels)
    ax.tick_params(labelsize=8)
    plt.yticks(plot_markers)
    ax.set_title('ANP Results')
    ax.grid(True)
    graph = get_graph()
    return graph

def make_trend_chart(df,names,title,ticks):
    plt.switch_backend('AGG')
    fig=plt.figure(figsize=(5,5))
    ax = fig.add_subplot(111)
    ax = df[names].plot(kind='box',title=title)
    ax.set_xticklabels(ticks)
    #plt.setp(ax, xticks=[np.random.normal(0, std, 100) for std in range(6, 10)], xticklabels=labels)
    graph = get_graph()
    return graph


def construct_matrix(selection,elements,dim=None):
    if len(selection)>1:
        matrix_size = dim if dim is not None else max(max(sublist) for sublist in elements)
        matrix = np.eye(matrix_size)
        
        for i in range(len(selection)):
            if selection[i]<0:
                value = 1/(abs(selection[i])+1)
            else:
                value = selection[i]+1
            
            matrix[elements[i][0]-1,elements[i][1]-1] = 1/value
            matrix[elements[i][1]-1,elements[i][0]-1] = value

    # eigenvalues and vectors
    elif len(selection) == 1:
        matrix = np.eye(2)
        value = 1 / (abs(selection[0]) + 1) if selection[0] < 0 else selection[0] + 1
        matrix[0,1] = value
        matrix[1,0] = 1/value

    else:
        matrix = np.array([[1]])
    print(elements)
    print(max(max(sublist) for sublist in elements))
    # eliminate rows and columns that contain 0,s
    #rows_to_keep = ~np.any(matrix == 0, axis=1)
    #columns_to_keep = ~np.any(matrix == 0, axis=0)
    #matrix = matrix[np.ix_(rows_to_keep, columns_to_keep)]
    #print(matrix)

    eigenvalues, eigenvectors = np.linalg.eig(matrix)
    principal_eigenvalue_index = np.argmax(eigenvalues)
    principal_eigenvector = eigenvectors[:, principal_eigenvalue_index]
    normalized_eigenvector = np.abs(principal_eigenvector) / np.sum(np.abs(principal_eigenvector))
    eig_vec = normalized_eigenvector.real
    eig_val = eigenvalues.max().real
    try:
        inconcistency = (eig_val-len(eigenvalues))/(len(eigenvalues)-1)
    except:
        inconcistency = 0.0
    return matrix, eig_vec, inconcistency

def EXECUTE_ANALYSIS(ANPAHP):
    try:
        supermatrix = eval(ANPAHP.supermatrix)
    except:
        supermatrix = ANPAHP.supermatrix
    supermatrix = np.array(supermatrix,dtype=float)
    columns_analysis = [1 if i == 0 else 0 for i in np.sum(supermatrix[:,1:5], axis=0)]
    if sum(columns_analysis) != 0:
        original = supermatrix[1:5,0]
        operated = [original[i] if k == 0 else 0 for (i,k) in enumerate(columns_analysis)]
        operated = np.abs(operated) / np.sum(np.abs(operated))
        supermatrix[1:5,0] = operated

    try:
        limitingmatrix = lm.calculus(supermatrix)
        hierarchy = lm.hiearhcy_formula(supermatrix)
        lista1 = limitingmatrix.tolist()
        lista2 = hierarchy.tolist()
    except:
        lista1 =[]
        lista2 = []
    return lista1,lista2, supermatrix


###############     register view
def UserRegisterView(request):
    form = RegisterForm

    if request.method == 'POST': 
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user =form.cleaned_data.get('username')
            messages.success(request,'Account was created for ' + user)
            return redirect('login')
    context = {'form':form}
    return render(request,'registration.html',context)



def UserLoginView(request):

    if request.method =="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        user =authenticate(request,username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Username or Password is incorrect')

    context = {}
    return render(request,'login.html',context)



def UserLogout(request):
    logout(request)
    return redirect('login')



#################### create new element

def home(request,year=my_datetime.now().year,month=my_datetime.now().strftime('%B')):
    name=""
    month =month.capitalize()
    #convert month from name to number
    month_number = list(calendar.month_name).index(month)
    cal =HTMLCalendar().formatmonth(year,month_number)


    return render(request,'home.html',{"first_name":name,
                                        "year":year,
                                        "month":month,
                                        "month_number":month_number,
                                        "cal":cal,
                                        })

def HowToAltai(request):
    context = {}
    return render(request,'howToAltai.html',context)

def FundamentalRights(request):
    context = {}
    return render(request,'fundamentalRights.html',context)

def HowToANPAHP(request):
    context = {}
    return render(request,'howToANPAHP.html',context)

def About(request):
    context = {}
    return render(request,'about.html',context)

def Privacy(request):
    context = {}
    return render(request,'privacy.html',context)


################# altai views
def MyANPAHP(request):
     ANPAHPs = EVALUATION.objects.all().filter(author=request.user)
     context = {'ANPAHPs':ANPAHPs}
     return render(request,'ANPAHP/myANPAHP.html',context)

def MyANPAHPCreate(request):
    submitted = False
    if request.method == "POST":
        form=ANPAHPForm(request.POST)
        if form.is_valid():
            assessment=form.save(commit=False) # this create the form but do not commit it so can be modified
            assessment.author = request.user # modify the form
            assessment.save()
            return HttpResponseRedirect('myANPAHP') # /add_event?submitted=True
    else:
        form=ANPAHPForm
        if 'submitted' in request.GET:
            submitted = True
    form=ANPAHPForm
    return render(request,'ANPAHP/myANPAHPCreate.html',{'form':form, 'submitted':submitted})

@login_required
def MyANPAHPDelete(request,pk):
    altai = EVALUATION.objects.get(pk=pk)
    altai.delete()
    return redirect('myANPAHP')

@login_required
def MyANPAHPHome(request,pk):
    ANPAHP = EVALUATION.objects.get(pk=pk)
    form = NotesForm(request.POST or None, instance=ANPAHP)
    if form.is_valid():
        form.save()
        return render(request,'ANPAHP/ANPAHPHome.html',{'ANPAHP':ANPAHP,'form':form})
    return render(request,'ANPAHP/ANPAHPHome.html',{'ANPAHP':ANPAHP,'form':form})

@login_required
def NewKPI(request,pk):
    ANPAHP = EVALUATION.objects.get(pk=pk)
    submitted = False
    if request.method == "POST":
        formout=NewKPIForm(request.POST)
        if formout.is_valid():
            KPI=formout.save(commit=False) # this create the form but do not commit it so can be modified
            KPI.author = request.user # modify the form
            KPI.save()
            submitted=True
            return redirect('myANPAHPStep2',pk=pk)
        else:
           message = 'Make sure that the name of the KPI is unique and the explanation does not match other KPIs.'
        return render(request, 'ANPAHP/newKPI.html', {'form': formout, 'submitted': submitted, 'ANPAHP': ANPAHP, 'message': message})
    else:
        formin=NewKPIForm()
        return render(request,'ANPAHP/newKPI.html',{'form':formin, 'submitted':submitted, 'ANPAHP':ANPAHP})

@login_required
def NewObjectives(request,pk):
    ANPAHP = EVALUATION.objects.get(pk=pk)
    submitted = False
    if request.method == "POST":
        form=NewObjectivesForm(request.POST)
        if form.is_valid():
            KPI=form.save(commit=False) # this create the form but do not commit it so can be modified
            KPI.author = request.user # modify the form
            KPI.save()
            submitted=True
            return render(request,'ANPAHP/newObjectives.html',{'form':form, 'submitted':submitted, 'ANPAHP':ANPAHP})
    form=NewObjectivesForm()
    return render(request,'ANPAHP/newObjectives.html',{'form':form, 'submitted':submitted, 'ANPAHP':ANPAHP})

@login_required
def NewCriteria(request,pk):
    ANPAHP = EVALUATION.objects.get(pk=pk)
    submitted = False
    if request.method == "POST":
        formout=NewCriteriaForm(request.POST)
        if formout.is_valid():
            KPI=formout.save(commit=False) # this create the form but do not commit it so can be modified
            KPI.author = request.user # modify the form
            KPI.save()
            submitted=True
            return redirect('myANPAHPStep7',pk=pk)
        else:
            message = 'Make sure that the name of the KPI is unique and the explanation does not match other KPIs.'
            return render(request, 'ANPAHP/newCriteria.html', {'form': formout, 'submitted': submitted, 'ANPAHP': ANPAHP, 'message': message})
    else:
        formin=NewCriteriaForm()
        return render(request,'ANPAHP/newCriteria.html',{'form':formin, 'submitted':submitted, 'ANPAHP':ANPAHP})


############# Objectives/Strategies

@login_required
def MyANPAHPStep1(request,pk): # ex 6
    
    ANPAHP = EVALUATION.objects.get(pk=pk)
    form = Step6Form(request.POST or None, instance=ANPAHP)
    ids = eval(ANPAHP.SelectedObjectives)
    lista = [True if x+1 in ids else False for x in range(Objective.objects.all().count())]
    ERROR = False
    if ANPAHP.status1 == False:
        ERROR = True
    if request.method == "POST":
        selection =[]
        
        #selection = list(map(int,request.POST.getlist('Failure')))
        KPIs=Objective.objects.all().values_list('name',flat=True)
        for j in range(len(KPIs)):
            selection+=list(map(int,request.POST.getlist(str(j+1))))
        if form.is_valid() and len(selection)==1:
            ANPAHP.SelectedObjectives = selection
            ANPAHP.shapes = {"Objectives":1, "Criterias":0,"KPIs":0, "BSC":4}
            ANPAHP.message = ''
            ANPAHP.save()
            form.save()
            return redirect('myANPAHPStep1_2',pk=pk)
        else:
            message = 'You have to choose ONE OBJECTIVE / Strategies'
            ERROR = True
            ANPAHP.status1 = False
            ANPAHP.save()
            return render(request,'ANPAHP/ANPAHPStep1.html',{'ANPAHP':ANPAHP,'form':form,'ids':ids,'lista':lista,'message':message,'message2':ANPAHP.message,'ERROR1':ERROR})
    return render(request,'ANPAHP/ANPAHPStep1.html',{'ANPAHP':ANPAHP,'form':form,'ids':ids,'lista':lista,'message2':ANPAHP.message,'ERROR1':ERROR})



@login_required
def MyANPAHPStep1_2(request,pk): # ex 2
    ANPAHP = EVALUATION.objects.get(pk=pk)
    ERROR1 = False
    ERROR2 = False
    message = ''
    if len(ANPAHP.message)!=0:
        ERROR2 = True
    if request.method == "POST":
        selection = []
        for j in range(6):
            id_list = request.POST.getlist(str(j+1))
            selection+=list(map(float,id_list))
        elements = [(2,1),(3,1),(4,1),(3,2),(4,2),(4,3)]
        matrix, vector, inconcistency = construct_matrix(selection,elements,dim=4)
        if abs(inconcistency) < 0.4:
            print(inconcistency)
            ANPAHP.status1 = True
            ANPAHP.BSC_Weights = vector.tolist()
            ANPAHP.save()
            return redirect('myANPAHPStep2',pk=pk)
        else:
            ANPAHP.status1 = False
            message = f'There is huge inconcistency  ({inconcistency}) in the information provided. Please re-evaluate.'
            ERROR1 = True
            return render(request,'ANPAHP/ANPAHPStep1_2.html',{'ANPAHP':ANPAHP,'message':message,'message2':ANPAHP.message,'ERROR1':ERROR1,'ERROR2':ERROR2})
    else:
        return render(request,'ANPAHP/ANPAHPStep1_2.html',{'ANPAHP':ANPAHP,'message':message,'message2':ANPAHP.message,'ERROR1':ERROR1,'ERROR2':ERROR2})



########### KPIs Selection

@login_required
def MyANPAHPStep2(request,pk): # ex1
    ANPAHP = EVALUATION.objects.get(pk=pk)
    form = Step1Form(request.POST or None, instance=ANPAHP)
    ids = eval(ANPAHP.SelectedKPIs)
    KPIs=KPI.objects.all().values_list('name',flat=True).order_by('id')
    if ids!=None and len(ids)!=0:
        merged_list = [item for sublist in ids.values() for item in sublist]
    else:
        merged_list = []
    lista = [True if x+1 in merged_list else False for x in range(len(KPIs))]
    if request.method == "POST" and ANPAHP.status1 == True:
        selection =[]
        for j in range(len(KPIs)):
            selection+=list(map(int,request.POST.getlist(str(j+1))))
        if form.is_valid() and len(selection)!=0 and ANPAHP.status1:
            supermatrix = np.zeros(shape=(len(selection)+5,len(selection)+5)).tolist()
            for num,content in enumerate(eval(ANPAHP.BSC_Weights)):
                supermatrix[1+num][0] = content
            ANPAHP.supermatrix = str(supermatrix)
            Drivers = list(KPI.objects.all().values_list('BSCfamily',flat=True))
            groups,combinations = {key: [] for key in ['Customer','Financial','Education and Growth','Internal Processes']}, {}
            for i in range(len(selection)):
                groups[Drivers[selection[i]-1]].append(selection[i])
            for key, indexes in groups.items():
                combinations[key] = list(itertools.combinations(indexes,2))
            ANPAHP.SelectedKPIs = groups
            ANPAHP.pairwise_combinations = combinations
            shapes = eval(ANPAHP.shapes)
            shapes["KPIs"] = len(selection)
            ANPAHP.shapes = shapes
            ANPAHP.status2 = True
            ANPAHP.message = ''
            ANPAHP.save()
            form.save()
            return redirect('myANPAHPStep3',pk=pk)
        elif not ANPAHP.status1:
            ANPAHP.message = 'There are modifications or missing information in previous stages, You have to define them before continue here'
            ANPAHP.status2 = False
            ANPAHP.save()
            return redirect('myANPAHPStep1',pk=pk)
        else:
            ANPAHP.message = 'You have to choose at least one KPI'
            ANPAHP.stats2 = False
            ANPAHP.save()
            return render(request,'ANPAHP/ANPAHPStep2.html',{'ANPAHP':ANPAHP,'form':form,'ids':ids,'lista':lista,'message':ANPAHP.message})
    if ANPAHP.status1 == False:
        ANPAHP.message = 'There are modifications or missing information in previous stages, Make Sure to Select and Objective'
        ANPAHP.save()
        return redirect('myANPAHPStep1',pk=pk)
    return render(request,'ANPAHP/ANPAHPStep2.html',{'ANPAHP':ANPAHP,'form':form,'ids':ids,'lista':lista})

########### KPIs Customer
@login_required
def MyANPAHPStep3(request,pk): # ex 2
    ANPAHP = EVALUATION.objects.get(pk=pk)
    pairs = ANPAHP.pairwise_combinations
    names = list(KPI.objects.all().values_list('name',flat=True).order_by('id'))
    ids1, ids2, ids2names = [], [], []
    SelectedKPIs = eval(ANPAHP.SelectedKPIs)
    supermatrix = eval(ANPAHP.supermatrix)
    form = Step2Form(request.POST or None, instance=ANPAHP)
    ERROR1 = False
    ERROR2 = False
    if len(ANPAHP.message)!=0:
        ERROR2 = True
    if len(pairs['Customer']) > 0 :
        print(pairs)
        print(names)
        for elements in pairs['Customer']:
            ids1.append(elements[0])
            ids2.append(elements[1])
            ids2names.append(names[elements[1]-1])
        if request.method == "POST":
            selection=[]
            for j in range(len(ids1)):
                id_list = request.POST.getlist(str(j+1))
                selection+=list(map(float,id_list))
            matrix, vector, inconcistency = construct_matrix(selection,transform_list(pairs['Customer']))
            ANPAHP.Scores1 = json.dumps(matrix.tolist())
            ANPAHP.inconcistency1 = str(inconcistency)
            ANPAHP.vector1 = json.dumps(vector.tolist())
            for index, value in enumerate(vector):
                supermatrix[5+index][1] = value
            if form.is_valid() and abs(inconcistency) < 0.4 and ANPAHP.status1 and ANPAHP.status2:
                ANPAHP.supermatrix = str(supermatrix)
                ANPAHP.status3 = True
                ANPAHP.message = ''
                ANPAHP.save()
                form.save()
                return redirect('myANPAHPStep4',pk=pk)
            elif not ANPAHP.status1 or not ANPAHP.status2:
                ANPAHP.message = 'There are modifications or missing information in previous stages, You have been returned Missing steps'
                ANPAHP.save()
                return redirect('myANPAHPStep2',pk=pk)
            else:
                ERROR1 = True
                message = f'There is huge inconcistency in the information provided {inconcistency}. Please re-evaluate the information provided'
                return render(request,'ANPAHP/ANPAHPStep3.html',{'ANPAHP':ANPAHP,'form':form,'ids1':ids1,'ids2':ids2,'ids2names':ids2names,'message':message,'message2':ANPAHP.message,'ERROR1':ERROR1,'ERROR2':ERROR2})
        else:
            return render(request,'ANPAHP/ANPAHPStep3.html',{'ANPAHP':ANPAHP,'form':form,'ids1':ids1,'ids2':ids2,'ids2names':ids2names,'ERROR2':ERROR2,'message2':ANPAHP.message})
    elif len(SelectedKPIs['Customer']) == 1:
        supermatrix[5][1] == 1
        ANPAHP.supermatrix == str(supermatrix)
        ANPAHP.Scores1, ANPAHP.inconcistency1,ANPAHP.vector1 = json.dumps([1]), str(0), json.dumps([1])
        ANPAHP.status3 = True
        ANPAHP.save()
        return redirect('myANPAHPStep4',pk=pk)
    else:
        ANPAHP.Scores1, ANPAHP.inconcistency1,ANPAHP.vector1 = json.dumps([]), np.nan, json.dumps([])
        ANPAHP.status3 = True
        ANPAHP.save()
        return redirect('myANPAHPStep4',pk=pk)

# THIS IS THE FOR FOR Financial
@login_required
def MyANPAHPStep4(request,pk): # ex3
    ANPAHP = EVALUATION.objects.get(pk=pk)
    pairs = ANPAHP.pairwise_combinations
    names = list(KPI.objects.all().values_list('name',flat=True).order_by('id'))
    ids1, ids2, ids2names = [], [], []
    SelectedKPIs = eval(ANPAHP.SelectedKPIs)
    supermatrix = eval(ANPAHP.supermatrix)
    form = Step2Form(request.POST or None, instance=ANPAHP)
    ERROR1 = False
    ERROR2 = False
    if len(ANPAHP.message)!=0:
        ERROR2 = True
    if len(pairs['Financial']) > 0:
        for elements in pairs['Financial']:
            ids1.append(elements[0])
            ids2.append(elements[1])
            ids2names.append(names[elements[1]-1])
        if request.method == "POST":
            selection=[]
            for j in range(len(ids1)):
                id_list = request.POST.getlist(str(j+1))
                selection+=list(map(float,id_list))
            matrix, vector, inconcistency = construct_matrix(selection,transform_list(pairs['Financial']))
            print(f'the inconcistency is {inconcistency}')
            ANPAHP.Scores2 = json.dumps(matrix.tolist())
            ANPAHP.inconcistency2 = str(inconcistency)
            ANPAHP.vector2 = json.dumps(vector.tolist())
            for index, value in enumerate(vector):
                supermatrix[5+index+len(SelectedKPIs['Customer'])][2] = value
            if form.is_valid() and abs(inconcistency) < 0.4 and ANPAHP.status1 and ANPAHP.status2 and ANPAHP.status3:
                ANPAHP.status4 = True
                ANPAHP.supermatrix = str(supermatrix)
                ANPAHP.message = ''
                ANPAHP.save()
                form.save()
                return redirect('myANPAHPStep5',pk=pk)
            else:
                ERROR1 = True
                message = f'There is huge inconcistency in the information provided {inconcistency}. Please re-evaluate the information provided'
                return render(request,'ANPAHP/ANPAHPStep4.html',{'ANPAHP':ANPAHP,'form':form,'ids1':ids1,'ids2':ids2,'ids2names':ids2names,'message':message,'message2':ANPAHP.message,'ERROR1':ERROR1,'ERROR2':ERROR2})
        else:
            return render(request,'ANPAHP/ANPAHPStep4.html',{'ANPAHP':ANPAHP,'form':form,'ids1':ids1,'ids2':ids2,'ids2names':ids2names,'ERROR2':ERROR2,'message2':ANPAHP.message})
    elif len(SelectedKPIs['Financial']) == 1:
        supermatrix[5+len(SelectedKPIs['Customer'])][2] = 1.0
        ANPAHP.supermatrix = str(supermatrix)
        ANPAHP.Scores2, ANPAHP.inconcistency2,ANPAHP.vector2 = json.dumps([1]), str(0), json.dumps([1])
        ANPAHP.status4 = True
        ANPAHP.save()
        return redirect('myANPAHPStep5',pk=pk)
    else:
        ANPAHP.Scores2, ANPAHP.inconcistency2, ANPAHP.vector2 = json.dumps([]), str(np.nan), json.dumps([])
        ANPAHP.status4 = True
        ANPAHP.save()
        return redirect('myANPAHPStep5',pk=pk)

# THIS IS THE FOR FOR 'Education and Growth'
@login_required
def MyANPAHPStep5(request,pk): # ex4
    ANPAHP = EVALUATION.objects.get(pk=pk)
    pairs = ANPAHP.pairwise_combinations
    names = list(KPI.objects.all().values_list('name',flat=True).order_by('id'))
    ids1, ids2, ids2names = [], [], []
    SelectedKPIs = eval(ANPAHP.SelectedKPIs)
    supermatrix = eval(ANPAHP.supermatrix)
    ERROR1 = False
    ERROR2 = False
    if len(ANPAHP.message)!=0:
        ERROR2 = True
    if len(pairs['Education and Growth']) > 0:
        for elements in pairs['Education and Growth']:
            ids1.append(elements[0])
            ids2.append(elements[1])
            ids2names.append(names[elements[1]-1])
        form = Step2Form(request.POST or None, instance=ANPAHP)
        if request.method == "POST":
            selection=[]
            for j in range(len(ids1)):
                id_list = request.POST.getlist(str(j+1))
                selection+=list(map(float,id_list))
            matrix, vector, inconcistency = construct_matrix(selection,transform_list(pairs['Education and Growth']))
            ANPAHP.Scores3 = json.dumps(matrix.tolist())
            ANPAHP.inconcistency3 = str(inconcistency)
            ANPAHP.vector3 = json.dumps(vector.tolist())
            for index, value in enumerate(vector):
                supermatrix[5+index+len(SelectedKPIs['Customer'])+len(SelectedKPIs['Financial'])][3] = value
            if form.is_valid() and abs(inconcistency) < 0.4 and ANPAHP.status1 and ANPAHP.status2 and ANPAHP.status3 and ANPAHP.status4:
                ANPAHP.status5 = True
                ANPAHP.supermatrix = str(supermatrix)
                ANPAHP.message = ''
                ANPAHP.save()
                form.save()
                return redirect('myANPAHPStep6',pk=pk)
            else:
                ERROR1 = True
                message = f'There is huge inconcistency in the information provided {inconcistency}. Please re-evaluate the information provided'
                return render(request,'ANPAHP/ANPAHPStep5.html',{'ANPAHP':ANPAHP,'form':form,'ids1':ids1,'ids2':ids2,'ids2names':ids2names,'message':message,'message2':ANPAHP.message,'ERROR1':ERROR1,'ERROR2':ERROR2})
        else:
            return render(request,'ANPAHP/ANPAHPStep5.html',{'ANPAHP':ANPAHP,'form':form,'ids1':ids1,'ids2':ids2,'ids2names':ids2names,'ERROR2':ERROR2,'message2':ANPAHP.message})
    elif len(SelectedKPIs['Education and Growth']) == 1:
        supermatrix[5+len(SelectedKPIs['Customer'])+len(SelectedKPIs['Financial'])][3] = 1.0
        ANPAHP.supermatrix = str(supermatrix)
        ANPAHP.Scores1, ANPAHP.inconcistency1,ANPAHP.vector1 = json.dumps([1]), str(0), json.dumps([1])
        ANPAHP.status5 = True
        ANPAHP.save()
        return redirect('myANPAHPStep6',pk=pk)
    else:
        ANPAHP.Scores3, ANPAHP.inconcistency3, ANPAHP.vector3 = json.dumps([]), str(np.nan), json.dumps([])
        ANPAHP.status5 = True
        ANPAHP.save()
        return redirect('myANPAHPStep6',pk=pk)
    
# THIS IS THE FOR FOR 'Internal Processes'
@login_required
def MyANPAHPStep6(request,pk): # ex5
    ANPAHP = EVALUATION.objects.get(pk=pk)
    pairs = ANPAHP.pairwise_combinations
    names = list(KPI.objects.all().values_list('name',flat=True).order_by('id'))
    ids1, ids2, ids2names = [], [], []
    SelectedKPIs = eval(ANPAHP.SelectedKPIs)
    supermatrix = eval(ANPAHP.supermatrix)
    ERROR1 = False
    ERROR2 = False
    if len(ANPAHP.message)!=0:
        ERROR2 = True
    if len(pairs['Internal Processes']) > 0:
        for elements in pairs['Internal Processes']:
            ids1.append(elements[0])
            ids2.append(elements[1])
            ids2names.append(names[elements[1]-1])
        form = Step2Form(request.POST or None, instance=ANPAHP)
        if request.method == "POST":
            selection=[]
            for j in range(len(ids1)):
                id_list = request.POST.getlist(str(j+1))
                selection+=list(map(float,id_list))
            matrix, vector, inconcistency = construct_matrix(selection,transform_list(pairs['Internal Processes']))
            ANPAHP.Scores4 = json.dumps(matrix.tolist())
            ANPAHP.inconcistency4 = str(inconcistency)
            ANPAHP.vector4 = json.dumps(vector.tolist())
            for index, value in enumerate(vector):
                supermatrix[5+index+len(SelectedKPIs['Customer'])+len(SelectedKPIs['Financial'])+len(SelectedKPIs['Education and Growth'])][4] = value
            if form.is_valid() and abs(inconcistency) < 0.4  and ANPAHP.status1 and ANPAHP.status2 and ANPAHP.status3 and ANPAHP.status4 and ANPAHP.status5:
                ANPAHP.status6 = True
                ANPAHP.supermatrix = str(supermatrix)
                ANPAHP.message = ''
                ANPAHP.save()
                form.save()
                return redirect('myANPAHPStep7',pk=pk)
            else:
                ERROR1 = True
                message = f'There is huge inconcistency in the information provided {inconcistency}. Please re-evaluate the information provided'
                return render(request,'ANPAHP/ANPAHPStep6.html',{'ANPAHP':ANPAHP,'form':form,'ids1':ids1,'ids2':ids2,'ids2names':ids2names,'message':message,'message2':ANPAHP.message,'ERROR1':ERROR1,'ERROR2':ERROR2})
        else:
            return render(request,'ANPAHP/ANPAHPStep6.html',{'ANPAHP':ANPAHP,'form':form,'ids1':ids1,'ids2':ids2,'ids2names':ids2names,'ERROR2':ERROR2,'message2':ANPAHP.message})
    elif len(SelectedKPIs['Internal Processes']) == 1:
        supermatrix[5+len(SelectedKPIs['Customer'])+len(SelectedKPIs['Financial'])+len(SelectedKPIs['Education and Growth'])][4] = 1.0
        ANPAHP.supermatrix = str(supermatrix)
        ANPAHP.Scores1, ANPAHP.inconcistency1,ANPAHP.vector1 = json.dumps([1]), str(0), json.dumps([1])
        ANPAHP.status6 = True
        ANPAHP.save()
        return redirect('myANPAHPStep7',pk=pk)
    else:
        ANPAHP.Scores4, ANPAHP.inconcistency4, ANPAHP.vector4 = json.dumps([]), str(np.nan), json.dumps([])
        ANPAHP.status6 = True
        ANPAHP.save()
        return redirect('myANPAHPStep7',pk=pk)

    ############# Criterias

@login_required
def MyANPAHPStep7(request,pk):
    ANPAHP = EVALUATION.objects.get(pk=pk)
    form = Step8Form(request.POST or None, instance=ANPAHP)
    form.fields['Criterias'].queryset = Criteria.objects.all().order_by('id')
    Criterias=Criteria.objects.all().values_list('name',flat=True)
    ids = eval(ANPAHP.SelectedCriterias)
    lista = [True if x+1 in ids else False for x in range(len(Criterias))]
    if request.method == "POST":
        selection =[]
        for j in range(len(Criterias)):
            selection+=list(map(int,request.POST.getlist(str(j+1))))
        ANPAHP.status4 = True

        if form.is_valid() and len(selection)!=0 and ANPAHP.status1 and ANPAHP.status6:
            ANPAHP.SelectedCriterias = selection
            groups,combinations = {'Criteria':selection}, {}
            for key, indexes in groups.items():
                combinations[key] = list(itertools.combinations(indexes,2))
            supermatrix = eval(ANPAHP.supermatrix)
            shapes = eval(ANPAHP.shapes)
            shapes['Criterias'] = len(selection)
            ANPAHP.shapes = shapes
            if len(supermatrix) == shapes["KPIs"] + 5 or len(supermatrix)!=shapes["KPIs"] +5 +shapes["Criterias"]:
                if len(supermatrix)!=shapes["KPIs"] +5 +shapes["Criterias"]:
                    num = shapes["KPIs"] +5
                    supnp =np.array(supermatrix)
                    supermatrix = supnp[:num,:num].tolist()
                expanded_array = np.zeros((len(supermatrix)+len(selection),len(supermatrix)+len(selection)))
                expanded_array[:len(supermatrix), :len(supermatrix)] = np.array(supermatrix)
                ANPAHP.supermatrix = expanded_array.tolist()
            ANPAHP.pairwise_combinations_criterias = combinations
            ANPAHP.save()
            form.save()
            return redirect('myANPAHPStep8',pk=pk)
        elif ~ANPAHP.status1 or ANPAHP.status6:
            ANPAHP.message = 'There are modifications or missing information in previous stages, You have to define them before continue here'
            return redirect('myANPAHPStep6',pk=pk)
        else:
            message = 'You have to choose at least one Criteria'
            return render(request,'ANPAHP/ANPAHPStep7.html',{'ANPAHP':ANPAHP,'form':form,'ids':ids,'lista':lista,'message':message})
    return render(request,'ANPAHP/ANPAHPStep7.html',{'ANPAHP':ANPAHP,'form':form,'ids':ids,'lista':lista})

@login_required
def MyANPAHPStep8(request,pk):
    ANPAHP = EVALUATION.objects.get(pk=pk)
    pairs = ANPAHP.pairwise_combinations_criterias
    names = list(Criteria.objects.all().values_list('name',flat=True).order_by('id'))
    ids1, ids2, ids2names = [], [], []
    SelectedKPIs = eval(ANPAHP.SelectedKPIs)
    ERROR1 = False
    ERROR2 = False
    if len(ANPAHP.message)!=0:
        ERROR2 = True
    if len(pairs['Criteria']) > 0:
        for elements in pairs['Criteria']:
            ids1.append(elements[0])
            ids2.append(elements[1])
            ids2names.append(names[elements[1]-1])
        form = Step8Form(request.POST or None, instance=ANPAHP)
        form.fields['Criterias'].queryset = Criteria.objects.all().order_by('id')
        if request.method == "POST":
            selection=[]
            for j in range(len(ids1)):
                id_list = request.POST.getlist(str(j+1))
                selection+=list(map(float,id_list))
            matrix, vector, inconcistency = construct_matrix(selection,transform_list(pairs['Criteria']))
            ANPAHP.Scores5 = json.dumps(matrix.tolist())
            ANPAHP.inconcistency5 = str(inconcistency)
            ANPAHP.vector5 = json.dumps(vector.tolist())
            supermatrix = eval(ANPAHP.supermatrix)
            for index, value in enumerate(vector):
                supermatrix[5+index+len(SelectedKPIs['Customer'])+len(SelectedKPIs['Financial'])+len(SelectedKPIs['Education and Growth'])+len(SelectedKPIs['Internal Processes'])][0] = value
            supnp= np.array(supermatrix)
            if np.sum(supnp[:,0]) != 1:
                supnp[:,0] = supnp[:,0]/np.sum(supnp[:,0])
            ANPAHP.supermatrix = supnp.tolist()
            if form.is_valid() and inconcistency < 0.4:
                ANPAHP.status7 = True
                ANPAHP.message = ''
                ANPAHP.save()
                form.save()
                return redirect('myANPAHPStep9',pk=pk)
            else:
                ERROR1 = True
                message = f'There is huge inconcistency in the information provided {inconcistency}. Please re-evaluate the information provided'
                return render(request,'ANPAHP/ANPAHPStep8.html',{'ANPAHP':ANPAHP,'form':form,'ids1':ids1,'ids2':ids2,'ids2names':ids2names,'message':message,'message2':ANPAHP.message,'ERROR1':ERROR1,'ERROR2':ERROR2})
        else:
            ANPAHP.message = 'There was a problem with it'
            return render(request,'ANPAHP/ANPAHPStep8.html',{'ANPAHP':ANPAHP,'form':form,'ids1':ids1,'ids2':ids2,'ids2names':ids2names,'ERROR2':ERROR2,'message2':ANPAHP.message})
    else:
        ANPAHP.Scores1, ANPAHP.inconcistency1,ANPAHP.vector1 = json.dumps([]), np.nan, json.dumps([])
        ANPAHP.status7 = True
        ANPAHP.save()
        return redirect('myANPAHPStep9',pk=pk)

######################## integration analysis
@login_required
def MyANPAHPStep9(request,pk):

    ANPAHP = EVALUATION.objects.get(pk=pk)
    SelectedKPIs = eval(ANPAHP.SelectedKPIs)
    SelectedCriterias = eval(ANPAHP.SelectedCriterias)
    KPIs_list = [value for sublist in SelectedKPIs.values() for value in sublist]
    KPIs_names = list(KPI.objects.all().values_list('name',flat=True).order_by('id'))
    Criteria_names = list(Criteria.objects.all().order_by('id').values_list('name',flat=True))
    KPIS_selected_names = [KPIs_names[index - 1] for index in KPIs_list if 0 < index <= len(KPIs_names)]
    Criterias_selected_names = [Criteria_names[index - 1] for index in SelectedCriterias if 0 < index <= len(Criteria_names)]
    rows = []
    rows.extend(KPIS_selected_names)
    rows.extend(Criterias_selected_names)

    #set the matrix of interactions
    matrix_data = np.eye(len(rows))
    count =0
    for key, value in SelectedKPIs.items():
        if value:
            size =len(value)
            matrix_data[count:count + size, count:count + size] = 1.0
            count +=size
    size = len(SelectedCriterias)
    #matrix_data[count:count + size, count:count + size] = 1.0
    form = Step9Form(request.POST or None, instance=ANPAHP)
    if request.method == "POST":
        matrix_data_post = []
        count =0
        for i in rows:
            rows_values = []
            for j in rows:
                if f'matrix[{i}][{j}]' in request.POST:
                    rows_values.append(1)
                    count += 1
                else:
                    rows_values.append(0)
            matrix_data_post.append(rows_values)
        ANPAHP.matrix_data_pre = str(matrix_data.tolist())
        ANPAHP.matrix_data = json.dumps(matrix_data_post)
        ANPAHP.KPIS_selected_names = KPIS_selected_names
        ANPAHP.Criterias_selected_names = Criterias_selected_names
        if count != 0 :
            ANPAHP.save()
            return redirect('myANPAHPStep10',pk=pk)
        else:
            limitingmatrix, Hierarchy, supermatrix = EXECUTE_ANALYSIS(ANPAHP)
            ANPAHP.status8 = True
            ANPAHP.results = limitingmatrix
            ANPAHP.hierarcy = Hierarchy
            ANPAHP.supermatrix = supermatrix.tolist()
            ANPAHP.save()
            return redirect('myANPAHPResults',pk=pk)
    else:
        
        rows2 = rows[:-len(SelectedCriterias)]
        return render(request,'ANPAHP/ANPAHPStep9.html',{'ANPAHP':ANPAHP,'form':form,'matrix_data': matrix_data.tolist(), 'rows': rows,'rows2': rows2})


@login_required
def MyANPAHPStep10(request,pk):
    ANPAHP = EVALUATION.objects.get(pk=pk)
    matrix_data = np.array(eval(ANPAHP.matrix_data))
    matrix_data_pre = np.array(eval(ANPAHP.matrix_data_pre))
    # Find the columns with one check and multiple checs. The columns with one check is direct dependance so no pairwise comparison and should be set as 1 in the supermatrix.
    column_counts  = np.sum(matrix_data, axis=0)
    columns_with_one_one = np.where(column_counts == 1)[0]
    columns_with_more_than_one_one = np.where(column_counts > 1)[0]
    # extract names and list to process Finaly, create a dictionary that links names of KPIs families instead of their numbers.
    KPIS_selected_names = eval(ANPAHP.KPIS_selected_names)
    Criterias_selected_names = eval(ANPAHP.Criterias_selected_names)
    names = KPIS_selected_names + Criterias_selected_names
    SelectedKPIs = eval(ANPAHP.SelectedKPIs)
    SelectedCriterias = eval(ANPAHP.SelectedCriterias)
    KPI_names = list(KPI.objects.all().values_list('name',flat=True))
    CRITERIA_names = list(Criteria.objects.all().order_by('id').values_list('name',flat=True))
    new_dict = {}
    for key, value in SelectedKPIs.items():
        new_values = [KPI_names[idx-1] for idx in value]
        new_dict[key] = new_values
    ######### generate the names to put in display for pairwise comparison.
    ids = {}
    ids1 = []
    ids2 = []
    comments = {}
    names_to_use = []
    for i in columns_with_more_than_one_one:
        name = names[i]
        comments[name] = f'For {name} please specify the relative importance of each pair of dependances:'
        name_columns = [name for num, name in enumerate(names) if matrix_data[num,i] == 1]
        for value in new_dict.values():
            count1 = sum([1 for item in name_columns if item in value])
            if count1 >=2:
                names_to_add1 = [name for name in name_columns if name in value]
                ids1.extend([names_to_add1])
        #count2 = sum([1 for item in name_columns if item in Criterias_selected_names])
        #if count2 >=2:
        #    names_to_add2 = [name for name in name_columns if name in Criterias_selected_names]
        #    ids2.extend(names_to_add2)
        #ids1.extend([ids2])
        names_to_use.extend([name])
        ####################### check for if ids need to create a list of pairs ###########
        ids[name] = ids1
        ids1=[]
    idsfinal = generate_pairs_as_lists(ids)

    if request.method == "POST":
        supermatrix = eval(ANPAHP.supermatrix)
        try:
            supermatrix = np.array(supermatrix)
        except:
            pass
        pairwise_comparison_values, interactions_matrix, interactions_vectors, interactions_inconcistency, names = {}, {}, {}, {}, {}
        for numero, ZZ in enumerate(names_to_use):
            for j in idsfinal[ZZ]:
                field_name = f"results{ZZ}{j}"
                pairwise_comparison_values[field_name] = request.POST.get(field_name)

            pairwise_comparison_values = {key: value for key, value in pairwise_comparison_values.items() if value is not None}
            selection = [float(value) for key, value in pairwise_comparison_values.items()]
            separated_results_matrix, separated_results_vectors, separated_results_inconcistency = [], [], []
            count = 0

            for num, content in enumerate(ids[ZZ]): # for those that have more than one count
                list_to_input = numerate_names([content])
                list_to_input2 = list(itertools.combinations(list_to_input[0],2))
                matrix, vector, inconcistency = construct_matrix(selection[count:count+len(list(itertools.combinations(content,2)))],list_to_input2,dim=len(content))
                separated_results_matrix.append(matrix)
                separated_results_vectors.append(vector.tolist())
                separated_results_inconcistency.append(inconcistency)
                count+=len(list(itertools.combinations(content,2)))
            interactions_matrix[ZZ] = separated_results_matrix
            interactions_vectors[ZZ] = separated_results_vectors
            interactions_inconcistency[ZZ] = separated_results_inconcistency

            ############## To check code ###################

            all_kpis_order = [kpi for sublist in new_dict.values() for kpi in sublist]

            weights_dict = {}
            for sublist, weights in zip(ids[ZZ], separated_results_vectors):
                for kpi, weight in zip(sublist, weights):
                    weights_dict[kpi] = weight
            for kpi in all_kpis_order:
                if kpi not in weights_dict:
                    weights_dict[kpi] = 1.0
            extended_weights_list = []
            current_sublist = []
            current_category = None

            # Iterate over dict1 to maintain category structure
            for category, kpis in new_dict.items():
                if current_category is not None and current_category != category:
                    extended_weights_list.append(current_sublist)
                    current_sublist = []
                current_category = category
                for kpi in kpis:
                    current_sublist.append(weights_dict[kpi])

            # Add the last sublist
            if current_sublist:
                extended_weights_list.append(current_sublist)

            normalized = ponder_and_normalize(extended_weights_list,supermatrix[1:5,0].tolist())
            normalized = [item for sublist in normalized for item in sublist]
            data = matrix_data[:,columns_with_more_than_one_one[numero]]
            for num, value in enumerate(data):
                if value == 1:
                    supermatrix[5+num,5+columns_with_more_than_one_one[numero]] = normalized[num]
            #### Asign values in the supermatrix

        for i in columns_with_one_one:
            KPIs_list = [value for sublist in SelectedKPIs.values() for value in sublist]
            vertical_position = matrix_data[:,i].tolist().index(1)
            if i in range(len(KPIs_list)): # if linked to a KPI
                count = 0
                for num,(key,value) in enumerate(SelectedKPIs.items()):
                    if KPIs_list[vertical_position] in value:
                        ponder_value_1 = supermatrix[num+1,0]
                        rango = list(range(count,count+len(value)))
                    if KPIs_list[vertical_position] in value:
                        ponder_value_2 = supermatrix[num+1,0]
                    count += len(value)

                ponder_values = [ponder_value_1, ponder_value_2]
                values_to_ponder = [[1.0], supermatrix[vertical_position+5,rango].tolist()]
                normalized = ponder_and_normalize(values_to_ponder, ponder_values)
                supermatrix[vertical_position+5,i+5] = normalized[0][0]
                if len(rango)>1:
                    supermatrix[vertical_position+5,rango] = normalized[1]
                else:
                    supermatrix[vertical_position+5,rango] = normalized[1][0]
            else:
                supermatrix[vertical_position+5,i+5] = 1.0
        
        ANPAHP.supermatrix = supermatrix.tolist()
        #matrix, vector, inconcistency = construct_matrix(selection,pairs['Financial'])
        limitingmatrix, Hierarchy, supermatrix = EXECUTE_ANALYSIS(ANPAHP)
        ANPAHP.status8 = True
        ANPAHP.results = limitingmatrix
        ANPAHP.hierarcy = Hierarchy
        ANPAHP.status8 = True
        ANPAHP.supermatrix = supermatrix.tolist()
        ANPAHP.save()
        return redirect('myANPAHPResults',pk=pk)
    else:
        idsfinal = {key: [item for item in value if item] for key, value in idsfinal.items()}
        return render(request,'ANPAHP/ANPAHPStep10.html',{'ANPAHP':ANPAHP,'ids':idsfinal,'names_to_use':names_to_use,'comments':comments})


@login_required
def myANPAHPResult(request,pk):
    ANPAHP = EVALUATION.objects.get(pk=pk)
    KPIS_selected_names = eval(ANPAHP.KPIS_selected_names)
    Criterias_selected_names = eval(ANPAHP.Criterias_selected_names)
    names = ['Strategy','Customer','Financial','Education and Growth','Internal Processes'] + KPIS_selected_names + Criterias_selected_names
    limiting_matrix = eval(ANPAHP.results)
    limiting_matrix_plot_KPIs = np.array(limiting_matrix)
    limiting_matrix_plot_KPIs = limiting_matrix_plot_KPIs[5:5+len(KPIS_selected_names),0]
    suma = np.sum(limiting_matrix_plot_KPIs)
    limiting_matrix_plot_KPIs = limiting_matrix_plot_KPIs/suma
    plot_markers = np.linspace(0.0,max(limiting_matrix_plot_KPIs),5).tolist()
    chart = make_radar_chart(limiting_matrix_plot_KPIs,KPIS_selected_names,plot_markers=plot_markers)
    ######## If a column has only 0's in the first one or the last ones, eliminate them for the table 


    limiting_matrix = pd.DataFrame(limiting_matrix,columns=names)
    limiting_matrix.index = names
    html_table = limiting_matrix.to_html(classes='table table-striped')

    form = Results1Form(request.POST or None, instance=ANPAHP)
    context = {'form':form,'ANPAHP':ANPAHP,'html_table':html_table,'chart':chart}
    if form.is_valid():
        form.save()
        return render(request,'ANPAHP/myANPAHPResults.html',context)
    return render(request,'ANPAHP/myANPAHPResults.html',context)



@login_required
def myANPAHPPdf(request,pk):
    ANPAHP = EVALUATION.objects.get(pk=pk)
    KPIS_selected_names = eval(ANPAHP.KPIS_selected_names)
    Criterias_selected_names = eval(ANPAHP.Criterias_selected_names)
    names = ['Strategy','Customer','Financial','Education and Growth','Internal Processes'] + KPIS_selected_names + Criterias_selected_names
    limiting_matrix = eval(ANPAHP.results)
    limiting_matrix_plot_KPIs = np.array(limiting_matrix)
    limiting_matrix_plot_KPIs = limiting_matrix_plot_KPIs[5:5+len(KPIS_selected_names),0]
    suma = np.sum(limiting_matrix_plot_KPIs)
    limiting_matrix_plot_KPIs = limiting_matrix_plot_KPIs/suma
    plot_markers = np.linspace(0.0,max(limiting_matrix_plot_KPIs),5).tolist()
    chart = make_radar_chart(limiting_matrix_plot_KPIs,KPIS_selected_names,plot_markers=plot_markers)
    limiting_matrix = pd.DataFrame(limiting_matrix,columns=names)
    limiting_matrix.index = names
    limiting_matrix = limiting_matrix.style.format("{:.3f}")
    html_table = limiting_matrix.to_html(classes='table table-striped',border=0, justify='center', index=True)

    context = {'html_table':html_table,'chart':chart}
    template_path = 'ANPAHP/myANPAHPPdf.html'
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
