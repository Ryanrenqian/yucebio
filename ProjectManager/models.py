from mongoengine import *
connect('test')
# Create your models here.


# 用户
class User(Document):
    '''
    账户
    姓名
    地区
    邮箱
    电话
    部门
    '''
    account=StringField(primary_key=True)
    name = StringField()
    region=StringField()
    email=StringField()
    telephone=StringField()
    department=StringField()
    def __str__(self):
        return self.account

# 产品
class Product(Document):
    '''
    产品编号
    产品名称
    产品手册（存储位置）
    产品周期（时长）
    样本类型（control）
    测序数据量（control）
    样本类型（case）
    测序数据量（case）
    技术平台
    最优上机时间
    最迟上机时间
    生产芯片
    测序策略
    分子标签建库
    '''
    productid = StringField(max_length=20, primary_key=True)
    productname = StringField(max_length=30)
    book=StringField(null=True)
    config = StringField(max_length=30)
    period = IntField()
    normaltype = StringField(null=True)
    normalsize = StringField(null=True)
    tumortype = StringField(null=True)
    tumorsize = StringField(null=True)
    platform = StringField(null=True)
    bestuptime=IntField(default=0)
    worstuptime=IntField(default=0)
    chip = StringField(null=True)
    strategy = StringField(null=True)
    moletag = StringField(null=True)
    def __str__(self):
        return self.pk


# 患者
class Patient(Document):
    '''
    患者编号
    患者姓名
    癌种
    年龄
    性别
    信息添加状态
    样本添加状态
    任务添加状态
    肿瘤分级
    家族患癌史
    吸烟程度
    是否做过PDL1表达
    MSIMMR
    '''
    patientid=StringField(max_length=30,primary_key=True)
    patientname=StringField(max_length=30)
    tumortype = StringField(null=True)
    age=IntField()
    gender=StringField(null=True)
    infostatus=StringField(default='无')
    samplestatus = StringField(default='无')
    taskstatus = StringField(default='无')
    level=StringField(null=True)
    relative=StringField(null=True)
    smoker=StringField(null=True)
    PDL1=StringField(null=True)
    MSIMMR=StringField(null=True)
    sugery=StringField(null=True)
    chemshistory=StringField(null=True)
    targethistory=StringField(null=True)
    immuhistory=StringField(null=True)
    immudrug=StringField(null=True)
    immutime=DateTimeField(null=True)
    explant=StringField(null=True)
    explanttime=DateTimeField(null=True)
    def __str__(self):
        return self.patientid

class Sample(Document):
    _id=StringField(primary_key=True)
    patient=ReferenceField(Patient)
    kind=StringField(null=True)
    tissue=StringField(null=True)
    receive=DateTimeField(null=True)
    status=StringField(null=True)
    receiver=StringField(null=True)
    receivestatus=StringField(default='已收样')
    def __str__(self):
        return self.pk
    def dict(self):
        data=''
# 任务
class Task(Document):
    product=ReferenceField(Product)
    patient=ReferenceField(Patient)
    tumor=StringField(null=True)
    starttime=DateTimeField(null=True)
    bestuptime=DateTimeField(null=True)
    worstuptime=DateTimeField(null=True)
    deadline=DateTimeField(null=True)
    status = StringField(null=True)
    expstatus = StringField(default='开始')
    anastatus = StringField(default='wait')
    jiedu_status = StringField(default='wait')
    reportstatus = StringField(default='wait')
    analyst= StringField(null=True)
    jiedu=StringField(null=True)
    rawdata=StringField(null=True)
    data=StringField(null=True)
    report=StringField(null=True)
    info=StringField(null=True)
    extrainfo=StringField(null=True)
    def __str__(self):
        return str(self.pk)

# 项目
class Project(Document):
    projectid=StringField(primary_key=True)
    tag=StringField(default='检测',choices=['科研','检测'])
    products = ListField(ReferenceField(Product))
    patients= ListField(ReferenceField(Patient))
    tasks=ListField(ReferenceField(Task),null=True)
    institute=StringField(null=True)
    duty=ReferenceField(User,null=True)
    status=StringField(default='待审查',choice=['待审查','未缴费','已付费/免费','已完成','暂停','已作废'])
    start_time=DateTimeField(null=True)
    deadline = DateTimeField(null=True)
    duration=IntField(null=True)
    finish=DateTimeField(null=True)
    delay = StringField(default='否')
    def __str__(self):
        return self.pk


# Lab管理部分

# class Labtask(Document):
#     task=ReferenceField(Task)
#     chip=ReferenceField(Chip)
#     datasize=StringField()
#     moletag=StringField()
#     best_xiaji_date=DateTimeField()
#     latest_xiaji_date=DateTimeField()
#     shangji_date=DateTimeField()
#     xiaji_date=DateTimeField()
#     def __str__(self):
#         return str(self.project)
#
#
# # 样本管理
# types='FFPF 血液 血浆 DNA ctDNA RNA 细胞 胸水 腹水 脑脊液 唾液 尿液 口腔拭子 粪便 fgs 干血片 胸水/腹水沉渣(新鲜组织)'.split()
#
# class Sample(Document):
#     sampleid=StringField(primary_key=True)
#     patient=ReferenceField(Patient)
#     times = IntField(max_value=9, default=0)
#     sampletype = StringField(choices=['Tumor', 'Normal'])
#     tissuetype = StringField(choices=types)
#     recieve_date = DateTimeField()
#     detect_date = DateTimeField(null=True)
#     user = ReferenceField(User,null=True)
#     status=StringField(choices=['无需反样','未反样','已反样'])
#     def __str__(self):
#         return self.sampleid
# # 实验参数
#
# class TiquShiji(Document):
#     name=StringField(primary_key=True)
#     def __str__(self):
#         return self.name
#
# class JiankuShiji(Document):
#     name=StringField(primary_key=True)
#     def __str__(self):
#         return self.name
#
# class I5(Document):
#     name=StringField(primary_key=True)
#
#
# # 实验内容
# class Experiment(Document):
#     experimentid=StringField(primary_key=True)
#     task=ReferenceField(Task)
#
#
# ##  分析解读师管理部分
# class AnaProject(Document):
#     taskid = StringField(primary_key=True)
#     project=ReferenceField(Project)
#     patient=ReferenceField(Patient)
#     product=ReferenceField(Product)
#     user=ReferenceField(User)
#     workspace=StringField(null=True)
#     samplelist=StringField(null=True)
#     getsample=StringField(null=True)
#     generator=StringField(null=True)
#     pairedlist=StringField(null=True)
#     config=StringField(null=True)
#     status=StringField(default='分析中',choices=['分析中','已完成','暂停'])
#
# ## report parse
# class Report(Document):
#     project=ReferenceField(Project)
#     user=ReferenceField(User)
#     result=StringField(null=True)
#     status=StringField(default='待解读',choices=['待解读','解读中','待审核','已完成'])
