import django_tables2 as tables

from config.tables import BaseTable
from .models import OPD, SubOPD


class OPDTable(BaseTable):
    aksi = tables.TemplateColumn(
        template_name="opd/actions.html",
        extra_context={"update_url_name": "opd_update", "delete_url_name": "opd_delete"},
        orderable=False,
        verbose_name="Aksi",
    )

    class Meta(BaseTable.Meta):
        model = OPD
        fields = ("kode", "nama", "aksi")
        order_by = ("kode",)


class SubOPDTable(BaseTable):
    aksi = tables.TemplateColumn(
        template_name="opd/actions.html",
        extra_context={"update_url_name": "subopd_update", "delete_url_name": "subopd_delete"},
        orderable=False,
        verbose_name="Aksi",
    )

    class Meta(BaseTable.Meta):
        model = SubOPD
        fields = ("kode", "nama", "opd", "aksi")
        order_by = ("kode",)
