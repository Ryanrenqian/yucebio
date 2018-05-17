from django import forms
from .models import *
from datetime import datetime

class Addinfo(forms.Form):
    tumortype = forms.CharField(label='肿瘤类型')
    level = forms.CharField(label='肿瘤分级',required=False)
    relative = forms.ChoiceField(label='家族是否有其他人患癌',choices=[('未知','未知'),('是','是'),('否','否')])
    smoker = forms.ChoiceField(label='吸烟程度',choices=[('未知','未知'),('不吸烟','不吸烟'), ('轻度','轻度'), ('重度','重度')])
    PDL1 = forms.ChoiceField(label='是否做过PD-L1表达',choices=[('未知','未知'),('是','是'),('否','否')])
    MSIMMR = forms.ChoiceField(label='是否做过MSI/MMR检测',choices=[('未知','未知'),('是','是'),('否','否')])
    sugery = forms.ChoiceField(label='既往手术史',choices=[('未知','未知'),('是','是'),('否','否')])
    chemshistory = forms.ChoiceField(label='化疗史',choices=[('未知','未知'),('无','无'), ('术后辅助','术后辅助'), ('一线','一线'), ('二线','二线'), ('三线','三线')])
    targethistory = forms.ChoiceField(label='靶向史',choices=[('未知','未知'),('有','有'), ('无','无')])
    immuhistory = forms.ChoiceField(label='免疫治疗史',choices=[('未知','未知'),('有','有'), ('无','无')])
    immudrug = forms.CharField(label='免疫治疗药物',initial='无')
    immutime = forms.DateTimeField(label='免疫治疗时间',initial=datetime.today,required=False)
    explant = forms.ChoiceField(label='是否有过器官移植',choices=[('未知','未知'),('有','有'), ('无','无')])
    explanttime = forms.DateTimeField(label='移植时间',initial=datetime.today,required=False)

class AddProduct(forms.Form):
    productid=forms.CharField(label='产品编号')
    productname = forms.CharField(label='产品名称')
    book = forms.CharField(label='产品手册',required=False)
    config = forms.CharField(label='配置文件',required=False)
    period = forms.IntegerField(label='产品周期')
    normaltype = forms.CharField(label='样本类型（control',required=False)
    normalsize = forms.CharField(label='测序数据量（control）',required=False)
    tumortype = forms.CharField(label='样本类型（case）',required=False)
    tumorsize = forms.CharField(label='测序数据量（case）',required=False)
    platform = forms.CharField(label='技术平台',required=False)
    bestuptime = forms.IntegerField(label='最优上机周期（天）',required=False)
    worstuptime = forms.IntegerField(label='最坏上机时间（天）',required=False)
    chip = forms.CharField(label='生产芯片',required=False)
    strategy = forms.CharField(label='测序策略',required=False)
    moletag = forms.CharField(label='分子标签建库',required=False)


tags=['科研','检测']

class AddProject(forms.Form):
    def __init__(self, *args, **kwargs):
        super(AddProject, self).__init__(*args, **kwargs)
        self.fields['projectid']=forms.CharField(label='项目编号')
        self.fields['tag']=forms.ChoiceField(label='项目类别',choices=zip(tags,tags))
        self.fields['products']=forms.MultipleChoiceField(choices=zip(Product.objects().all(),Product.objects().all()),label='产品',widget=forms.CheckboxSelectMultiple())
        self.fields['patients']=forms.CharField(label='患者编号(使用空白分隔符填入多个样本)')
        self.fields['start_time']=forms.DateTimeField(label='开始日期')
        self.fields['deadline']=forms.DateTimeField(label='截止日期')
        self.fields['institute']=forms.CharField(label='合作单位',required=False)
        self.fields['duty']=forms.ChoiceField(label='负责人',choices=zip(User.objects,User.objects))



# strategies=Strategy.objects().all()
# stypes=Sampletypes.objects().all()
#
# class Order(forms.Form):
#     product=forms.ChoiceField(label='产品编号',choices=zip(products,products))
#     sampletypes=forms.MultipleChoiceField(choices=zip(stypes,stypes),label='样本要求',widget=forms.CheckboxSelectMultiple())
#     strategy=forms.ChoiceField(label='测序策略',choices=zip)
#     chip=forms.ChoiceField(label='芯片',choices=zip(chips,chips))
#     datasize = forms.CharField(label='测序量')
#     moletag = forms.CharField(label='分子标签')
#     best_xiaji_date = forms.DateTimeField(label='最优下机时间')
#     latest_xiaji_date = forms.DateTimeField(label='最迟下机时间')
#

