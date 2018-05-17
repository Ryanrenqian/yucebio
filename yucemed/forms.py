from django import forms
from .models import *
from datetime import datetime


types = [("FFPF", "FFPF"),
       ('血液', '血液'),
       ('血浆' ,'血浆'),
       ('DNA', 'DNA'),
       ('ctDNA', 'ctDNA'),
       ('RNA', 'RNA'),
       ('细胞', '细胞'),
       ('胸水', '胸水'),
       ('腹水', '腹水'),
       ('胸水/腹水沉渣(新鲜组织)','胸水/腹水沉渣(新鲜组织)'),
       ('脑脊液', '脑脊液'),
       ('尿液', '尿液'),
       ('fgS', 'fgS'),
       ('粪便', '粪便'),
       ('干血片', '干血片')
             ]
products=Product.objects().all()
users=User.objects.all()
chips=['Yuceone Target','YuceOne Plus','WES','ZPC','TMB','外送']


class Addinfo(forms.Form):
    tumortype = forms.CharField(label='肿瘤类型')
    level = forms.CharField(label='肿瘤分级',required=False)
    relative = forms.ChoiceField(label='家族是否有其他人患癌',choices=[('是','是'),('否','否')])
    smoker = forms.ChoiceField(label='吸烟程度',choices=[('不吸烟','不吸烟'), ('轻度','轻度'), ('重度','重度')])
    PDL1 = forms.ChoiceField(label='是否做过PD-L1表达',choices=[('是','是'),('否','否')])
    MSIMMR = forms.ChoiceField(label='是否做过MSI/MMR检测',choices=[('是','是'),('否','否')])
    sugery = forms.ChoiceField(label='既往手术史',choices=[('是','是'),('否','否')])
    chemshistory = forms.ChoiceField(label='化疗史',choices=[('无','无'), ('术后辅助','术后辅助'), ('一线','一线'), ('二线','二线'), ('三线','三线')])
    targethistory = forms.ChoiceField(label='靶向史',choices=[('有','有'), ('无','无')])
    immuhistory = forms.ChoiceField(label='免疫治疗史',choices=[('有','有'), ('无','无')])
    immudrug = forms.CharField(label='免疫治疗药物',initial='无')
    immutime = forms.DateTimeField(label='免疫治疗时间',initial=datetime.today,required=False)
    explant = forms.ChoiceField(label='是否有过器官移植',choices=[('有','有'), ('无','无')])
    explanttime = forms.DateTimeField(label='移植时间',initial=datetime.today,required=True)


class AddProject(forms.Form):
    projectid=forms.CharField(label='项目编号')
    productid=forms.ChoiceField(label='产品编号',choices=zip(products,products))
    sampletype = forms.ChoiceField(label='样本类型',choices=types)
    chip = forms.ChoiceField(label='芯片',choices=zip(chips,chips))
    datasize=forms.CharField(label='测序量')
    strategy=forms.ChoiceField(label='测序策略',choices=[('PEP151','PEP151')])
    moletag=forms.ChoiceField(label='分子标签',choices=[('是','是'),('否','否')])
    best_xiaji_date = forms.DateField(label='最优下机时间', initial=datetime.today)
    latest_xiaji_date = forms.DateField(label='最优上机时间', initial=datetime.today)

class AddProduct(forms.Form):
    productid=forms.CharField(max_length=20,label='产品编号')
    productname=forms.CharField(max_length=30,label='产品名称')
    config=forms.CharField(label='config文件')
    period=forms.IntegerField(min_value=1,label='实验周期')