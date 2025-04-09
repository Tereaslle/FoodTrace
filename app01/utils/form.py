from app01 import models
from django.core.exceptions import ValidationError
from django import forms
from app01.utils.bootstrap import BootStrapModelForm  # 给你自动生成的models添加样式
from app01.utils.encrypt import md5  # 引入md5加密


class EnterpriseModelForm(BootStrapModelForm):
    # 这里面还得加验证规则
    class Meta:
        model = models.EnterpriseInfo
        exclude = ["enterpriseID"]  # 排除该字段
        # fields = "__all__" #选取所有字段
        # fields = ["name", "type", "organization_code", "address", "create_time"] #自由选择字段
        widgets = {
            # create_time 字段使用DateInput输入框，属性添加placeholder
            "create_time": forms.DateInput(attrs={"placeholder": "请输入日期"})
        }

    # 验证用户输入的正确性，钩子方法
    def clean_organization_code(self):  # 函数名为clean_字段名
        # 验证18位的社会信息代码
        # 获取用户输入的值
        text_organization_code = self.cleaned_data["organization_code"]
        if len(text_organization_code) != 18:
            # 如果验证不通过
            raise ValidationError(f"社会统一信用代码为18位，目前输入{len(text_organization_code)}位")
        # 获取主键
        pk = self.instance.pk
        # 验证唯一的社会信用代码，注意要排除自己，否则编辑的时候一定会报错
        exists = models.EnterpriseInfo.objects.exclude(enterpriseID=pk).filter(
            organization_code=text_organization_code).exists()
        if exists:
            raise ValidationError("该社会统一信用代码已注册")
        return text_organization_code


class UserModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(
            render_value=True,
            attrs={'class': "form-control", "placeholder": "Password"}
        ),  # 自己创建的字段只能在这里添加widget

    )

    class Meta:
        model = models.UserInfo
        fields = ['name', 'account_num', 'password', 'confirm_password', 'type', 'enterpriseID']
        widgets = {
            'password': forms.PasswordInput(render_value=True),  # render_value=True 表示密码出错了不会清空
        }

    def clean_account_num(self):  # 函数名为clean_字段名
        text_account_num = self.cleaned_data["account_num"]  # 获取用户输入的值
        pk = self.instance.pk  # 获取主键
        # 注意要排除自己，否则编辑的时候一定会报错
        exists = models.EnterpriseInfo.objects.exclude(enterpriseID=pk).filter(
            organization_code=text_account_num).exists()

        if exists:
            raise ValidationError("该账号已注册")
        return text_account_num

    def clean_password(self):
        password = self.cleaned_data.get("password")
        # return md5(password)
        return password

    def clean_confirm_password(self):
        # confirm_password = md5(self.cleaned_data["confirm_password"])
        confirm_password = self.cleaned_data.get("confirm_password")
        password = self.cleaned_data.get("password")
        if confirm_password != password:
            raise ValidationError("密码不一致")
        # 返回值将会替换原confirm_password的值，如果confirm_password要保存数据库，也会保存返回的值
        return confirm_password


class UserResetModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True),  # 自己创建的字段只能在这里添加widget

    )

    class Meta:
        model = models.UserInfo
        fields = ['password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput(render_value=True),  # render_value=True 表示密码出错了不会清空
        }

    def clean_password(self):
        password = self.cleaned_data.get("password")
        md5_pwd = md5(password)
        # 去数据库校验当前密码和新输入的密码是否一致
        exists = models.UserInfo.objects.filter(userID=self.instance.pk, password=password).exists()
        if exists:
            raise ValidationError("不能与以前的密码相同")
        return password

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data.get("confirm_password")
        password = self.cleaned_data.get("password")
        if confirm_password != password:
            raise ValidationError("密码不一致")
        # 返回值将会替换原confirm_password的值，如果confirm_password要保存数据库，也会保存返回的值
        return confirm_password


class LoginForm(forms.Form):
    name = forms.CharField(
        label='用户名',
        widget=forms.TimeInput(attrs={'class': "form-control"}),
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(render_value=True, attrs={'class': "form-control"}),
    )
    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput(attrs={'class': "form-control", "placeholder": "请输入验证码"}),
        required=True
    )

    def clean_password(self):
        password = self.cleaned_data.get("password")
        return password


class FoodModelForm(BootStrapModelForm):
    class Meta:
        model = models.FoodInfo
        exclude = ["foodID"]  # 排除该字段
        widgets = {
            "create_time": forms.DateInput(attrs={"placeholder": "请输入日期"})
        }


class DeviceModelForm(BootStrapModelForm):
    class Meta:
        model = models.DeviceInfo
        exclude = ["deviceID"]  # 排除该字段


class OperationRecordModelForm(BootStrapModelForm):
    class Meta:
        model = models.OperationRecord
        exclude = ["operateID"]  # 排除该字段


class FoodbatchModelForm(BootStrapModelForm):
    class Meta:
        model = models.FoodbatchInfo
        exclude = ["batchID"]  # 排除该字段


class FlowRecordModelForm(BootStrapModelForm):
    class Meta:
        model = models.FlowRecord
        exclude = ["flowID"]  # 排除该字段


class SingleFoodInfoModelForm(BootStrapModelForm):
    class Meta:
        model = models.SingleFoodInfo
        exclude = ["traceID"]  # 排除该字段


class MaterialInfoModelForm(BootStrapModelForm):
    class Meta:
        model = models.MaterialInfo
        exclude = ["id"]  # 排除该字段
