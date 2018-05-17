from django.db import models
from datetime import datetime
# Create your models here.
from mongoengine import *
connect('test')

# User admin

class User(Document):
    name=StringField(primary_key=True)
    account=StringField(unique=True)
    password=StringField()
    def __str__(self):
        return self.name

class Group(Document):
    name=StringField(primary_key=True)
    user=ListField(User)
    def __str__(self):
        return self.name

# patient info
class Product(Document):
    productid=StringField(max_length=20,primary_key=True)
    productname=StringField(max_length=30)
    config=StringField(max_length=30)
    book=StringField()
    period=IntField()
    def __str__(self):
        return self.productid
class Patient(Document):
    patientid=StringField(max_length=30,primary_key=True)
    patientname=StringField(max_length=30)
    age=IntField()
    gender=StringField(choices=['female','male'])
    infostatus=StringField(default='无',choices=['有','无'])
    samplestatus = StringField(default='无',choices=['有', '无'])
    projectstatus=StringField(default='无',choices=['有', '无'])
    def __str__(self):
        return self.patientid
class PatientInfo(Document):
    patient=ReferenceField(Patient)
    tumortype=StringField(null=True)
    level=StringField(null=True)
    relative=StringField(choices=['否','是'],null=True)
    smoker=StringField(null=True,choices=['不吸烟','轻度','重度'])
    PDL1=StringField(choices=['是','否'],null=True)
    MSIMMR=StringField(choices=['否','是'],null=True)
    sugery=StringField(choices=['否','是'],null=True)
    chemshistory=StringField(null=True,choices=['无','术后辅助','一线','二线','三线'])
    targethistory=StringField(null=True,choices=['无','有'])
    immuhistory=StringField(null=True,choices=['有','无'])
    immudrug=StringField(null=True)
    immutime=DateTimeField(null=True)
    explant=StringField(null=True,choices=['有','无'])
    explanttime=DateTimeField(null=True)
    def __str__(self):
        return 'PationInfo:'+str(self.patient)
types='FFPF 血液 血浆 DNA ctDNA RNA 细胞 胸水 腹水 脑脊液 唾液 尿液 口腔拭子 粪便 fgs 干血片 胸水/腹水沉渣(新鲜组织)'.split()

class Sample(Document):
    sampleid=StringField(primary_key=True)
    patient=ReferenceField(Patient)
    times = IntField(max_value=9, default=0)
    sampletype = StringField(choices=['Tumor', 'Normal'])
    tissuetype = StringField(choices=types)
    recieve_date = DateTimeField()
    detect_date = DateTimeField(null=True)
    user = ReferenceField(User,null=True)
    status=StringField(choices=['无需反样','未反样','已反样'])
    def __str__(self):
        return self.sampleid

# med project
class Project(Document):
    projectid=StringField(primary_key=True)
    patient=ReferenceField(Patient,null=True)
    product=ReferenceField(Product)
    deadline=DateTimeField()
    duration=IntField(null=True)
    status=StringField(default='待审查',choice=['待审查','下单','实验','上机','下机','分析中','已分析','已解读','报告审核','提交','暂停'])
    delay=StringField(default='否',choice=['是','否'])
    xiajitime=DateTimeField(null=True)
    shangjitime=DateTimeField(null=True)
    Normal = StringField(null=True)
    Tumor = StringField(null=True)
    extra=StringField()
    def __str__(self):
        return self.projectid

class Experiment(EmbeddedDocument):
    QC=StringField()
    conclusion=StringField()
    suggestion=StringField()

chips=['Yuceone Target','YuceOne Plus','WES','ZPC','TMB','外送']
class LabProject(Document):
    project = ReferenceField(Project)
    sampletype = StringField(choices=types)
    chip = StringField(choices=chips)
    datasize = StringField()
    strategy = StringField(choices=['PEP151'])
    moletag = StringField(choices=['是','否'])
    best_xiaji_date = DateTimeField(label='最优下机时间')
    latest_xiaji_date = DateTimeField(label='最优上机时间')
    status = StringField(default='待审核',
                         choice=[ '待审核','已下单', '实验中', '实验完成','上机', '下机',  '暂停'])
    delay = StringField(default='否', choice=['是', '否'])
    experiments=ListField(EmbeddedDocumentField(Experiment))
    def __str__(self):
        return str(self.project)

class MedProject(Document):
    projectid=ReferenceField(Project)
    execute=ReferenceField(User,null=True)
    workdir=StringField(null=True)













