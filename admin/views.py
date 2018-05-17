from django.shortcuts import render
from django.shortcuts import render,redirect,reverse
from .models import *
from .forms import *
import datetime
import json
# Create your views here.
def project_index(request):
    if request.session.get('message',None):
        message=request.session.pop('message')
    columns='项目编号 患者编号 项目状态 截止日期 剩余日期 结束日期 延迟状态 实验状态 分析状态 解读状态'.split()
    project_list=Project.objects().all()
    for project in project_list:
        if project.status not in [ '提交' , '暂停'] :
            project.duration=(project.deadline-datetime.datetime.now()).days
            if project.duration<0:
                project.delay='是'
            project.save()
    form=AddProject()
    return render(request,'admin/project_index.html',locals())

def add_project(request):
    message = {}
    if request.method=="POST":
        form=AddProject(request.POST)
        if form.is_valid():
            if form.cleaned_data['patient']:
                if len(Patient.objects(patientid=form.cleaned_data['patient']).all())==1:
                    try:
                        project=Project(**form.cleaned_data)
                        project.save()
                        message['success']='保存成功'
                    except:
                        message['error']='保存失败'
                else:
                    message['error'] = '患者不存在'
            else:
                project = Project(**form.cleaned_data)
                project.save()
                message['success'] = '保存成功'
        else:
            message['info']='请检查内容'
    request.session['message']=message
    return redirect(reverse('admin:project_index'))

def delete_project(request,project):
    message={}
    try:
        Project.objects(projectid=project).delete()
        message['success']='操作成功'
    except:
        message['error']='操作失败'
    request.session['message']=message
    return redirect(reverse('admin:project_index'))

def modify_project(request,project):
    message={}
    if request.method=="POST":
        form=AddProject(request.POST)
        if form.is_valid():
            try:
                Project(**form.cleaned_data)
                message['success']='保存成功'
                request.session['message']=message
                return redirect(reverse('admin:project_index'))
            except:
                message['error']='保存失败'
        else:
            message['info']='请检查内容'
    request.session['message'] = message
    init=Project.objects(projectid=project).first().to_mongo().to_dict()
    init['projectid']=init['_id']
    form=AddProject(initial=init)
    url=reverse('admin:modify_project',args=[project])
    return render(request,'admin/modify.html',locals())

def user_index(request):
    if request.session.get('message',None):
        message=request.session['message']
    user_list = User.objects().all()
    form=AddUser()
    request.session['message'] = None
    return render(request, 'admin/user_index.html', locals())

def add_user(request):
    message={}
    if request.method=="POST":
        form=AddUser(request.POST)
        if form.is_valid():
            try:
                User(**form.cleaned_data).save()
                message['success']='保存成功'
            except:
                message['error']='保存失败'
        else:
            message['info']='请检查内容'
    request.session['message']=message
    return redirect(reverse('admin:user_index'))

def modify_user(request,user):
    message={}
    if request.method=="POST":
        form=AddUser(request.POST)
        if form.is_valid():
            User(**form.cleaned_data).save()
            message['success']='修改成功'
            request.session['message']=message
            return redirect(reverse('admin:user_index'))
        else:
            message['info']='请检查内容'
        init=user.to_mongo().to_dict()
    else:
        init=User.objects(account=user).first().to_mongo().to_dict()
        init['account']=init['_id']
    form=AddUser(initial=init)
    url=reverse('admin:modify_user',args=[user])
    return render(request,'admin/modify.html',locals())

def delete_user(request,user):
    message={}
    try:
        User.objects(account=user).delete()
        message['success']='操作成功'
    except:
        message['error']='操作失败'
    request.session['message']=message
    return redirect(reverse('admin:user_index'))

def patient_index(request):
    if request.session.get('message',None):
        message=request.session['message']
    columns='患者编号 患者姓名 患者性别'.split()
    patient_list=Patient.objects().all()
    form=AddPatient()
    request.session['message'] = None
    return render(request, 'admin/patient_index.html', locals())

def add_patient(request):
    message={}
    if request.method=="POST":
        form=AddPatient(request.POST)
        if form.is_valid():
            if len(Patient.objects(patientid=form.cleaned_data['patientid']))==0:
                try:
                    Patient(**form.cleaned_data).save()
                    message['success']='保存成功'
                except:
                    message['error']='保存失败'
            else:
                message['info']='病人已存在'
        else:
            message['error']='请检查内容'
    request.session['message']=message
    form=AddPatient()
    return redirect(reverse('admin:patient_index'))

