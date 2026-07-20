from config.tables import BaseTable, action_column

from .models import Menu, Role, RolePermission, SubMenu


class MenuTable(BaseTable):
    aksi = action_column("menu_update", "menu_delete")

    class Meta(BaseTable.Meta):
        model = Menu
        fields = ("no", "nama", "icon", "urutan", "aktif", "aksi")
        order_by = ("urutan", "nama")


class SubMenuTable(BaseTable):
    aksi = action_column("submenu_update", "submenu_delete")

    class Meta(BaseTable.Meta):
        model = SubMenu
        fields = ("no", "menu", "nama", "url_name", "icon", "urutan", "aktif", "aksi")
        order_by = ("menu__urutan", "urutan", "nama")


class RoleTable(BaseTable):
    aksi = action_column("role_update", "role_delete")

    class Meta(BaseTable.Meta):
        model = Role
        fields = ("no", "nama", "keterangan", "aksi")
        order_by = ("nama",)


class RolePermissionTable(BaseTable):
    aksi = action_column("rolepermission_update", "rolepermission_delete")

    class Meta(BaseTable.Meta):
        model = RolePermission
        fields = ("no", "role", "submenu", "can_view", "can_add", "can_edit", "can_delete", "aksi")
        order_by = ("role__nama", "submenu__menu__urutan", "submenu__urutan")
