from django.shortcuts import render, redirect
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import DeviceModelForm

table_title = '设备'
search_info = '设备名'

def list(request):
    """ 显示信息表 """
    # 搜索功能
    data_dict = {}
    info_dict = request.session.get("info")
    if info_dict:
        if info_dict['type_name'] != '超级管理员':
            data_dict["enterpriseID"] = info_dict["enterpriseID"]

    search_data = request.GET.get('q', "")  # 得到搜索框的数据
    if search_data:
        data_dict["name__contains"] = search_data  # __contains表示name字段中包含，类似于LIKE
    # 去数据库中获取所有的元组，如果查询框中有数据，则筛选数据
    queryset = models.DeviceInfo.objects.filter(**data_dict)
    # 自动生成表头名字
    table_head = []
    for item in models.DeviceInfo._meta.fields:
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
        "form": DeviceModelForm(),
    }
    return render(request, 'device_list.html', context)

def add(request):
    """ 添加信息 """
    context = {
        "table_title": table_title,
        "method": "新建",
    }
    if request.method == "GET":
        form = DeviceModelForm()
        context["form"] = form
        return render(request, 'add_edit.html', context)
    # 用户POST提交数据，数据校验。
    form = DeviceModelForm(data=request.POST)
    if form.is_valid():
        # 如果数据合法，保存到数据库
        form.save()
        return redirect('/device/list/') #页面重定向

    # 校验失败（在页面上显示错误信息）
    context["form"] = form
    return render(request, 'add_edit.html', context)


def delete(request):
    """ 删除信息 """
    nid = request.GET.get('nid')
    models.DeviceInfo.objects.filter(deviceID=nid).delete()
    return redirect("/device/list/")


def edit(request, nid):
    """ 修改信息 """
    context = {
        "table_title": table_title,
        "method": "编辑",
    }
    row_object = models.DeviceInfo.objects.filter(deviceID=nid).first()
    if not row_object:
        # 数据不存在的情况，返回原编辑页面
        return redirect('/device/list/')
    if request.method == "GET":
        # 根据ID去数据库获取要编辑的那一行数据（对象）
        form = DeviceModelForm(instance=row_object)
        context["form"] = form
        return render(request, 'add_edit.html', context)

    form = DeviceModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/device/list/')
    context["form"] = form
    return render(request, 'add_edit.html', context)