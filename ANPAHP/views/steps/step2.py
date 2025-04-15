from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from ...models import Evaluation
from ..helpers import construct_matrix

@login_required
def step2_view(request, pk):
    ANPAHP = Evaluation.objects.get(pk=pk)
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
        matrix, vector, inconcistency = construct_matrix(selection, elements, dim=4)
        if abs(inconcistency) < 0.4:
            print(inconcistency)
            ANPAHP.step_status1 = True
            ANPAHP.BSC_Weights = vector.tolist()
            ANPAHP.save()
            return redirect('myANPAHPStep2',pk=pk)
        else:
            ANPAHP.step_status1 = False
            message = f'There is huge inconcistency  ({inconcistency}) in the information provided. Please re-evaluate.'
            ERROR1 = True
            return render(request,'ANPAHP/ANPAHPStep2.html',{'ANPAHP':ANPAHP,'message':message,'message2':ANPAHP.message,'ERROR1':ERROR1,'ERROR2':ERROR2})
    else:
        return render(request,'ANPAHP/ANPAHPStep2.html',{'ANPAHP':ANPAHP,'message':message,'message2':ANPAHP.message,'ERROR1':ERROR1,'ERROR2':ERROR2})
