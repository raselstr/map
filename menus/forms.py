from django import forms
from django.contrib.auth import get_user_model

from config.forms import BaseAppModelForm

from .models import Menu, Role, RolePermission, SubMenu


User = get_user_model()


class MenuForm(BaseAppModelForm):
    class Meta:
        model = Menu
        fields = ["nama", "icon", "urutan", "aktif"]


class SubMenuForm(BaseAppModelForm):
    class Meta:
        model = SubMenu
        fields = ["menu", "nama", "url_name", "icon", "urutan", "aktif"]


class RoleForm(BaseAppModelForm):
    class Meta:
        model = Role
        fields = ["nama", "keterangan"]


class RolePermissionForm(BaseAppModelForm):
    class Meta:
        model = RolePermission
        fields = ["role", "submenu", "can_view", "can_add", "can_edit", "can_delete"]


class UserForm(BaseAppModelForm):
    password1 = forms.CharField(
        label="Password",
        required=False,
        widget=forms.PasswordInput(render_value=False),
    )
    password2 = forms.CharField(
        label="Konfirmasi Password",
        required=False,
        widget=forms.PasswordInput(render_value=False),
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "is_active",
            "is_staff",
            "is_superuser",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.instance.pk:
            self.fields["password1"].required = True
            self.fields["password2"].required = True

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 or password2:
            if password1 != password2:
                raise forms.ValidationError("Password dan konfirmasi password tidak sama.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password1")

        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user