def delete_patient(request,patient):
    message={}
    try:
        Patient.objects(patientid=patient).delete()
        message['success']='操作成功'
    except:
        message['error']='操作失败'
    request.session['message']=message
    return redirect(reverse('admin:patient_index'))

def modify_patient(request,patient):
    message={}
    if request.method=="POST":
        form=AddPatient(request.POST)
        if form.is_valid():
            try:
                patient=Patient.objects(patientid=patient).first()
                patient.modify(**form.cleaned_data).save()
                message['success']='保存成功'
                request.session['message'] = message
                return redirect(reverse('admin:patient_index'))
            except:
                message['error']='保存失败'
        else:
            message['info']='请检查内容'
    init=Patient.objects(patientid=patient).first().to_mongo().to_dict()
    init['patientid']=init['_id']
    form=AddPatient(initial=init)
    url = reverse('admin:modify_patient', args=[patient])
    request.session['message'] = message
    return render(request, 'admin/modify.html', locals())

def group_index(request):
    if request.session.get('message',None):
        message=request.session['message']
    group_list=Group.objects().all()
    form=AddGroup()
    request.session['message'] = None
    return render(request,'admin/group_index.html',locals())

def add_group(request):
    message={}
    if request.method=="POST":
        form=AddGroup(request.POST)
        if form.is_valid():
            try:
                Group(**form.cleaned_data).save()
                message['success']='保存成功'
            except:
                message['error']='保存失败'
        else:
            message['info']='请检查内容'
    request.session['message'] = message
    return redirect(reverse('admin:group_index'))

def delete_group(request,group):
    message = {}
    try:
        Group.objects(name=group).delete()
        message['success']='操作成功'
    except:
        message['error']='删除失败'
    request.session['message'] = message
    return redirect(reverse('admin:group_index'))

def chips_index(request):
    if request.session.get('message',None):
        message=request.session['message']
    chip_list=Chip.objects().all()
    form=AddChip()
    request.session['message']=None
    return render(request,'admin/chips_index.html',locals())

def add_chip(request):
    message = {}
    if request.method=="POST":
        form=AddChip(request.POST)
        if form.is_valid():
            try:
                Chip(**form.cleaned_data).save()
                message['success']='保存成功'
            except:
                message['error']='保存失败'
        else:
            message['info']='请检查内容'
    request.session['message'] = message
    return redirect(reverse('admin:chip_index'))
def delete_chip(request,chip):
    message={}
    try:
        Chip.objects(chip=chip).delete()
        message['success']='操作成功'
    except:
        message['error']='删除失败'
    request.session['message'] = message
    return redirect(reverse('admin:chip_index'))

def product_index(request):
    if request.session.get('message',None):
        message=request.session['message']
    columns='产品编号 产品名称 产品手册 config 产品周期 操作'.split()
    product_list=Product.objects().all()
    form=AddProduct()
    request.session['message'] = None
    return render(request,'admin/product_index.html',locals())

def add_product(request):
    message={}
    if request.method=="POST":
        form=AddProduct(request.POST)
        if form.is_valid():
            try:
                Product(**form.cleaned_data).save()
                message['success']='保存成功'
            except:
                message['error']='保存失败'
        else:
            message['info']='请检查内容'
    request.session['message'] = message
    return redirect(reverse('admin:product_index'))

def delete_product(request,product):
    message={}
    try:
        Product.objects(productid=product).delete()
        message['success']='操作成功'
    except:
        message['error']='删除失败'
    request.session['message'] = message
    return redirect(reverse('admin:product_index'))
def modify_product(request,product):
    message={}
    if request.method=="POST":
        form=AddProduct(request.POST)
        if form.is_valid():
            try:
                Product.objects(**form.cleaned_data).save()
                message['success']='修改成功'
                request.session['message'] = message
                return redirect(reverse('admin:product_index'))
            except:
                message['error']='保存失败'
        else:
            message['info']='请检查内容'
    init=Product.objects(productid=product).first().to_mongo.to_dict()
    init['productid']=init['_id']
    form=AddProduct(initial=init)
    url = reverse('admin:modify_product', args=[product])
    request.session['message'] = message
    return render(request, 'admin/modify.html', locals())