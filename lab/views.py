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
def task_index(request):
    task_list=json.loads(Task.objects().all().to_json(ensure_ascii=False))
    product_list = json.loads(Product.objects().all().to_json(ensure_ascii=False))
    product_dict={}
    for product in product_list:
        product_dict[product['_id']]=product
    for task in task_list:
        task['starttime']=datetime.datetime.fromtimestamp(task['starttime']).strftime('"%Y-%m-%d %H:%M:%S')
        task['bestuptime'] = datetime.datetime.fromtimestamp(task['bestuptime']).strftime('"%Y-%m-%d %H:%M:%S')
        task['worstuptime'] = datetime.datetime.fromtimestamp(task['worstuptime']).strftime('"%Y-%m-%d %H:%M:%S')
        task['product']=product_dict[task['product']]
    return HttpResponse(json.dumps(task_list,ensure_ascii=False))
    # request.session['ref']=reverse('lab:task_index',args=[key])
    # return render(request,'lab/task/task.html',locals())

# 进行任务
def process_task(request):
    message={}
    if request.method=='POST':
        data=json.loads(request.body.decode('utf-8'))
        task = Task.objects(pk=data['taskid']).first()
        try:
            task.modify(status='进行',expstatus='进行')
            message['success']='操作成功'
        except Exception as e:
            message['error']=e
    return HttpResponse(json.dumps(message, ensure_ascii=False))
    # if request.session.get('ref', None):
    #     return redirect(request.session.pop('ref'))
    # else:
    #     return redirect(reverse('lab:task_index', args=['index']))

#完成任务
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

# 暂停任务
def pause_task(request):
    message={}
    if request.method=='POST':
        data=json.loads(request.body.decode('utf-8'))
        task = Task.objects(pk=data['taskid']).first()
        info = task.info
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
    return HttpResponse(json.dumps(message, ensure_ascii=False))


# 任务上机
def up_task(request,task):
    message = {}
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        task = Task.objects(pk=data['taskid']).first()
        try:
            task.modify(expstatus='上机')
        except Exception as e:
            message['error']=e
    return HttpResponse(json.dumps(message, ensure_ascii=False))
    # if request.session.get('ref', None):
    #     return redirect(request.session.pop('ref'))
    # else:
    #     return redirect(reverse('lab:task_index', args=['index']))

# 重置实验
def reset_task(request,task):
    message={}
    if request.method=='POST':
        data=json.loads(request.body.decode('utf-8'))
        task=Task.objects(pk=data['taskid']).first()
        info=task.info
        info += data['info']
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
    return HttpResponse(json.dumps(message, ensure_ascii=False))
    # if request.session.get('ref', None):
    #     return redirect(request.session.pop('ref'))
    # else:
    #     return redirect(reverse('lab:task_index', args=['index']))

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

