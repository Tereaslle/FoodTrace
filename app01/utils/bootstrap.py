from django import forms

from django import forms


class BootStrap:
    bootstrap_exclude_fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环ModelForm中的所有字段，给每个字段的插件设置
        for name, field in self.fields.items():
            # 字段中有属性，保留原来的属性，没有属性，才增加。
            if field.widget.attrs:
                if name in ["type", "enterpriseID"]:
                    field.widget.attrs["class"] = "form-select"
                else:
                    field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = name
            else:
                if name in ["type", "enterpriseID"]:
                    field.widget.attrs = {
                        "class": "form-select"
                    }
                else:
                    field.widget.attrs = {
                        "class": "form-control"
                    }
                field.widget.attrs["placeholder"] = name

            if name == "create_time":
                field.widget.attrs["placeholder"] = "请输入日期"


class BootStrapModelForm(BootStrap, forms.ModelForm):
    pass


class BootStrapForm(BootStrap, forms.Form):
    pass


