from django import forms
import  datetime
from .models import *
class SubmitTask(forms.Form):
    task = forms.CharField(label='任务编号')
    rawdata=forms.CharField(label='测序数据路径')

class PauseTask(forms.Form):
    task=forms.CharField(label='任务编号')
    info=forms.CharField(label='暂停原因')

class AddSample(forms.Form):
    patient=forms.CharField(label='患者编号')
    _id=forms.CharField(label='样本编号')
    kind=forms.ChoiceField(label='类型',choices=[('肿瘤','肿瘤'),('正常','正常')])
    tissue=forms.CharField(label='组织形态')
    receive=forms.DateField(label='收样时间',initial=datetime.datetime.now())
    receiver=forms.CharField(label='收样人')
    status=forms.CharField(label='样本状态',required=False)


class Search(forms.Form):
    patientid = forms.CharField(label='患者编号', required=False)
    patientanme = forms.CharField(label='患者姓名', required=False)
    sampleid = forms.CharField(label='样本编号',required=False)