from django.shortcuts import render,reverse,redirect
from .models import *
from .forms import *
# Create your views here.
# analyst
def index(request):
    pass

def task_index(request,key):
    if request.session.get('message',None):
        message=request.session.pop('message')
    title='任务列表'
    task_list=[]
    if key=='index':
        task_list+=Task.objects().all()
    elif key=='analyst':
        task_list+=Task.objects(anastatus='开始').all()
    elif key=='jiedu':
        task_list += Task.objects(jiedu_status='开始').all()
    return render(request,'Analyst/task/taskindex.html',locals())

