from django.shortcuts import render, redirect
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import OperationRecordModelForm

table_title = '操作记录'
search_info = '操作ID'

def list(request):
    """ 显示信息表 """
    # 搜索功能
    data_dict = {}
    search_data = request.GET.get('q', "")  # 得到搜索框的数据
    if search_data:
        data_dict["operateID__contains"] = search_data  # __contains表示name字段中包含，类似于LIKE
    # 去数据库中获取所有的元组，如果查询框中有数据，则筛选数据
    queryset = models.OperationRecord.objects.filter(**data_dict)
    # 自动生成表头名字
    table_head = []
    for item in models.OperationRecord._meta.fields:
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
        "form": OperationRecordModelForm(),
    }
    return render(request, 'operation_list.html', context)

def add(request):
    """ 添加信息 """
    context = {
        "table_title": table_title,
        "method": "新建",
    }
    if request.method == "GET":
        form = OperationRecordModelForm()
        context["form"] = form
        return render(request, 'add_edit.html', context)
    # 用户POST提交数据，数据校验。
    form = OperationRecordModelForm(data=request.POST)
    if form.is_valid():
        # 如果数据合法，保存到数据库
        form.save()
        return redirect('/operation/list/') #页面重定向

    # 校验失败（在页面上显示错误信息）
    context["form"] = form
    return render(request, 'add_edit.html', context)


def delete(request):
    """ 删除信息 """
    nid = request.GET.get('nid')
    models.OperationRecord.objects.filter(operateID=nid).delete()
    return redirect("/operation/list/")


def edit(request, nid):
    """ 修改信息 """
    context = {
        "table_title": table_title,
        "method": "编辑",
    }
    row_object = models.OperationRecord.objects.filter(operateID=nid).first()
    if not row_object:
        # 数据不存在的情况，返回原编辑页面
        return redirect('/operation/list/')
    if request.method == "GET":
        # 根据ID去数据库获取要编辑的那一行数据（对象）
        form = OperationRecordModelForm(instance=row_object)
        context["form"] = form
        return render(request, 'add_edit.html', context)

    form = OperationRecordModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/operation/list/')
    context["form"] = form
    return render(request, 'add_edit.html', context)