from django import forms


class BootScrap:
    bootstrap_exclude_fields = []

    def __init__(self, *args, **kwargs, ):
        super().__init__(*args, **kwargs)

        # 循环找到所有的插件，添加 form-control的样式
        for name, field in self.fields.items():
            if name in self.bootstrap_exclude_fields:
                continue
            if field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = field.label
            else:
                field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}


class BootScrapModelForm(BootScrap, forms.ModelForm):
    pass


class BootScrapForm(BootScrap, forms.Form):
    pass
