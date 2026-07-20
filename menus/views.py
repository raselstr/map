from types import SimpleNamespace

from config.crud.base import BaseCRUDView

from .forms import MenuForm, RoleForm, RolePermissionForm, SubMenuForm
from .models import Menu, Role, RolePermission, SubMenu
from .tables import MenuTable, RolePermissionTable, RoleTable, SubMenuTable


class FullAccessCRUDView(BaseCRUDView):
    def get_permission(self):
        return SimpleNamespace(can_view=True, can_add=True, can_edit=True, can_delete=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form(self.request)
        context["search_query"] = self.request.GET.get("search", "")
        return context


class MenuListView(FullAccessCRUDView):
    model = Menu
    form_class = MenuForm
    table_class = MenuTable
    title = "Menu"
    url_list = "/menu/"
    url_action = "/menu/"
    url_action_pk = "/menu/"


class SubMenuListView(FullAccessCRUDView):
    model = SubMenu
    form_class = SubMenuForm
    table_class = SubMenuTable
    title = "Sub Menu"
    url_list = "/sub-menu/"
    url_action = "/sub-menu/"
    url_action_pk = "/sub-menu/"


class RoleListView(FullAccessCRUDView):
    model = Role
    form_class = RoleForm
    table_class = RoleTable
    title = "Role"
    url_list = "/role/"
    url_action = "/role/"
    url_action_pk = "/role/"


class RolePermissionListView(FullAccessCRUDView):
    model = RolePermission
    form_class = RolePermissionForm
    table_class = RolePermissionTable
    title = "Hak Akses Menu"
    url_list = "/hak-akses-menu/"
    url_action = "/hak-akses-menu/"
    url_action_pk = "/hak-akses-menu/"
