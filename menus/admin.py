from django.contrib import admin

from .models import Menu, Role, RolePermission, SubMenu


class SubMenuInline(admin.TabularInline):
    model = SubMenu
    extra = 1


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ("nama", "icon", "urutan", "aktif")
    list_editable = ("urutan", "aktif")
    search_fields = ("nama",)
    inlines = [SubMenuInline]


@admin.register(SubMenu)
class SubMenuAdmin(admin.ModelAdmin):
    list_display = ("nama", "menu", "url", "url_name", "urutan", "aktif")
    list_filter = ("menu", "aktif")
    list_editable = ("urutan", "aktif")
    search_fields = ("nama", "url", "url_name")


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("nama", "keterangan")
    search_fields = ("nama",)


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ("role", "submenu", "can_view", "can_add", "can_edit", "can_delete")
    list_filter = ("role", "submenu__menu", "can_view")
    list_editable = ("can_view", "can_add", "can_edit", "can_delete")
    search_fields = ("role__nama", "submenu__nama")
