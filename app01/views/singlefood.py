from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import SingleFoodInfoModelForm

table_title = '食品零售单位'
search_info = '溯源码'


def list(request):
    """ 显示信息表 """
    # 搜索功能
    data_dict = {}
    search_data = request.GET.get('q', "")  # 得到搜索框的数据
    if search_data:
        data_dict["traceID__contains"] = search_data  # __contains表示name字段中包含，类似于LIKE
    # 去数据库中获取所有的元组，如果查询框中有数据，则筛选数据
    queryset = models.SingleFoodInfo.objects.filter(**data_dict)
    # 自动生成表头名字
    table_head = []
    for item in models.SingleFoodInfo._meta.fields:
        table_head.append(item.verbose_name)

        # 2.实例化分页对象
    page_object = Pagination(request, queryset)

    context = {
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html(),  # 生成页码
        "search_data": search_data,
        "table_title": table_title,
        "search_info": search_info,
        "table_head": table_head,
        "form": SingleFoodInfoModelForm(),
    }
    return render(request, 'singlefood_list.html', context)


def add(request):
    """ 添加信息 """
    context = {
        "table_title": table_title,
        "method": "新建",
    }
    if request.method == "GET":
        form = SingleFoodInfoModelForm()
        context["form"] = form
        return render(request, 'add_edit.html', context)
    # 用户POST提交数据，数据校验。
    form = SingleFoodInfoModelForm(data=request.POST)
    if form.is_valid():
        # 如果数据合法，保存到数据库
        form.save()
        return redirect('/singlefood/list/')  # 页面重定向

    # 校验失败（在页面上显示错误信息）
    context["form"] = form
    return render(request, 'add_edit.html', context)


def delete(request):
    """ 删除信息 """
    nid = request.GET.get('nid')
    models.SingleFoodInfo.objects.filter(traceID=nid).delete()
    return redirect("/singlefood/list/")


def edit(request, nid):
    """ 修改信息 """
    context = {
        "table_title": table_title,
        "method": "编辑",
    }
    row_object = models.SingleFoodInfo.objects.filter(traceID=nid).first()
    if not row_object:
        # 数据不存在的情况，返回原编辑页面
        return redirect('/singlefood/list/')
    if request.method == "GET":
        # 根据ID去数据库获取要编辑的那一行数据（对象）
        form = SingleFoodInfoModelForm(instance=row_object)
        context["form"] = form
        return render(request, 'add_edit.html', context)

    form = SingleFoodInfoModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/singlefood/list/')
    context["form"] = form
    return render(request, 'add_edit.html', context)


table_head = ['周转号', '食品名', '批次号', '负责人', '设备名', '目的企业', '记录时间']


def info(request):
    """ 溯源信息展示 """
    if request.method == "GET":
        context = {
            "table_title": table_title,
            "search_info": search_info,
            "table_head": table_head,
        }
        traceid = request.GET.get('nid')
        if traceid:
            context['traceid'] = traceid
            batchid = models.SingleFoodInfo.objects.filter(traceID=traceid).first().batchID.batchID
            context['batchid'] = batchid
            trace_info_dict = find_trace_info(batchid)
            if len(trace_info_dict) > 0:
                context['trace_info_dict'] = trace_info_dict
        else:
            traceid = 2
            context['traceid'] = traceid
            batchid = models.SingleFoodInfo.objects.filter(traceID=traceid).first().batchID.batchID
            context['batchid'] = batchid
            trace_info_dict = find_trace_info(batchid)
            if len(trace_info_dict) > 0:
                context['trace_info_dict'] = trace_info_dict
        return render(request, 'qrcode.html', context)


import qrcode
import json
from io import BytesIO
from app01.utils.find_trace_info import find_trace_info


def image_qrcode(request):
    """ 生成溯源二维码 """
    if request.method == "GET":
        msg = request.GET.get('nid')
        # 查找所有周转信息
        trace_info_dict = find_trace_info(msg)
        # print(trace_info_dict)
        qr = qrcode.QRCode(
            version=1,  # 值为 1~40 的整数，控制二维码的大小（最小值是 1，是个 12×12 的矩阵）如果x想让程序自动确定，将值设置为 None 并使用 fit 参数即可。
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            # 控制二维码的错误纠正功能。可取值下列4个常量: ERROR_CORRECT_L：大约7%或更少的错误能被纠正。ERROR_CORRECT_M（默认）：大约 15%或更少的错误能被纠正。ERROR_CORRECT_H：大约30%或更少的错误能被纠正。
            box_size=30,  # 控制二维码中每个小格子包含的像素数，数值越小，图片越小
            border=4,  # 控制边框（二维码与图片边界的距离）包含的格子数（最小值和默认为 4，是相关标准规定的最小值）
        )
        message = ""
        for dict in trace_info_dict.values():
            message = message + "\n" + json.dumps(dict, ensure_ascii=False)
        # print(message)

        message = msg
        qr.make(fit=True)
        qr.add_data(message)
        img = qr.make_image()
        stream = BytesIO()  # 创建内存中的文件
        img.save(stream, format='PNG')  # 保存二维码 每个像素点为40像素大小
        return HttpResponse(stream.getvalue())

def security_code(request):
    """ 生成防伪二维码 """
    if request.method == "GET":
        msg = request.GET.get('nid')
        # print(trace_info_dict)
        qr = qrcode.QRCode(
            version=1,  # 值为 1~40 的整数，控制二维码的大小（最小值是 1，是个 12×12 的矩阵）如果x想让程序自动确定，将值设置为 None 并使用 fit 参数即可。
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            # 控制二维码的错误纠正功能。可取值下列4个常量: ERROR_CORRECT_L：大约7%或更少的错误能被纠正。ERROR_CORRECT_M（默认）：大约 15%或更少的错误能被纠正。ERROR_CORRECT_H：大约30%或更少的错误能被纠正。
            box_size=30,  # 控制二维码中每个小格子包含的像素数，数值越小，图片越小
            border=4,  # 控制边框（二维码与图片边界的距离）包含的格子数（最小值和默认为 4，是相关标准规定的最小值）
        )
        message = "validation:"+msg
        qr.make(fit=True)
        qr.add_data(message)
        img = qr.make_image()
        stream = BytesIO()  # 创建内存中的文件
        img.save(stream, format='PNG')  # 保存二维码 每个像素点为40像素大小
        return HttpResponse(stream.getvalue())

@csrf_exempt
def validate_food(request):
    "食品验证状态置为已验证"
    if request.method == "GET":
        id = request.GET.get('nid')
        row_object = models.SingleFoodInfo.objects.filter(traceID=id).first()
        if row_object:
            # 数据不存在的情况，返回错误
            print(row_object.get_status_display())
            form = SingleFoodInfoModelForm(data={"traceID":row_object.traceID,
                                                 "foodID":row_object.foodID.foodID,
                                                 "batchID":row_object.batchID.batchID,
                                                 "status":1}, instance=row_object)
            if form.is_valid():
                form.save()
            return HttpResponse(json.dumps({'success': "修改成功",
                                            'batchID': row_object.batchID.batchID}))
        return HttpResponse(json.dumps({'error': "找不到元组"}))