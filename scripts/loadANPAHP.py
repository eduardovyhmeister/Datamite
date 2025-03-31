from ANPAHP.models import KPI, Criteria, Objective
import csv, os
import pandas as pd

def run():
    path=os.path.join(os.getcwd(),"static/mine","KPIs.csv")
    path2 = os.path.join(os.getcwd(),"static/mine","Objectives.csv")
    path3 = os.path.join(os.getcwd(),"static/mine","Criterias.csv")
    info=pd.read_csv(path,sep=",")
    info2=pd.read_csv(path2,sep=",")
    info3=pd.read_csv(path3,sep=",")
    for i in range(len(info)):
        name = info.iloc[i]['name']
        existing_kpi = KPI.objects.filter(name=name).first()
        if existing_kpi:
            continue
        kpis,check= KPI.objects.get_or_create(name=info.iloc[i]['name'],explanation=info.iloc[i]['explanation'],BSCfamily=info.iloc[i]['BSCfamily'])
        if not check:
            print(info.iloc[i]['name'] + ' already exist' )
        kpis.save()

    for i in range(len(info2)):
        name = info2.iloc[i]['name']
        existing_objective = Objective.objects.filter(name=name).first()
        if existing_objective:
            continue
        objectives,check= Objective.objects.get_or_create(name=info2.iloc[i]['name'],explanation=info2.iloc[i]['explanation'])
        if not check:
            print(info2.iloc[i]['name'] + ' already exist' )
        objectives.save()

    for i in range(len(info3)):
        name = info3.iloc[i]['name']
        existing_criteria = Criteria.objects.filter(name=name).first()
        if existing_criteria:
            continue
        criterias,check= Criteria.objects.get_or_create(name=info3.iloc[i]['name'],explanation=info3.iloc[i]['explanation'])
        if not check:
            print(info3.iloc[i]['name'] + ' already exist' )
        criterias.save()

