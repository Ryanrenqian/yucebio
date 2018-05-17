from .models import *
from django import forms
class AddGroup(forms.Form):
    name=forms.CharField(label='组名')

class AddUser(forms.Form):
    name=forms.CharField(label='姓名')
    account=forms.CharField(label='账号')
    password=forms.CharField(label='密码')
    region=forms.CharField(label='地区')
    email=forms.CharField(label='邮箱')
    telephone=forms.CharField(label='电话')
    group=forms.ChoiceField(label='组',choices=[(i,i) for i in Group.objects().all()])

tags=['科研','检测']
products = Product.objects().all()
user=User.objects()
class AddProject(forms.Form):
    _expstatus=['开始','进行中','暂停','完成' ]
    _anastatus=['开始','进行中','暂停','完成']
    _jiedu_status=['开始','进行中','暂停','完成']
    _status=['开始','进行中','暂停','完成']
    projectid = forms.CharField(label='项目名')
    institute=forms.CharField(label='合作单位')
    duty=forms.ChoiceField(label='负责人',choices=zip(user,user))
    tag = forms.ChoiceField(label='项目类别', choices=zip(tags, tags))
    products = forms.MultipleChoiceField(choices=zip(products, products), label='产品',
                                         widget=forms.CheckboxSelectMultiple())
    patients = forms.CharField(label='患者编号(使用空白分隔符填入多个样本)', required=False)
    status = forms.ChoiceField(label='项目状态',choices=zip(_status,_status))
    deadline = forms.DateTimeField(label='项目截止日期')
    finish = forms.DateTimeField(required=False,label='项目完成日期')
    delay = forms.CharField(label='是否延期',initial='否')
    expstatus = forms.ChoiceField(choices=zip(_expstatus,_expstatus),label='实验状态')
    anastatus = forms.ChoiceField(choices=zip(_anastatus,_anastatus),label='分析状态')
    jiedu_status = forms.ChoiceField(label='解读状态',choices=zip(_jiedu_status,_jiedu_status))

genders=['female','male']
class AddPatient(forms.Form):
    patientid=forms.CharField(label='患者编号')
    patientname=forms.CharField(label='姓名')
    age=forms.IntegerField(label='年龄')
    gender=forms.ChoiceField(label='性别',choices=zip(genders,genders))

class AddChip(forms.Form):
    chip=forms.CharField()


class AddProduct(forms.Form):
    productid=forms.CharField(max_length=20,label='产品编号')
    productname=forms.CharField(max_length=30,label='产品名称')
    config=forms.CharField(label='config文件')
    book=forms.CharField(label='产品手册')
    period=forms.IntegerField(min_value=1,label='产品周期')