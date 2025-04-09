from django.db import models

# Create your models here.
from django.db import models
import django.utils.timezone as timezone
from django.core.validators import RegexValidator  # 正则表达式的模块


class EnterpriseInfo(models.Model):
    """ 企业表 """
    # 如果自己创建主键，django就不会自动给你创建id字段了
    enterpriseID = models.AutoField(verbose_name='企业ID', primary_key=True)
    name = models.CharField(verbose_name='企业名称', max_length=32)
    enterprise_choices = (
        (0, "生产企业"),
        (1, "经销企业"),
        (2, "零售企业"),
    )
    type = models.SmallIntegerField(verbose_name="企业类别", choices=enterprise_choices)
    organization_code = models.CharField(verbose_name='社会信用代码', max_length=18)
    permission_code = models.CharField(verbose_name="食品生产许可证编号", max_length=16)
    address = models.TextField(verbose_name='企业地址', default='无')
    create_time = models.DateField(verbose_name="成立日期", default=timezone.now)
    notes = models.TextField(verbose_name='备注', default='无')

    def __str__(self):
        return self.name  # 在modelform中显示外键为对象的输出函数，这里定义对象print时显示的值


class FoodInfo(models.Model):
    """ 食品信息表 """
    foodID = models.AutoField(verbose_name='食品ID', primary_key=True)
    enterpriseID = models.ForeignKey(verbose_name="所属企业", to="EnterpriseInfo", to_field="enterpriseID",
                                     on_delete=models.CASCADE)
    name = models.CharField(verbose_name="食品名称", max_length=50)
    weight = models.CharField(verbose_name='净含量', max_length=50, default='0')
    chemical_addition = models.TextField(verbose_name='化学食品添加剂', default='无')
    nutrition_table = models.TextField(verbose_name='营养成分表', default='无')
    create_time = models.DateField(verbose_name="登记日期", default=timezone.now)
    notes = models.TextField(verbose_name='备注', default='无')

    def __str__(self):
        return self.name  # 在modelform中显示外键为对象的输出函数，这里定义对象print时显示的值


class UserInfo(models.Model):
    userID = models.AutoField(verbose_name='用户ID', primary_key=True)
    name = models.CharField(verbose_name='用户名',
                            max_length=20,
                            unique=True,
                            validators=[RegexValidator(r'^(\w)+$', '用户名只能有字母数字下划线组成')])
    # \w表示字母下划线的表达式，+表示匹配(\w)表达式一次或多次
    account_num = models.CharField(verbose_name='账号', max_length=20, unique=True)
    password = models.CharField(verbose_name='密码',
                                max_length=20,
                                validators=[RegexValidator(r'^(?![a-z]+$)(?![A-Z]+$)(?!\d+$).{6,20}$',
                                                           '密码必须包含大写\小写字母、数字、特殊字符至少两种,且长度在6-20')]
                                )  # ?![a-z]+$  表示查找不是单纯以小写字母结束的字符串  . 表示匹配除换行符 \n 之外的任何单字符  .{6,20}表示对 . 匹配6-20次
    user_choices = (
        (0, "超级管理员"),
        (1, "企业级管理员"),
        (2, "终端管理员"),
    )
    type = models.SmallIntegerField(verbose_name="用户类别", choices=user_choices)
    enterpriseID = models.ForeignKey(verbose_name="所属企业", to="EnterpriseInfo", to_field="enterpriseID",
                                     on_delete=models.CASCADE, blank=True, null=True)
    create_time = models.DateField(verbose_name="创建日期", auto_now_add=True)  # 在创建时自动添加当前时间，且不可修改

    def __str__(self):
        return self.name  # 在modelform中显示外键为对象的输出函数，这里定义对象print时显示的值


class DeviceInfo(models.Model):
    """ 设备信息表 """
    deviceID = models.AutoField(verbose_name='设备ID', primary_key=True)
    enterpriseID = models.ForeignKey(verbose_name="所属企业", to="EnterpriseInfo", to_field="enterpriseID",
                                     on_delete=models.CASCADE, null=True)
    userID = models.ForeignKey(verbose_name="负责人", to="UserInfo", to_field="userID", on_delete=models.CASCADE,
                               null=True)
    name = models.CharField(verbose_name="设备名称", max_length=16)
    mac_code = models.CharField(verbose_name="MAC号", max_length=16)
    notes = models.TextField(verbose_name='备注', default='无')

    def __str__(self):
        return self.name  # 在modelform中显示外键为对象的输出函数，这里定义对象print时显示的值


