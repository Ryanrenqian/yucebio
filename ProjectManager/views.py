from django.shortcuts import render,reverse,redirect
from django.http import HttpResponseRedirect,HttpResponse
from .models import *
from .forms import *
import pandas as pd
import datetime
import random,string,os,json
from django.views.decorators.csrf import csrf_exempt
import logging
# Create your views here.
# creat Index for all your need
# 工具函数
logging.basicConfig(level=logging.DEBUG,filename='log.txt')

def GenerateID(database):
    ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 10))
    while True:
        if len(database.objects(pk=ran_str))==0:
            obj=database(pk=ran_str)
            obj.save()
            break
        else:
            ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 10))
    return ran_str

# 保存上传数据
def handle_uploaded_file(f):
    file='/Users/ryan/PycharmProjects/yucebio/tmp/'+f.name
    with open(file, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return file

# 首页
def index(request):
    return render(request,'ProjectManager/index.html')

# 项目列表
def project_index(request):
    # if request.session.get('message',None):
    #     message=request.session.pop('message')
    # else:
    #     message={}
    # columns='项目编号 项目状态 项目负责人 开始日期 剩余时间 截止日期 完成时间 延迟状态 项目操作'.split()
    message={}
    project_list = Project.objects().all()
    for project in project_list:
        if project.status not in ['提交','暂停'] :
            try:
                project.duration=(project.deadline-datetime.datetime.now()).days
                if project.duration<0:
                    project.delay='是'
                project.save()
            except Exception as e:
                message['error']=e
    project_list=json.loads(project_list.to_json(ensure_ascii=False))
    new_project_list=[]
    for project in project_list:
        project['projectid']=project['_id']
        if project.get('tag',None):
            new_project_list.append(project)
        patient_list = []
        product_list = []
        task_list = []
        for patient in project.get('patients',[]):
            patient=json.loads(Patient.objects(pk=patient).first().to_json(ensure_ascii=False))
            patient_list.append(patient)
        for product in project.get('products',[]):
            product=json.loads(Product.objects(pk=product).first().to_json(ensure_ascii=False))

            product_list.append(product)
        for task in project.get('tasks',[]):
            task=json.loads(Task.objects(pk=task).first().to_json(ensure_ascii=False))
            task['patientname'] = Patient.objects(pk=task.get('patient')).first().patientname
            task_list.append(task)
        project['patient_list']=patient_list
        project['product_list']=product_list
        project['task_list']=task_list
    # return render(request,'ProjectManager/project/project.html',locals())
    return HttpResponse(json.dumps({'data':new_project_list},ensure_ascii=False))
# 添加项目
# 直接添加项目
def add_project(request):
    message={}
    # url=reverse('projectmanager:add_project')
    if request.method=='POST':
        # form=AddProject(request.POST)
        data=json.loads(request.body.decode('utf-8'))
        # if form.is_valid():
        logging.debug(data)
        warning = []
        patients=set(data['patients'].split())
        for patient in data['patients'].split():
            if len(Patient.objects(pk=patient)) == 0:
                warning.append(patient)
                patients.remove(patient)
        data['patients']=list(patients)
        tumortypes=data.get('tumortype').split()
        data['start_time']=datetime.datetime.strptime(data['start_time'],"%Y-%m-%d %H:%M:%S")
        data['deadline']=datetime.datetime.strptime(data['deadline'],"%Y-%m-%d %H:%M:%S")
        # if len(Project.objects(pk=data['projectid']))==0:
        project=Project(**data)
        project.save()
        tasks=[]
        for product in project.products:
            for patient in project.patients:
                for tumortype in tumortypes:
                    patient.modify(taskstatus='有')
                    taskid = GenerateID(Task)
                    task=Task.objects(pk=taskid).first()
                    task.modify(tumortype=tumortype, product=product, patient=patient, status='暂停', expstatus='暂停',
                                anastatus='暂停', jiedu_status='暂停', reportstatus='暂停')
                    tasks.append(task)
        project.modify(tasks=tasks)
        message['success'] = '保存成功'
        if len(warning)!=0:
            message['warning'] = '以下患者出现问题，可能不存在：%s'%(','.join(set(warning)))
        # else:
        #     message['warning']='该项目已存在，请刷新获取新的项目编号'
        # else:
        #     message['warning']='请检查表格'
        return HttpResponse(json.dumps(message,ensure_ascii=False))
    else:
        data={}
        projectid=GenerateID(Project)
        product_list = json.loads(Product.objects().all().to_json(ensure_ascii=False))
        for i in product_list:
            i['productid'] = i['_id']
        user_list=json.loads(User.objects().all().to_json(ensure_ascii=False))
        for i in user_list:
            i['account'] = i['_id']
        data['projectid']=projectid
        data['product_list']=product_list
        data['user_list']=user_list
        return HttpResponse(json.dumps({'data':[data]},ensure_ascii=False))
    # title='添加项目'
    # ran_str,form = projectGenerate()
    # return render(request,'ProjectManager/form.html',locals())


# 从Excel表格导入  需要修改
def add_project_excel(request):
    reminder='批量导入项目'
    if request.session.get('message',None):
        message=request.session.pop('message')
    else:
        message={}
    if request.method=='POST':
        message['warning'] = '以下提示患者信息未保存'
        form=FileUpload(request.POST,request.FILES)
        if form.is_valid():
            if request.FILES.get('file',None):
                try:
                    data=pd.read_excel(handle_uploaded_file(request.FILES['file']),header=0,sheetname=0)
                    for i in data.index:
                        row=data.loc[i]
                        if row.get('projectid',None):
                            projectid=row['projectid']
                        else:
                            projectid,_form=projectGenerate()
                        products=[row['product']]
                except Exception as e:
                    message['error']=e
            else:
                message='请重新上传文件'
    form=FileUpload()
    return render(request, 'ProjectManager/form.html', locals())

# 终止项目
def stop_project(request,project):
    message={}
    project=Project.objects(projectid=project).first()
    for task in project.tasks:
        task.modify(status='终止',expstatus='终止',anastatus='终止',jiedu_status='终止')
    project.modify(status='终止')
    message['success']='该项目已终止'
    return HttpResponse(json.dumps(message,ensure_ascii=False))

# 项目详情
# def project_detail(request,project):
#     # if request.session.get('message',None):
#     #     message=request.session.pop('message')
#     # request.session['ref']=reverse('projectmanager:project_detail',args=[project])
#     # projectcolumns='项目编号 项目状态 项目负责人 开始日期 剩余时间 截止日期 完成时间 延迟状态 项目操作'.split()
#     project=json.loads(Project.objects(projectid=project).first().to_json(ensure_ascii=False))
#     patient_list=[]
#     product_list=[]
#     task_list=[]
#     for patient in project['patients']:
#         patient_list.append(json.loads(Patient.objects(pd=patient).first().to_json(ensure_ascii=False)))
#     for product in project['products']:
#         product_list.append(json.loads(Product.objects(pk=product).first().to_json(ensure_ascii=False)))
#     for task in project['tasks']:
#         task_list.append(json.loads(Task.objects(pk=task).first().to_json(ensure_ascii=False)))
#     data={}
#     data['product_list']=product_list
#     data['task_list']=task_list
#     data['patient_list']=patient_list
#     return HttpResponse(json.dumps({'data':data},ensure_ascii=False))
#     # productcolumns='产品编号 产品名称 产品说明书 产品周期 样本类型（control）	测序数据量（control）	样本类型（case）	测序数据量（case） 技术平台	生产芯片	测序策略	分子标签建库'.split()
#     # patientcolumns='患者编号 患者姓名 患者年龄 患者性别 癌种'.split()
#     # taskcolumns='任务编号 任务产品 任务病人 状态 分析状态 实验状态 解读状态 报告状态 操作'.split()
#     # request.session['ref'] = reverse('projectmanager:project_detail', args=[project])
#     # return render(request, 'ProjectManager/project/project_detail.html', locals())

# 可能不需要

def project_addpatient(request):
    message = {}
    warning=[]
    if request.method=="POST":
        data=json.loads(request.body.decode('utf-8'))
        project=Project.objects(pk=data['projectid']).first()
        project.patients.append(project)
        tumortypes=project.tumortype.split()
        patients = set(data['patients'].split())
        for patient in data['patients'].split():
            if len(Patient.objects(pk=patient)) == 0:
                warning.append(patient)
                patients.remove(patient)
        data['patients'] = list(patients)
        for product in project.products:
            for patient in project.patients:
                if len(tumortypes)!=0:
                    for tumortype in tumortypes:
                        patient.modify(taskstatus='有')
                        taskid = GenerateID(Task)
                        task=Task.objects(pk=taskid).first()
                        task.modify(tumortype=tumortype, product=product, patient=patient, status='暂停', expstatus='暂停',
                                    anastatus='暂停', jiedu_status='暂停', reportstatus='暂停')
                        project.tasks.append(task)
                else:
                    patient.modify(taskstatus='有')
                    taskid = GenerateID(Task)
                    task = Task.objects(pk=taskid).first()
                    task.modify(product=product, patient=patient, status='暂停', expstatus='暂停',
                                anastatus='暂停', jiedu_status='暂停', reportstatus='暂停')
                    project.tasks.append(task)
        project.save()
        message['success']='保存成功'
    if len(warning)!=0:
        message['warning'] = '以下患者出现问题，可能不存在：%s'%(','.join(set(warning)))
    # else:
    #     message['warning']='该项目已存在，请刷新获取新的项目编号'
    # else:
    #     message['warning']='请检查表格'
    return HttpResponse(json.dumps(message,ensure_ascii=False))

# 项目内部添加
# def project_add_task(request,project):
#     if request.session.get('message',None):
#         message=request.session.pop('message')
#     else:
#         message={}
#     project=Project.objects(pk=project).first()
#     request.session['message'] = message
#     if request.method=='POST':
#         data=ProjectAddTask(request.POST)
#         if data.is_valid():
#             if data.cleaned_data['patient'] in project.patients:
#                 try:
#                     task=Task(**data.cleaned_data)
#                     task.save()
#                     message['success']='保存成功'
#                     project.tasks.append(task)
#                     project.save()
#                     # if request.session.get('ref',None):
#                     #     return redirect(request.session.pop('ref'))
#                     # else:
#                     #     return  redirect(reverse('projectmanager:project_detail',args=[project]))
#                 except:
#                     message['warning']='保存失败'
#             else:
#                 message['error']='该项目无此成员'
#         else:
#             message['error']='请检查表格'
#     url=reverse('projectmanager:project_add_task',args=[project])
#     form=ProjectAddTask()
#     return render(request,'ProjectManager/form.html',locals())

# 项目操作
def project_pay(request,project):
    message={}
    project = Project.objects(pk=project).first()
    try:
        project.modify(status='已付费/免费')
        for task in project.tasks:
            starttime=datetime.datetime.now()
            bestuptime =datetime.datetime.now()+datetime.timedelta(days=task.product.bestuptime)
            worstuptime =datetime.datetime.now()+datetime.timedelta(days=task.product.worstuptime)
            task.modify(status='进行',
                        expstatus='开始',
                        anastatus='wait',
                        jiedu_status='wait',
                        starttime=starttime,
                        bestuptime=bestuptime,
                        worstuptime=worstuptime)
        message['success'] = '缴费并成功下单'
    except Exception as e:
        message['error']=str(e)
    return HttpResponse(json.dumps(message,ensure_ascii=False))

def project_pause(request,project):
    message = {}
    project = Project.objects(pk=project).first()
    try:
        for task in project.tasks:
            task.modify(status='暂停',jiedu_status='暂停',expstatus='暂停',anastatus='暂停')
        project.status='暂停'
    except Exception as e:
        message['error']=e
    # return redirect(reverse('projectmanager:project_detail',args=[project]))
    return HttpResponse(json.dumps(message))

def project_declare_lab(request,project):
    message={}
    project = Project.objects(pk=project).first()
    try:
        for task in project.tasks:
            task.modify(expstatus='无')
        message['success']='取消实验操作成功'
    except Exception as e:
        message['error']=e
    return HttpResponse(json.dumps(message))
    # request.session['message']=message
    # return redirect(reverse('projectmanager:project_detail',args=[project]))

def project_declare_jiedu(request,project):
    message = {}
    try:
        project = Project.objects(pk=project).first()
        for task in project.tasks:
            task.modify(jiedu_status='无',reportstatus='无')
        message['success'] = '批量操作成功'
    except Exception as e:
        message['error'] = e
    return HttpResponse(json.dumps(message))
# 项目下单
# def project_add_lab(request,project):
#     if request.session.get('message',None):
#         message=request.session.pop('message')
#     else:
#         message={}
#     title='实验室下单'
#     project=Project.objects(projectid=project).first()
#     project.modify(status='已付费/免费')
#     if request.method=='POST':
#         form=Order(request.POST)
#         if form.is_valid():
#             for task in project.tasks:
#                 if task.product==form.cleaned_data['product']:
#                     try:
#                         task.status='已下单'
#                         labtask=Labtask(task=task,**form.cleaned_data)
#                         labtask.save()
#                         message['success']='保存成功'
#                     except Exception as e:
#                         message['error']=e
#             request.session['message']=message
#             return redirect(reverse('projectmanager:project_detail',args=[project]))
#         else:
#             message['warning']='请检查表格'
#     form=Order()
#     return render(request,'ProjectManager/form.html',locals())

# 需要重新考虑
# def project_add_ana(request,project):
#     if request.session.get('message',None):
#         message=request.session.pop('message')
#     else:
#         message={}
#     if request.method=='POST':
#         pass
#         return redirect(reverse('projectmanager:project_detail',args=[project]))
#     return render(request,'ProjectManager/form.html',locals())
#
# def project_add_rep(request,project):
#     if request.session.get('message',None):
#         message=request.session.pop('message')
#     else:
#         message={}
#     if request.method=='POST':
#         pass
#         return redirect(reverse('projectmanager:project_detail',args=[project]))
#     return render(request,'ProjectManager/form.html',locals())
#
# def add_expproject(request):
#     message={}
#     title = '添加实验项目'
#     url = reverse('projectmanager:add_expproject')
#     if request.method=='POST':
#         form=AddExpProject(request.POST)
#         if form.is_valid():
#             try:
#                 project=ExpProject(**form.cleaned_data)
#                 project.save()
#                 message['success']='保存成功'
#             except Exception as e:
#                 message['error']=e
#         else:
#             message['warning']='请检查表格'
#     form=AddExpProject()
#     return render(request,'ProjectManager/form.html',locals())
#
# def add_anaproject(request):
#     message={}
#     title='添加分析项目'
#     url= reverse('projectmanager:add_anaproject')
#     if request.method=='POST':
#         form=AddAnaProject(request.POST)
#         if form.is_valid():
#             try:
#                 project=AnaProject(**form.cleaned_data)
#                 project.save()
#                 message['success']='保存成功'
#             except Exception as e:
#                 message['error']=e
#         else:
#             message['warning']='请检查表格'
#     form=AddAnaProject()
#     return render(request,'ProjectManager/form.html',locals())
#
# def add_report(request):
#     pass
# 患者列表

def patient_index(request):
    columns='患者编号 患者姓名 患者年龄 患者性别 患者信息状态 患者样本状态 癌种  操作'.split()
    patient_list = Patient.objects().all()
    # return render(request,'ProjectManager/patient/patient.html',locals())
    patient_list=json.loads(patient_list.to_json(ensure_ascii=False))
    for i in patient_list:
        i['patientid']=i['_id']
    return HttpResponse(json.dumps({'data':patient_list},ensure_ascii=False))

#@csrf_exempt
def add_patient(request):
    # url=reverse('projectmanager:add_patient')
    message = {}
    # title='添加病人'
    logging.debug(request.body.decode('utf-8'))
    if request.method == 'POST':
        data=json.loads(request.body.decode('utf-8'))
        if len(Patient.objects(**data)) == 0:
            try:
                patient= Patient(**data)
                patient.save()
                message['success'] = '保存成功'
                # return redirect(reverse('projectmanager:patient_detail',args=[patient]))
            except Exception as e:
                message['error'] = e
        else:
            message['warning'] = '该患者编号已存在'
    # form = AddPatient()
    # return render(request, 'ProjectManager/form.html', locals())
    return HttpResponse(json.dumps(message,ensure_ascii=False))

def patient_addtask(request):
    # if request.session.get('message',None):
    #     message=request.session.pop('message')
    # else:
    #     message={}
    message={}

    # url = reverse('projectmanager:patient_order',args=[patient])
    if request.method=='POST':
        # data = Order(request.POST)
        # if data.is_valid():
        projectid = GenerateID(Project)
        data=json.loads(request.body.decode('utf-8'))
        patient = Patient.objects(pk=data['patientid']).first()
        try:
            tasks = []
            starttime = datetime.datetime.now()
            prodeadline=starttime
            for product in data['products']:
                product=Product.objects(productid=product).first()
                bestuptime = starttime+datetime.timedelta(days=product.bestuptime)
                worstuptime = starttime+datetime.timedelta(days=product.worstuptime)
                deadline = starttime+datetime.timedelta(days=product.worstuptime)
                prodeadline=max(deadline,prodeadline)
                task=GenerateID(Task)
                task=Task.objects(pk=task).first()
                task.modify(status='开始',
                            product=product,
                            patient=patient,
                            starttime=starttime,
                            bestuptime=bestuptime,
                            worstuptime=worstuptime,
                            deadline=deadline,
                            extrainfo=data.get('extrainfo','')
                )
                # task.save()
                tasks.append(task)
            # data['patients']=data['patients'].split()
            project = Project(pk=projectid,
                              patients=[patient],
                              products=data['products'],
                              tasks=tasks,
                              status='已付费',
                              duty=data['account'],
                              start_time=starttime,
                              deadline=prodeadline,
                              tag=data['tag']
                              )
            project.save()
            # project = project.modify(
            #
            #     )
            message['success'] = '保存成功'
            patient.modify(taskstatus='有')
        except Exception as e:
            message['error']=str(e)
            logging.debug(e)
        return HttpResponse(json.dumps(message, ensure_ascii=False))
        # else:
        #     message['warning']='请检查表格内容'
    # form=Order(initial={'projectid':GenerateID(Project),'patients':patient,'tag':'检测'})
    # return render(request,'ProjectManager/form.html',locals())
    elif request.method=="GET":
        data={}
        product_list = json.loads(Product.objects().all().to_json(ensure_ascii=False))
        for product in product_list:
            product['productid'] = product['_id']
        user_list=json.loads(User.objects().all().to_json(ensure_ascii=False))
        for user in user_list:
            user['account'] = user['_id']
        # data['projectid']=projectid
        data['product_list']=product_list
        data['user_list']=user_list
        return HttpResponse(json.dumps({'data':data},ensure_ascii=False))

def patient_add2project(request):
    message = {}
    # url = reverse('projectmanager:patient_order',args=[patient])
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        project=Project.objects(pd=data['projectid']).first()
        starttime = datetime.datetime.now()
        patient=data['patientid']
        project.patients.append(patient)
        for product in project.products:
            try:
                # product = Product.objects(productid=product).first()
                bestuptime = starttime + datetime.timedelta(days=product.bestuptime)
                worstuptime = starttime + datetime.timedelta(days=product.worstuptime)
                deadline = starttime + datetime.timedelta(days=product.worstuptime)
                task = GenerateID(Task)
                task = Task.objects(pk=task).first()
                task.modify(status='开始', product=product, patient=patient, starttime=starttime, bestuptime=bestuptime,
                            worstuptime=worstuptime, deadline=deadline)
                project.tasks.append(task)
            except Exception as e:
                logging.debug(e)
                message['error']=str(e)
        project.save()
        message['success']='添加患者成功'
    return HttpResponse(json.dumps(message,ensure_ascii=False))

def add_patient_batch(request):
    if request.session.get('message',None):
        message=request.session.pop('message')
    else:
        message={}
        request.session['message'] = message
    if request.method=='POST':
        form=FileUpload(request.POST,request.FILES)
        if form.is_valid():
            if request.FILES.get('file',None):
                f=handle_uploaded_file(request.FILES['file'])
                if os.path.getsize(f)==request.FILES['file'].size:
                    try:
                        fail=[]
                        warn=[]
                        message['warning']=''
                        data=pd.read_excel(f,header=0,sheetname=0,dtype=str)
                        for i in data.index:
                            row = data.loc[i].to_dict()
                            if len(Patient.objects(patientid=row['patientid'])) == 0:
                                try:
                                    patient=Patient(**row)
                                    patient.save()
                                except Exception as e:
                                    message['error'] = e
                                    fail.append(row['patientid']+ row['patientname'])
                            else:
                                warn.append(row['patientid']+row['patientname'])
                        message['warning'] += '以下患者编号已存在：%s' % ' '.join(warn)
                        message['warning'] += '以下患者保存失败：%s' % ' '.join(fail)
                        if request.session.get('ref',None):
                            return redirect(request.session.pop('ref'))
                        else:
                            return redirect(reverse('projectmanager:patient_index',args=['index']))
                    except Exception as e:
                        message['error']=e
                else:
                    message['error'] = '文件保存失败'
            else:
                message['error'] = '文件不存在'
        else:
            message['warning']='无效表格'
    reminder = '病人内容应该至少包括以下几列：patientid\tpatientname\tage\tgender\ttumortype ..请查询patient模型'
    url=reverse('projectmanager:add_patient_batch')
    form=FileUpload()
    return render(request,'ProjectManager/form.html',locals())

# def patient_detail(request,patient):
#     if request.session.get('message',None):
#         message=request.session.pop('message')
#     else:
#         message={}
#     request.session['message']=message
#     columns = '患者编号 患者姓名 年龄 性别 癌种 详细信息 样本信息'.split()
#     infocolumns='肿瘤级别 家族史 吸烟程度 PDL1治疗 MSI/MMR 手术 化疗 靶向治疗 免疫治疗 免疫药物 免疫治疗时间 器官移植 器官移植时间'.split()
#     samplecolumns='样本编号 样本类型 组织类型 接受时间 样本状态 收样人'.split()
#     try:
#         patient=Patient.objects(patientid=patient).first()
#         sample_list = Sample.objects(patient=patient).all()
#     except:
#         message['error']='无法找到该患者'
#     request.session['message']=message
#     infoform=Addinfo()
#     if request.method=='POST':
#         infoform=Addinfo(request.POST)
#         if infoform.is_valid():
#             try:
#                 patient.modify(infostatus='有',**infoform.cleaned_data)
#                 message['success']='修改成功'
#             except Exception as e:
#                 message['success'] = e
#                 infoform=Addinfo(initial=infoform.cleaned_data)
#     return render(request,'ProjectManager/patient/patient_detail.html',locals())


# 信息检索
def search(request):
    if request.method=="POST":
        data=json.loads(request.body.decode('utf-8'))
        patient_list=Patient.objects(**data).all()
        task_list=[]
        project_list=[]
        for patient in patient_list:
            task_list+=json.loads(Task.objects(patient=patient).all().to_json(ensure_ascii=False))
            project_list+=json.loads(Project.objects(patients__exists=str(patient)).all().to_json(ensure_ascii=False))
        for task in task_list:
            task['taskid'] = task['_id']
        for project in project_list:
            project['projectid'] = project['_id']
        data=[patient_list,project_list,task_list]
        return HttpResponse(json.dumps({'data':data},ensure_ascii=False))
    # url=reverse('projectmanager:search')
    # if request.session.get('message',None):
    #     message=request.session.pop('message')
    # if request.method=="POST":
    #     message = {}
    #     form=Search(request.POST)
    #     if form.is_valid():
    #         pcolumns='患者编号 患者姓名 年龄 性别 详细信息 样本信息'.split()
    #         if form.cleaned_data['patientid']:
    #             patient_list=Patient.objects(patientid=form.cleaned_data['patientid']).all()
    #         elif form.cleaned_data['patientname']:
    #             patient_list = Patient.objects(patientname=form.cleaned_data['patientname']).all()
    #         procolumn='项目编号 项目状态 截止日期 项目完成时间 项目延迟 项目'.split()
    #         project_list=[]
    #         taskcolumn='任务编号 患者编号 产品编号 任务状态 实验状态 分析状态 解读状态'.split()
    #         task_list=[]
    #         for patient in patient_list:
    #             project_list+=Project.objects(patients__exists=str(patient))
    #             task_list+=Task.objects(patient=patient).all()
    #         if form.cleaned_data['projectid']:
    #             project_list = Project.objects(projectid=form.cleaned_data['projectid']).all()
    #         message['success']='检索完成'
    #     else:
    #         message['error']='请检查表格'
    # form=Search()
    # return render(request,'ProjectManager/search.html',locals())

# 任务
## 任务列表
def task_index(request):
    if request.session.get('message',None):
        message=request.session.pop('message')
    # title='任务管理'
    # columns='任务编号 任务产品 患者编号 患者姓名 任务状态 分析状态 实验状态 解读状态 操作'.split()
    task_list = json.loads(Task.objects().all().to_json(ensure_ascii=False))
    task_list= [task for task in task_list if task.get('starttime')]
    product_list = json.loads(Product.objects().all().to_json(ensure_ascii=False))
    product_dict = {}
    for product in product_list:
        product_dict[product['_id']] = product
    for task in task_list:
        task['taskid']=task['_id']
        task['patientname']=Patient.objects(pk=task.get('patient')).first().patientname
        task['starttime'] = datetime.datetime.fromtimestamp(task['starttime']['$date']/1000).strftime('%Y-%m-%d %H:%M:%S')
        task['bestuptime'] = datetime.datetime.fromtimestamp(task['bestuptime']['$date']/1000).strftime('%Y-%m-%d %H:%M:%S')
        task['worstuptime'] = datetime.datetime.fromtimestamp(task['worstuptime']['$date']/1000).strftime('%Y-%m-%d %H:%M:%S')
        task['product'] = product_dict[task['product']]
    # return render(request, 'ProjectManager/task/task_index.html', locals())
    return HttpResponse(json.dumps({'data':task_list},ensure_ascii=False))

# ## 任务细节
# def task_detail(request,task):
#     task=Task.objects(pk=task).first()
#     taskcolumns = '任务编号 任务产品 任务病人 状态 分析状态 实验状态 解读状态 报告状态 操作'.split()
#     productcolumns = '产品编号 起始时间 最优上机实践 最迟下机时间 样本类型（control） 测序数据量（control）	样本类型（case）	测序数据量（case) 技术平台	生产芯片	测序策略	分子标签建库'.split()
#     return render(request,'ProjectManager/task/task_detail.html',locals())

# 任务操作
## 暂停实验
def task_pause_lab(request):
    message={}
    if request.method=='POST':
        data=json.loads(request.body.decode('utf-8'))
        logging.debug(data)
        task=Task.objects(pk=data['taskid']).first()
        info=str(task.info)
        info=info + data['info']
        try:
            task.modify(status='暂停',expstatus='暂停',info=info)
            message['success']='暂停成功'
        except Exception as e:
            message['error']=e
        # request.session['message']=message
    return HttpResponse(json.dumps(message,ensure_ascii=False))
    # return redirect(request.session['ref'])

## 暂停分析
def task_pause_ana(request):
    message={}
    # request.session['message'] = message
    if request.method=='POST':
        data=json.loads(request.body.decode('utf-8'))
        task=Task.objects(pk=data['taskid']).first()
        info=str(task.info)
        info=info+data['info']
        try:
            task.modify(status='暂停',anastatus='暂停',info=info)
            message['success']='暂停成功'
        except Exception as e:
            message['error']=str(e)
    return HttpResponse(json.dumps(message,ensure_ascii=False))
    # request.session['message']=message
    # return redirect(request.session['ref'])

## 暂停解读
def task_pause_jiedu(request):
    message={}
    # request.session['message'] = message
    if request.method=='POST':
        data=json.loads(request.body.decode('utf-8'))
        task=Task.objects(pk=data['taskid']).first()
        info=str(task.info)
        info = info + data['info']
        try:
            task.modify(status='暂停',jiedu_status='暂停',info=info)
            message['success']='暂停成功'
        except Exception as e:
            message['error']=e
    return HttpResponse(json.dumps(message,ensure_ascii=False))
    # request.session['message']=message
    # return redirect(request.session['ref'])

## 取消解读
def task_declare_jiedu(request):
    message = {}
    if request.method=='POST':
        data=json.loads(request.body.decode('utf-8'))
        task=Task.objects(pk=data['taskid']).first()
        info=str(task.info)
        info += data['info']
    # request.session['message'] = message
        try:
            task.modify(jiedu_status='无',reportstatus='无',info=info)
            message['success'] = '取消成功'
        except Exception as e:
            message['error'] = e
    return HttpResponse(json.dumps(message, ensure_ascii=False))
    # request.session['message'] = message
    # return redirect(request.session['ref'])

## 取消分析
def task_declare_ana(request):
    message = {}
    if request.method=='POST':
        data=json.loads(request.body.decode('utf-8'))
        task=Task.objects(pk=data['taskid']).first()
        info=task.info
        info += data['info']
        try:
            task.modify(anastatus='无')
            if task.jiedu_status=='wait':
                task.modify(jiedu_status='开始',info=info)
            message['success'] = '取消成功'
        except Exception as e:
            message['error'] = e
    return HttpResponse(json.dumps(message, ensure_ascii=False))
    # request.session['message'] = message
    # return redirect(request.session['ref'])

## 取消实验
def task_declare_lab(request):
    message = {}
    if request.method=='POST':
        data=json.loads(request.body.decode('utf-8'))
        task=Task.objects(pk=data['taskid']).first()
        info=str(task.info)
        info += data['info']
        # request.session['message'] = message
        try:
            task.modify(expstatus='无',anastatus='开始')
            message['success'] = '取消成功'
        except Exception as e:
            message['error'] = e
        # request.session['message'] = message
        # return redirect(request.session['ref'])
    return HttpResponse(json.dumps(message, ensure_ascii=False))

## 重置任务
def task_reset(request):
    message = {}
    if request.method=='POST':
        data=json.loads(request.body.decode('utf-8'))
        task=Task.objects(pk=data['taskid']).first()
        info=str(task.info)
        info =str(info)+ str(data['info'])
    # task = Task.objects(pk=task).first()
        try:
            task.modify(status='进行',expstatus='开始',anastatus='wait',jiedu_status='wait',reportstatus='wait')
            message['success'] = '重置成功'
        except Exception as e:
            message['error'] = str(e)
    return HttpResponse(json.dumps(message, ensure_ascii=False))
    # request.session['message'] = message
    # return redirect(request.session['ref'])

## 终止任务
def task_stop(request):
    message = {}
    if request.method=='POST':
        data=json.loads(request.body.decode('utf-8'))
        task=Task.objects(pk=data['taskid']).first()
        info=str(task.info)
        info += data['info']
        try:
            task.modify(status='终止',expstatus='终止',anastatus='终止',jiedu_status='终止')
            message['success'] = '终止成功'
        except Exception as e:
            message['error'] = e
    # request.session['message'] = message
    # return redirect(request.session['ref'])
    return HttpResponse(json.dumps(message, ensure_ascii=False))

## 任务分配
def task_distribute(request):
    message={}
    warning=[]
    if request.method=='POST':
        data=json.loads(request.body.decode('utf-8'))
        for task in data['tasks']:
            task=Task.objects(pk=task).first()
            try:
                task.modify(analyst=data['analyst'],jiedu=data['jiedu'])
            except:
                warning.append(task)
        message['success']='分配成功'
        if len(warning)!=0:
            message['warning']='以下任务分配失败'+'，'.join(warning)
        HttpResponse(json.dumps(message,ensure_ascii=False))
    else:
        users=User.objects().all().to_json(ensure_ascii=False)
        tasks=Task.objects(analyst=None).all().to_json(ensure_ascii=False)
        data={}
        data['user_list']=json.loads(users)
        data['task_list']=json.loads(tasks)
        return HttpResponse(json.dumps(data,ensure_ascii=False))

    # url = reverse('projectmanager:task_distribute')
    # form=TaskDistribute()
    # # form.fields['jiedu'].choices=zip(User.objects,User.objects)
    # # form.fields['analyst'].choices=zip(User.objects,User.objects)
    # # form.fields['tasks'].choices=[(str(task),str(task.patient)+'|'+str(task.product)) for task in Task.objects(analyst=None).all()]
    # return render(request,'ProjectManager/form.html',locals())


# 产品管理
def product_index(request):
    # if request.session.get('message',None):
    #     message=request.session.pop('message')
    # title='产品管理'
    # columns='产品编号 产品名称 产品手册 产品配置 产品周期 样本类型（control）' \
    #         '	测序数据量（control）	样本类型（case）	测序数据量（case）	' \
    #         '技术平台	 最优上机周期 最晚上机周期 生产芯片	  测序策略	分子标签建库 操作'.split()
    product_list=json.loads(Product.objects().all().to_json(ensure_ascii=False))
    for product in product_list:
        product['productid']=product['_id']
    # request.session['ref']=reverse('projectmanager:product_index')
    # return render(request,'ProjectManager/product/product.html',locals())
    return HttpResponse(json.dumps({'data':product_list},ensure_ascii=False))

# 添加或修改产品
def product_add(request):
    message={}
    if request.method=="POST":
        logging.debug('add_product:'+request.body.decode('utf-8'))
        # data=AddProduct(request.POST)
        # if data.is_valid():
        data=json.loads(request.body.decode('utf-8'))
        data.pop('_id')
        data.pop('isSelected')
        try:
            product=Product(**data)
            product.save()
            message['sucess']='产品保存/修改成功'
        except Exception as e:
            message['error']=str(e)
        # else:
        #     message['error']='请检查内容'
    else:
        message['warning'] = '请POST数据'
    return HttpResponse(json.dumps(message,ensure_ascii=False))