#
# class AddExpProject(forms.Form):
#     project=forms.CharField(label='项目编号')
#     chip=forms.ChoiceField(label='芯片',choices=zip(chips,chips))
#     datasize=forms.CharField(label='测序量')
#     moletag=forms.CharField(label='分子标签')
#     best_xiaji_date=forms.DateTimeField(label='最优下机时间')
#     latest_xiaji_date=forms.DateTimeField(label='最迟下机时间')
#
# analyst=User.objects().all()
# class AddAnaProject(forms.Form):
#     project=forms.CharField(label='项目编号')
#     user=forms.ChoiceField(choices=zip(analyst,analyst),label='分析人员')
#
# class AddReport(forms.Form):
#     project=forms.ChoiceField(label='项目编号')
#     user=forms.ChoiceField(choices=zip(analyst,analyst),label='解读人员')

class Search(forms.Form):
    patientid=forms.CharField(label='患者编号',required=False)
    patientanme = forms.CharField(label='患者姓名', required=False)
    projectid = forms.CharField(label='项目编号', required=False)

yesorno=['未知','无','有']
genders=['男','女']
class AddPatient(forms.Form):
    patientid = forms.CharField(label='患者编号')
    patientname=forms.CharField(label='患者姓名')
    age=forms.IntegerField(label='患者年龄')
    tumortype = forms.CharField(label='癌种',required=False)
    gender=forms.ChoiceField(label='患者性别',choices=zip(genders,genders))
    infostatus=forms.ChoiceField(label='信息状态',choices=zip(yesorno,yesorno))
    samplestatus=forms.ChoiceField(label='收样状态',choices=zip(yesorno,yesorno))
    # projectstatus=forms.ChoiceField(label='项目状态',choices=zip(yesorno,yesorno))

class Order(forms.Form):
    projectid=forms.CharField(label='项目编号')
    tag = forms.ChoiceField(label='项目类别', choices=zip(tags, tags))
    patients=forms.CharField(label='患者编号')
    tumortype = forms.CharField(label='癌种',required=False)
    institute=forms.CharField(label='合作单位',required=False)
    duty=forms.CharField(label='负责人',required=False)
    extrainfo=forms.CharField(label='下单备注',required=False)
    def __init__(self, *args, **kwargs):
        super(Order,self).__init__(*args, **kwargs)
        self.fields['products']=forms.MultipleChoiceField(choices=zip(Product.objects,Product.objects),label='产品',widget=forms.CheckboxSelectMultiple())
        self.fields['duty']=forms.ChoiceField(choices=zip(User.objects().all(),User.objects().all()))


class FileUpload(forms.Form):
    filetype=forms.ChoiceField(label='文件类型：csv，txt，xlsx',choices=zip('csv,txt,xlsx'.split(','),'csv,txt,xlsx'.split(',')),required=False)
    file=forms.FileField(label='文件')

class ProjectAddTask(forms.Form):
    product=forms.ChoiceField(label='产品编号',choices=zip(Product.objects,Product.objects))
    patient=forms.CharField(label='患者编号')

# class TaskDistribute(forms.Form):
#     analyst=forms.ChoiceField(label='分析师')
#     jiedu=forms.ChoiceField(label='解读师')
#     tasks=forms.MultipleChoiceField(label='任务列表',widget=forms.CheckboxSelectMultiple())

class TaskDistribute(forms.Form):
    def __init__(self, *args, **kwargs):
        super(TaskDistribute, self).__init__(*args, **kwargs)
        self.fields['jiedu']=forms.ChoiceField(label='解读者',choices=zip(User.objects,User.objects))
        self.fields['analyst'] = forms.ChoiceField(label='分析者',choices=zip(User.objects, User.objects))
        self.fields['tasks'] = forms.MultipleChoiceField(label='任务列表',
            choices=[(str(task),str(task.patient)+'|'+str(task.product)) for task in Task.objects(expstatus='上机',analyst=None).all()],
            widget=forms.CheckboxSelectMultiple())

class ProjectID(forms.Form):
    project=forms.CharField(label='项目编号')

class TaskID(forms.Form):
    task=forms.CharField(label='任务编号')