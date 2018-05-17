from django.shortcuts import render
from django.shortcuts import render,reverse,redirect,HttpResponse
from django.http import HttpResponseRedirect
from .models import *
from .forms import *
import pandas as pd
import datetime,random,string,json
# Create your views here.
# 首页
def index(request):
    if request.session.get('message',None):
        message=request.session.pop('message')
    return render(request,'lab/index.html',locals())

# 任务管理
def task_index(request,key):
    columns='任务编号 任务状态 实验状态 产品编号 癌种 患者编号 开始时间 最优上机时间 最坏下机时间 样本类型（control） 测序数据量（control）	样本类型（case）	测序数据量（case）	技术平台	生产芯片	测序策略	分子标签建库 操作'.split()
    if request.session.get('message',None):
        message=request.session.pop('message')
        title='任务总览'
        task_list=Task.objects().all()
    products={}
    for product in Product.objects().all():
        value=product.to_mongo().to_dict()
        value.pop('bestuptime')
        value.pop('worstuptime')
        value.pop('book')
        value.pop('period')
        products[value.pop('_id')]=value
    tasks=[]
    for task in task_list:
        task=json.loads(task.to_json(ensure_ascii=False))
        task.update(products[task['product']])
        task['_id']=task['_id']['$oid']
        task['bestuptime']=task['bestuptime']['$date']
        task['deadline']=task['deadline']['$date']
        tasks.append(task)

    return HttpResponse(json.dumps(tasks,ensure_ascii=False))
    # request.session['ref']=reverse('lab:task_index',args=[key])
    # return render(request,'lab/task/task.html',locals())

def process_task(request,task):
    message={}
    try:
        task = Task.objects(pk=task).first()
        task.modify(status='进行',expstatus='进行')
        message['success']='操作成功'
    except Exception as e:
        message['error']=e
    if request.session.get('ref', None):
        return redirect(request.session.pop('ref'))
    else:
        return redirect(reverse('lab:task_index', args=['index']))

def submitted_task(request,task):
    url=reverse('lab:submitted_task',args=[task])
    if request.session.get('message',None):
        message=request.session.pop('message')
    else:
        message={}
        request.session['message']=message
    task=Task.objects(pk=task).first()
    if request.method=='POST':
        data=SubmitTask(request.POST)
        if data.is_valid():
            try:
                task.modify(expstatus='完成',**data.cleaned_data)
                message['success']='提交成功'
                if request.session.get('ref',None):
                    return redirect(request.session.pop('ref'))
                else:
                    return redirect(reverse('lab:task_index',args=['index']))
            except Exception as e:
                message['error']=e
    form=SubmitTask()
    return render(request,'lab/form.html',locals())

def pause_task(request):
    if request.session.get('message',None):
        message=request.session.pop('message')
    else:
        message={}
        request.session['message']=message

    if request.method=='POST':
        data=PauseTask(request.POST)
        if data.is_valid():
            try:
                task = Task.objects(pk=data.cleaned_data['task']).first()
                task.modify(status='暂停',expstatus='暂停',**data.cleaned_data)
                message['success']='暂停成功'
                if request.session.get('ref',None):
                    return redirect(request.session.pop('ref'))
                else:
                    return redirect(reverse('lab:task_index',args=['index']))
            except Exception as e:
                message['error']='操作失败'
    url=reverse('lab:pause_task',args=[task])
    form=PauseTask()
    return render(request,'lab/form.html',locals())

def up_task(request,task):
    message={}
    request.session['message'] = message
    task=Task.objects(pk=task)
    try:
        task.modify(expstatus='上机')
    except Exception as e:
        message['error']=e
    if request.session.get('ref', None):
        return redirect(request.session.pop('ref'))
    else:
        return redirect(reverse('lab:task_index', args=['index']))

def reset_task(request,task):
    message={}
    request.session['message']=message
    task = Task.objects(pk=task).first()
    starttime=datetime.datetime.now()
    deadline=datetime.datetime.now()+datetime.timedelta(days=task.product.period)
    bestuptime=datetime.datetime.now()+datetime.timedelta(days=task.product.bestuptime)
    worstuptime=datetime.datetime.now()+datetime.timedelta(days=task.product.worstuptime)
    try:
        task.modify(
            starttime=starttime,deadline=deadline,
            bestuptime=bestuptime,worstuptime=worstuptime,
            status='开始',expstatus='开始')
        message['success']='重置成功'
    except Exception as e:
        message['error']= e
    if request.session.get('ref', None):
        return redirect(request.session.pop('ref'))
    else:
        return redirect(reverse('lab:task_index', args=['index']))

# 患者列表
def patient_index(request):
    if request.session.get('message',None):
        message=request.session.pop('message')
    request.session['ref']=reverse('lab:patient_index')
    columns='患者编号 患者姓名 患者年龄 患者性别 癌种 样本状态 信息状态'.split()
    request.session['ref'] = reverse('lab:patient_index')
    # patient_list=Patient.objects().all()
    # return render(request,'lab/patient/patient.html',locals())

    data=Patient.objects().all().to_json(ensure_ascii=False)
    return HttpResponse(data)

# 患者详情页
def patient_detail(request,patient):
    if request.session.get('message',None):
        message=request.session.pop('message')
    else:
        message={}
        request.session['message'] = message
    request.session['ref']=reverse('lab:patient_detail',args=[patient])
    patient=Patient.objects(patientid=patient).first()
    patientcolumns='患者编号 患者姓名 年龄 性别 癌肿 操作'.split()
    sample_list=Sample.objects(patient=patient).all()
    samplecolumns='样本编号 样本类型 样本接受时间 样本状态'.split()
    task_list=Task.objects(patient=patient).all()
    return render(request,'lab/patient/patient_detail.html',locals())

def patient_addsample(request,patient):
    if request.session.get('message',None):
        message=request.session.pop('message')
    else:
        message={}
        request.session['message']=message
    if request.method=='POST':
        data=AddSample(request.POST)
        if data.is_valid():
            try:
                sample=Sample(receivestatus=datetime.datetime.now(),**data.cleaned_data)
                sample.save()
                message['success']='添加样本成功'
                if request.session.get('ref',None):
                    return redirect(request.session.pop('ref'))
                else:
                    return redirect(reverse('lab:task_index',args=['index']))
            except Exception as e:
                message['error']=e
        else:
            message['error']='请检查表格内容'
    url=reverse('lab:patient_addsample',args=[patient])
    form=AddSample(initial={'patient':patient})
    return render(request,'lab/form.html',locals())

# 样本列表
def sample_index(request):
    if request.session.get('message',None):
        message=request.session.pop('message')
    request.session['ref']=reverse('lab:sample_index')
    columns='样本编号 患者 类型 组织类型 接收时间 样本状态 接受者 接受状态'.split()
    sample_list=Sample.objects().all().to_json(ensure_ascii=False)
    # return render(request,'lab/sample/sample.html',locals())
    return HttpResponse(sample_list)

# 检索样本，患者
def search(request):
    if request.session.get('message',None):
        message=request.session.pop('message')
    else:
        message = {}
    url=reverse('lab:search')
    if request.method=='POST':
        return HttpResponse('后面再补充')

