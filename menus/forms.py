from config.forms import BaseAppModelForm

from .models import Menu, Role, RolePermission, SubMenu


class MenuForm(BaseAppModelForm):
    class Meta:
        model = Menu
        fields = ["nama", "icon", "urutan", "aktif"]


class SubMenuForm(BaseAppModelForm):
    class Meta:
        model = SubMenu
        fields = ["menu", "nama", "url", "url_name", "icon", "urutan", "aktif"]


class RoleForm(BaseAppModelForm):
    class Meta:
        model = Role
        fields = ["nama", "keterangan"]


class RolePermissionForm(BaseAppModelForm):
    class Meta:
        model = RolePermission
        fields = ["role", "submenu", "can_view", "can_add", "can_edit", "can_delete"]