class OperationRecord(models.Model):
    """ 操作记录信息表 """
    operateID = models.AutoField(verbose_name='操作ID', primary_key=True)
    userID = models.ForeignKey(verbose_name="负责人", to="UserInfo", to_field="userID", on_delete=models.CASCADE)
    deviceID = models.ForeignKey(verbose_name="操作设备", to="DeviceInfo", to_field="deviceID", on_delete=models.CASCADE)
    operate_datetime = models.DateTimeField(verbose_name="操作时间", auto_now_add=True)
    notes = models.TextField(verbose_name='操作内容', default='添加周转记录')

    def __str__(self):
        return str(self.operateID)  # 在modelform中显示外键为对象的输出函数，这里定义对象print时显示的值


class FoodbatchInfo(models.Model):
    """ 批次信息表 """
    batchID = models.AutoField(verbose_name='批次号', primary_key=True)
    foodID = models.ForeignKey(verbose_name="关联食品", to="FoodInfo", to_field="foodID", on_delete=models.CASCADE)
    amount = models.CharField(verbose_name='数量', max_length=20, default='0')
    quality = models.TextField(verbose_name='抽检结果', default='无')
    manufactureDate = models.DateField(verbose_name="生产日期", default=timezone.now)
    expireDate = models.DateField(verbose_name="截止日期")

    def __str__(self):
        return str(self.batchID)  # 在modelform中显示外键为对象的输出函数，这里定义对象print时显示的值


class FlowRecord(models.Model):
    """ 食品周转信息表 """
    flowID = models.AutoField(verbose_name='周转ID', primary_key=True)
    foodID = models.ForeignKey(verbose_name="关联食品", to="FoodInfo", to_field="foodID", on_delete=models.CASCADE)
    batchID = models.ForeignKey(verbose_name="生产批次号", to="FoodbatchInfo", to_field="batchID", on_delete=models.CASCADE)
    deviceID = models.ForeignKey(verbose_name="操作设备", to="DeviceInfo", to_field="deviceID", on_delete=models.CASCADE)
    userID = models.ForeignKey(verbose_name="负责人", to="UserInfo", to_field="userID", on_delete=models.CASCADE)
    enterpriseID = models.ForeignKey(verbose_name="目的企业", to="EnterpriseInfo", to_field="enterpriseID",
                                     on_delete=models.CASCADE, null=True)
    record_datetime = models.DateTimeField(verbose_name="记录时间", auto_now_add=True)
    quality = models.TextField(verbose_name='质检结果', default='无')

    def __str__(self):
        return str(self.flowID)  # 在modelform中显示外键为对象的输出函数，这里定义对象print时显示的值


class SingleFoodInfo(models.Model):
    """ 单个食品信息表 """
    traceID = models.AutoField(verbose_name='溯源码', primary_key=True)
    foodID = models.ForeignKey(verbose_name="关联食品", to="FoodInfo", to_field="foodID", on_delete=models.CASCADE)
    batchID = models.ForeignKey(verbose_name="生产批次号", to="FoodbatchInfo", to_field="batchID", on_delete=models.CASCADE)
    status_choices = (
        (0, "未被验证"),
        (1, "已被验证"),
    )
    status = models.SmallIntegerField(verbose_name="防伪状态", choices=status_choices, default=0)

    def __str__(self):
        return str(self.traceID)  # 在modelform中显示外键为对象的输出函数，这里定义对象print时显示的值


class MaterialInfo(models.Model):
    """ 食品原材料表 """
    id = models.AutoField(verbose_name='关联ID', primary_key=True)
    product = models.ForeignKey(verbose_name="产品", to="FoodInfo",
                                to_field="foodID", on_delete=models.CASCADE,
                                related_name="product")  # 定义了两个依赖相同表的外键，需要定义related_name的别名
    product_batch = models.ForeignKey(verbose_name="产品批次号", to="FoodbatchInfo",
                                      to_field="batchID", on_delete=models.CASCADE,
                                      related_name="product_batch")
    material = models.ForeignKey(verbose_name="原材料", to="FoodInfo",
                                 to_field="foodID", on_delete=models.CASCADE,
                                 related_name="material")
    material_batch = models.ForeignKey(verbose_name="原材料批次号", to="FoodbatchInfo",
                                       to_field="batchID", on_delete=models.CASCADE,
                                       related_name="material_batch")

    def __str__(self):
        return str(self.id)  # 在modelform中显示外键为对象的输出函数，这里定义对象print时显示的值
