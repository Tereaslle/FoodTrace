"""
URL configuration for FoodTrace project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app01.views import enterprise, user, food, device, operation, foodbatch, flowrecord, singlefood, material, esp32

urlpatterns = [
    # 展示溯源信息
    path('trace/info/', singlefood.info),
    path('trace/qrcode/', singlefood.image_qrcode),
    path('trace/security/qrcode/', singlefood.security_code),
    path('esp32/validate/food/', singlefood.validate_food),
    # 后端请求接口
    path('esp32/add/',esp32.add),
    path('esp32/trace/info/',esp32.trace_info),
    path('esp32/single/food/info/',esp32.search_single_food),

    # 登录
    path('login/', user.login),
    path('logout/', user.logout),
    path('image/code/', user.image_code),
    # 测试接口
    path('test/ajax/', user.test_ajax),

    # 企业信息管理
    path('enterprise/list/', enterprise.enterprise_list),
    path('enterprise/add/', enterprise.enterprise_add),
    path('enterprise/delete/', enterprise.enterprise_delete),
    path('enterprise/<int:nid>/edit/', enterprise.enterprise_edit),

    # 用户信息管理
    path('user/list/', user.user_list),
    path('user/add/', user.user_add),
    path('user/delete/', user.user_delete),
    path('user/<int:nid>/reset/', user.user_reset),
    path('user/<int:nid>/edit/', user.user_edit),

    # 食品信息管理
    path('food/list/', food.list),
    path('food/add/', food.add),
    path('food/delete/', food.delete),
    path('food/<int:nid>/edit/', food.edit),

    # 设备信息管理
    path('device/list/', device.list),
    path('device/add/', device.add),
    path('device/delete/', device.delete),
    path('device/<int:nid>/edit/', device.edit),

    # 操作记录信息管理
    path('operation/list/', operation.list),
    path('operation/add/', operation.add),
    path('operation/delete/', operation.delete),
    path('operation/<int:nid>/edit/', operation.edit),

    # 食品批次信息管理
    path('foodbatch/list/', foodbatch.list),
    path('foodbatch/add/', foodbatch.add),
    path('foodbatch/delete/', foodbatch.delete),
    path('foodbatch/<int:nid>/edit/', foodbatch.edit),

    # 食品周转信息管理
    path('flowrecord/list/', flowrecord.list),
    path('flowrecord/add/', flowrecord.add),
    path('flowrecord/delete/', flowrecord.delete),
    path('flowrecord/<int:nid>/edit/', flowrecord.edit),

    # 单位食品信息管理
    path('singlefood/list/', singlefood.list),
    path('singlefood/add/', singlefood.add),
    path('singlefood/delete/', singlefood.delete),
    path('singlefood/<int:nid>/edit/', singlefood.edit),

    # 原材料信息管理
    path('material/list/', material.list),
    path('material/add/', material.add),
    path('material/delete/', material.delete),
    path('material/<int:nid>/edit/', material.edit),
]
