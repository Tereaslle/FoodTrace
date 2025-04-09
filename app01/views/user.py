from django.shortcuts import render, redirect, HttpResponse
from django.http.response import JsonResponse
from app01 import models
from django import forms
from app01.utils.form import UserModelForm, UserResetModelForm, LoginForm
from app01.utils.pagination import Pagination  # 添加分页模块
from app01.utils.code import check_code  # 引入验证码图片生成模块
from io import BytesIO

table_title = '用户'


def user_list(request):
    """ 显示用户信息表 """
    # 搜索功能
    data_dict = {}
    info_dict = request.session.get("info")
    if info_dict:
        if info_dict['type_name'] != '超级管理员':
            data_dict["userID"] = info_dict["id"]

    search_data = request.GET.get('q', "")  # 得到搜索框的数据
    if search_data:
        data_dict["name__contains"] = search_data  # __contains表示name字段中包含，类似于LIKE
    # 去数据库中获取所有的元组，如果查询框中有数据，则筛选数据
    queryset = models.UserInfo.objects.filter(**data_dict)

    # 自动生成表头名字
    table_head = []
    for item in models.UserInfo._meta.fields:
        table_head.append(item.verbose_name)

        # 2.实例化分页对象
    page_object = Pagination(request, queryset)
    context = {
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html(),  # 生成页码
        "search_data": search_data,
        "table_title": table_title,
        "table_head": table_head,
        "form": UserModelForm(),
    }
    return render(request, 'user_list.html', context)


def user_add(request):
    """ 添加用户信息(Ajax请求) """
    print(f'添加用户信息(Ajax请求):{request.POST}')
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()  # 如果数据合法，保存到数据库
        return JsonResponse({"status": True})

    return JsonResponse({"status": False, "error": form.errors})


def user_delete(request):
    """ 删除用户信息 """
    nid = request.GET.get('nid')
    models.UserInfo.objects.filter(userID=nid).delete()
    return redirect("/user/list/")


def user_edit(request, nid):
    """ 修改用户信息 """
    context = {
        "table_title": table_title,
        "method": "编辑",
    }
    row_object = models.UserInfo.objects.filter(userID=nid).first()
    if not row_object:
        return redirect('/user/list/')  # 数据不存在的情况，返回原编辑页面
    if request.method == "GET":
        # 根据ID去数据库获取要编辑的那一行数据（对象）
        form = UserModelForm(instance=row_object)
        context["form"] = form  # 一般编辑的modelform和添加的不是同一个，要单独设置
        return render(request, 'add_edit.html', context)

    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    context["form"] = form
    return render(request, 'add_edit.html', context)


def user_reset(request, nid):
    """ 重制用户密码 """
    row_object = models.UserInfo.objects.filter(userID=nid).first()
    if not row_object:
        return redirect('/user/list/')  # 数据不存在的情况，返回原编辑页面
    context = {
        "table_title": row_object.name,
        "method": "重制密码 - ",
    }
    if request.method == "GET":
        form = UserResetModelForm()
        context['form'] = form
        return render(request, 'add_edit.html', context)
    form = UserResetModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list')
    context['form'] = form
    return render(request, 'add_edit.html', context)


def login(request):
    """ 登录 """
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 去数据库校验用户名和密码是否正确，获取用户对象、None
        # admin_object = models.Admin.objects.filter(username=xxx, password=xxx).first()
        user_input_code = form.cleaned_data.pop('code')  # 一定要弹出code字段，因为数据库中不存，后面拿去查询会报错
        code = request.session.get('image_code', "")
        if code.upper() != user_input_code.upper():
            form.add_error("code", "验证码错误")
            return render(request, 'login.html', {'form': form})
        object = models.UserInfo.objects.filter(**form.cleaned_data).first()
        if not object:
            form.add_error("password", "用户名或密码错误")
            # form.add_error("username", "用户名或密码错误")
            return render(request, 'login.html', {'form': form})
        print(f"登陆用户{object.name}   类别：{object.get_type_display()}")
        # 网站生成随机字符串; 写到用户浏览器的cookie中；在写入到session中；
        request.session["info"] = {'id': object.userID,
                                   'name': object.name,
                                   'enterpriseID': object.enterpriseID.enterpriseID,    # object.enterpriseID取到的是外键的对象
                                   'type_num': object.type,
                                   'type_name': object.get_type_display()}
        # 更新session有效期，之前在image_code函数中是60s，现在session可以保存7天
        request.session.set_expiry(60 * 60 * 24 * 7)

        return redirect("/user/list/")

    return render(request, 'login.html', {'form': form})


def logout(request):
    """ 注销 """""
    request.session.clear()
    print("用户已注销")
    return redirect('/login/')


def image_code(request):
    """ 生成图片验证码 """

    # 调用pillow函数，生成图片
    img, code_string = check_code()

    # 写入到自己的session中（以便于后续获取验证码再进行校验）
    request.session['image_code'] = code_string
    # 给Session设置60s超时
    request.session.set_expiry(60)
    # 写入内存
    stream = BytesIO()  # 创建内存中的文件
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())


def test_ajax(request):
    print(request.POST)
    return HttpResponse("成功了")
