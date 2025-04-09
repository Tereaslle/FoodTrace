from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import FlowRecordModelForm,OperationRecordModelForm
from django.views.decorators.csrf import csrf_exempt
from app01.utils.find_trace_info import find_trace_info
import json


@csrf_exempt
def add(request):
    """ 上传周转数据 """
    if request.method == 'GET':
        print(f'添加周转信息(后端接口请求)GET方法:')
        return HttpResponse("上传GET请求成功")
    data_json = json.loads(request.body)
    print(f'添加周转信息(后端接口请求)POST方法:{data_json}  type{type(data_json)}')
    if "quality" not in data_json.keys():
        data_json["quality"]="无"
    form = FlowRecordModelForm({"foodID": data_json['foodID'],
                                "deviceID": data_json['deviceID'],
                                "batchID": data_json['batchID'],
                                "userID": data_json['userID'],
                                "enterpriseID": data_json['enterpriseID'],
                                "quality": data_json["quality"]})

    if form.is_valid():
        form.save()  # 如果数据合法，保存到数据库
        opertation_record = OperationRecordModelForm({"userID": data_json['userID'],
                                                      "deviceID": data_json['deviceID'],
                                                      "notes": "添加周转记录"})
        if opertation_record.is_valid():
            opertation_record.save()
            return JsonResponse({"status": True})

    return JsonResponse({"status": False, "error": form.errors})


@csrf_exempt
def trace_info(request):
    trace_info_dict = {}
    if request.method == 'GET':
        trace_id = request.GET.get('nid')
        if trace_id:
            trace_info_dict = find_trace_info(trace_id)
            if len(trace_info_dict) <= 0:
                trace_info_dict = {}
        else:
            trace_info_dict = {}
    else:

        # request.POST结果数据类型 <class 'django.http.request.QueryDict'>
        data_json = json.loads(request.body)
        print(f'查询溯源信息(后端接口请求):{data_json}')
        # trace_id = request.POST.get('nid', '')    # Content-type为application/json时 这句话不能获取到数据
        trace_id = data_json.get('nid', '')
        if trace_id != '':
            trace_info_dict = find_trace_info(trace_id)
            if len(trace_info_dict) <= 0:
                trace_info_dict = {}
    return HttpResponse(json.dumps(trace_info_dict))

@csrf_exempt
def search_single_food(request):
    single_food_info={}
    if request.method == 'GET':
        trace_id = request.GET.get('nid')
        if trace_id:
            singlefood_queryset = models.SingleFoodInfo.objects.filter(batchID=trace_id).first()
            # single_food_info= model_to_dict(singlefood_queryset)
            single_food_info['expire_date'] = singlefood_queryset.batchID.expireDate.strftime('%Y-%m-%d')
            single_food_info['status'] = singlefood_queryset.get_status_display()
            print(single_food_info)
        else:
            single_food_info = {'error':"未提供溯源码"}
    else:
        data_json = json.loads(request.body)
        print(f'查询食品单品信息(后端接口请求):{data_json}')
        trace_id = data_json.get('nid', '')
        if trace_id != '':
            singlefood_queryset = models.SingleFoodInfo.objects.filter(batchID=trace_id).first()
            single_food_info['expire_date'] = singlefood_queryset.batchID.expireDate.strftime('%Y-%m-%d')
            single_food_info['status'] = singlefood_queryset.get_status_display()
            print(single_food_info)
        else:
            single_food_info = {'error':"未提供溯源码"}
    return HttpResponse(json.dumps(single_food_info))