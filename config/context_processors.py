from menus.models import RolePermission, Menu


SPJ_ACTIVE_SUBMENU_MAP = {
    "penginapan_action": "penginapan_list",
    "penginapan_action_pk": "penginapan_list",
    "penginapan_delete": "penginapan_list",
    "pesawat_action": "pesawat_list",
    "pesawat_action_pk": "pesawat_list",
    "pesawat_delete": "pesawat_list",
    "uang_harian_action": "uang_harian_list",
    "uang_harian_action_pk": "uang_harian_list",
    "uang_harian_delete": "uang_harian_list",
    "transport_action": "transport_list",
    "transport_action_pk": "transport_list",
    "transport_delete": "transport_list",
    "uang_representasi_action": "uang_representasi_list",
    "uang_representasi_action_pk": "uang_representasi_list",
    "uang_representasi_delete": "uang_representasi_list",
    "laporan_perjalanan_action": "laporan_perjalanan_list",
    "laporan_perjalanan_action_pk": "laporan_perjalanan_list",
    "laporan_perjalanan_delete": "laporan_perjalanan_list",
    "laporan_perjalanan_preview": "laporan_perjalanan_list",
    "laporan_perjalanan_print": "laporan_perjalanan_list",
    "kwitansi_print": "kwitansi_list",
}


def _active_submenu_name(request):
    resolver_match = getattr(request, "resolver_match", None)
    url_name = getattr(resolver_match, "url_name", "") or ""
    for suffix in ("_add", "_update", "_delete"):
        if url_name.endswith(suffix):
            return f"{url_name[:-len(suffix)]}_list"
    return SPJ_ACTIVE_SUBMENU_MAP.get(url_name, url_name)

def menu_context(request):
    # Jika belum login → tidak tampilkan menu
    if not request.user.is_authenticated:
        return {}

    user = request.user

    # ==============================
    # SUPERUSER (LIHAT SEMUA MENU)
    # ==============================
    if user.is_superuser:
        menus = Menu.objects.filter(aktif=True).prefetch_related('submenus').all()

        menu_data = []
        for menu in menus:
            submenus = menu.submenus.filter(aktif=True)
            if not submenus.exists():
                continue

            menu_data.append({
                'menu': menu,
                'submenus': submenus
            })

        return {
            'menu_data': menu_data,
            'active_submenu': _active_submenu_name(request),
        }

    # ==============================
    # USER BIASA (BERDASARKAN ROLE)
    # ==============================
    try:
        role = user.userprofile.role
    except Exception:
        return {}

    # Ambil permission sesuai role
    permissions = RolePermission.objects.filter(
        role=role,
        can_view=True,
        submenu__aktif=True,
        submenu__menu__aktif=True,
    ).select_related('submenu__menu').order_by(
        'submenu__menu__urutan',
        'submenu__urutan'
    )

    menu_dict = {}

    for perm in permissions:
        menu = perm.submenu.menu

        # Jika menu belum ada → buat
        if menu.id not in menu_dict:
            menu_dict[menu.id] = {
                'menu': menu,
                'submenus': []
            }

        menu_dict[menu.id]['submenus'].append(perm.submenu)

    # Convert ke list
    menu_data = list(menu_dict.values())

    return {
        'menu_data': menu_data,
        'active_submenu': _active_submenu_name(request),
    }
