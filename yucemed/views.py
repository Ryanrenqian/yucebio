from django.shortcuts import render,redirect,reverse
from .models import *
import json
from .forms import *
import datetime
# Create your views here.
def index(request):
    title='首页'
    return render(request,'yucemed/base.html',locals())


# patient part
def patientindex(request,key):
    title='患者总览'
    columns = '患者编号 患者姓名 患者年龄 患者性别 患者详细信息 样本信息 项目信息'.split()
    if key=='unorder':
        patient_list = Patient.objects(projectstatus='无').all()
    elif key=='index':
        patient_list = Patient.objects().all()
    return render(request,'yucemed/patient.html',locals())

def patientdetail(request,patient_id):
    title='患者数据'
    if len(Patient.objects(patientid=patient_id).all())==0:
        message='此患者不存在，请先添加'
    patient=Patient.objects(patientid=patient_id).all()[0]
    infos=PatientInfo.objects(patient=patient_id).all()
    infoform=Addinfo()
    projectform=AddProject()
    projects=Project.objects(patient=patient_id).all()
    return render(request,'yucemed/patient_detail.html',locals())


def addinfo(request,patient_id):
    if request.method=='POST':
        infoform=Addinfo(request.POST)
        title = "请检查内容"
        if infoform.is_valid():
            patient = Patient.objects(patientid=patient_id).all()[0]
            info=PatientInfo(patient=patient,**infoform.cleaned_data)
            title='keep info'
            info.save()
            patient.infostatus='有'
            title='keep patient'
            patient.save()
            title='No problem'
    patient = Patient.objects(patientid=patient_id).all()[0]
    infos = PatientInfo.objects(patient=patient).all()
    infoform = Addinfo()
    projectform = AddProject()
    return render(request, 'yucemed/patient_detail.html', locals())

def addproject(request,patient_id):
    if request.method=='POST':
        projectform=AddProject(request.POST)
        message='请检查内容'
        if projectform.is_valid():
            projectid=projectform.cleaned_data['projectid']
            if len(Project.objects(projectid=projectid).all())==0:
                productid = projectform.cleaned_data['productid']
                sampletype = projectform.cleaned_data['sampletype']
                chip = projectform.cleaned_data['chip']
                datasize = projectform.cleaned_data['datasize']
                strategy = projectform.cleaned_data['strategy']
                moletag = projectform.cleaned_data['moletag']
                best_xiaji_date = projectform.cleaned_data['best_xiaji_date']
                latest_xiaji_date = projectform.cleaned_data['latest_xiaji_date']
                sample = Sample.objects(patient=patient_id).all()[0]
                begintime = sample.recieve_date
                product = Product.objects(productid=productid).all()[0]
                deadline = begintime + datetime.timedelta(days=product.period)
                project = Project(
                    projectid=projectid,
                    patient=patient_id,
                    product=product,
                    deadline=deadline
                )
                project.save()
                patient = Patient.objects(patientid=patient_id).first()
                patient.projectstatus = '有'
                patient.save()
                try:
                    labproject = LabProject(project=projectid, sampletype=sampletype, chip=chip,
                                            datasize=datasize, strategy=strategy, moletag=moletag,
                                            best_xiaji_date=best_xiaji_date, latest_xiaji_date=latest_xiaji_date
                                            )
                    labproject.save()
                    message = '下单成功'
                except:
                    message['error']='Labproject 下单失败'
                else:
                    message['error'] = ''
    return redirect(reverse('yucemed:patientdetail',args=[patient_id]))
    # patient = Patient.objects(patientid=patient_id).all()[0]
    # infos = PatientInfo.objects(patient=patient_id).all()
    # infoform = Addinfo()
    # projectform=AddProject()
    # return render(request, 'yucemed/patient_detail.html', locals())

# product part
def product(request):
    columns='产品编号 产品名称 产品分析配置 产品周期'.split()
    product_list=Product.objects().all()
    form=AddProduct()
    return render(request,'yucemed/product.html',locals())

def addproduct(request):
    if request.method=="POST":
        productform=AddProduct(request.POST)
        error='请检查格式'
        if productform.is_valid():
            Product(**productform.cleaned_data).save()
            success='保存成功'
    return redirect(reverse('yucemed:product'))

# project part


def projectindex(request,key):
    title='项目管理'
    columns='项目编号 病人编号 产品编号 项目截止日期 项目剩余时间 项目状态 项目延时 数据下机时间 数据上机时间 备注'.split()
    if key=='index':
        project_list = Project.objects().all()
    elif key=='checkorder':
        project_list = Project.objects(status='待审查').all()
        columns.append('审查')
        return render(request, 'yucemed/project/checkorder.html', locals())
    elif key=='unanalyse':
        project_list = Project.objects(status='下机').all()
    elif key=='checkrecord':
        project_list = Project.objects(status='已解读').all()
    elif key=='unparse':
        project_list = Project.objects(status='已分析').all()
    elif key=='checkrecord':
        project_list = Project.objects(status='已解读').all()
    for project in project_list:
        if project.status not in [ '提交' , '暂停'] :
            project.duration=(project.deadline-datetime.datetime.now()).days
            if project.duration<0:
                project.delay='是'
            project.save()
    return render(request, 'yucemed/project/project.html', locals())

def ordercheck(request,project_id):
    project=Project.objects(projectid=project_id).first()
    if project.status=='待审查':
        project.status='下单'
    labpro=LabProject.objects(project=project).first()
    try:
        labpro.status='已下单'
        project.save()
        labpro.save()
    except:
        pass
    return redirect(reverse('yucemed:project',args=['checkorder']))

def pause(request,project_id):
    project = Project.objects(projectid=project_id).first()
    project.status='暂停'
    labpro = LabProject.objects(project=project).first()
    labpro.status = '暂停'
    project.save()
    labpro.save()
    redirect(reverse('yucemed.views.projectindex', args='checkorder'))

def projectdetail(request,porject_id):
    return render(request, 'yucemed/project/project_detail.html', locals())



