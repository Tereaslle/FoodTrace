from django.shortcuts import render, redirect
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import EnterpriseModelForm

table_title = '企业'

def enterprise_list(request):
    """ 显示用户信息表 """
    # 搜索功能
    data_dict = {}
    search_data = request.GET.get('q', "")  # 得到搜索框的数据
    if search_data:
        data_dict["name__contains"] = search_data  # __contains表示name字段中包含，类似于LIKE
    # 去数据库中获取所有的元组，如果查询框中有数据，则筛选数据
    queryset = models.EnterpriseInfo.objects.filter(**data_dict)
    # 自动生成表头名字
    table_head = []
    for item in models.EnterpriseInfo._meta.fields:
        table_head.append(item.verbose_name)

        # 2.实例化分页对象
    page_object = Pagination(request, queryset)

    context = {
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html(),  # 生成页码
        "search_data": search_data,
        "table_title": table_title,
        "table_head": table_head,
        "form": EnterpriseModelForm(),
    }
    return render(request, 'enterprise_list.html', context)

def enterprise_add(request):
    """ 添加用户信息 """
    context = {
        "table_title": table_title,
        "method": "新建",
    }
    if request.method == "GET":
        form = EnterpriseModelForm()
        context["form"] = form
        return render(request, 'add_edit.html', context)
    # 用户POST提交数据，数据校验。
    form = EnterpriseModelForm(data=request.POST)
    if form.is_valid():
        # 如果数据合法，保存到数据库
        form.save()
        return redirect('/enterprise/list/') #页面重定向

    # 校验失败（在页面上显示错误信息）
    context["form"] = form
    return render(request, 'add_edit.html', context)


def enterprise_delete(request):
    """ 删除用户信息 """
    # 获取ID http://127.0.0.1:8000/enterprise/delete/?nid=1
    nid = request.GET.get('nid')
    # 删除
    models.EnterpriseInfo.objects.filter(enterpriseID=nid).delete()
    # 重定向回企业信息列表
    return redirect("/enterprise/list/")


def enterprise_edit(request, nid):
    """ 修改用户信息 """
    context = {
        "table_title": table_title,
        "method": "编辑",
    }
    row_object = models.EnterpriseInfo.objects.filter(enterpriseID=nid).first()
    if not row_object:
        # 数据不存在的情况，返回原编辑页面
        return redirect('/user/list/')
    if request.method == "GET":
        # 根据ID去数据库获取要编辑的那一行数据（对象）
        form = EnterpriseModelForm(instance=row_object)
        context["form"] = form
        return render(request, 'add_edit.html', context)

    form = EnterpriseModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # 如果用户提交数据校验成功
        # 默认保存的是用户输入的所有数据，如果想要再用户输入以外增加一点值
        # form.instance.字段名 = 值
        form.save()
        return redirect('/enterprise/list/')
    context["form"] = form
    return render(request, 'add_edit.html', context)