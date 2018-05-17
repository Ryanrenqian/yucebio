from django.shortcuts import render,HttpResponse,get_object_or_404,redirect

# Create your tests here.

def medindex(request,**kwargs):
    patient_list=Patient.objects(**kwargs).all()
    content={'title':'病人管理'}
    content['patient_list']={}
    for patient in patient_list:
        content['patient_list'][patient]=(patient,Product[patient])
    return HttpResponse(content)

