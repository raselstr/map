from django.shortcuts import render

from config.crud.base import BaseCRUDView

from .forms import OPDForm, SubOPDForm
from .models import OPD, SubOPD
from .tables import OPDTable, SubOPDTable


class OPDListView(BaseCRUDView):
    model = OPD
    form_class = OPDForm
    table_class = OPDTable
    template_name = "opd/list.html"
    template_list = "opd/list.html"
    template_form = "opd/form.html"
    title = "OPD"
    url_list = "/opd/"
    url_action = "/opd/"
    url_action_pk = "/opd/"

    def get_permission(self):
        return type("Perm", (), {"can_view": True, "can_add": True, "can_edit": True, "can_delete": True})()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("search", "")
        return context


class OPDCreateView(OPDListView):
    pass


class OPDUpdateView(OPDListView):
    pass


class OPDDeleteView(OPDListView):
    def delete_view(self, request, pk):
        perm = self.get_permission()
        if not perm or not perm.can_delete:
            return self._forbidden(request)

        obj = self.get_object_queryset().get(pk=pk)
        if request.method == "POST":
            obj.delete()
            return redirect(self.get_success_redirect_url())

        return render(request, "opd/delete.html", {"object": obj, "url_list": self.url_list, "title": "Hapus Data"})


class SubOPDListView(BaseCRUDView):
    model = SubOPD
    form_class = SubOPDForm
    table_class = SubOPDTable
    template_name = "opd/list.html"
    template_list = "opd/list.html"
    template_form = "opd/form.html"
    title = "Sub OPD"
    url_list = "/sub-opd/"
    url_action = "/sub-opd/"
    url_action_pk = "/sub-opd/"

    def get_permission(self):
        return type("Perm", (), {"can_view": True, "can_add": True, "can_edit": True, "can_delete": True})()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("search", "")
        return context


class SubOPDCreateView(SubOPDListView):
    pass


class SubOPDUpdateView(SubOPDListView):
    pass


class SubOPDDeleteView(SubOPDListView):
    def delete_view(self, request, pk):
        perm = self.get_permission()
        if not perm or not perm.can_delete:
            return self._forbidden(request)

        obj = self.get_object_queryset().get(pk=pk)
        if request.method == "POST":
            obj.delete()
            return redirect(self.get_success_redirect_url())

        return render(request, "opd/delete.html", {"object": obj, "url_list": self.url_list, "title": "Hapus Data"})
