from django.urls import path

from .views import OPDListView, OPDCreateView, OPDUpdateView, OPDDeleteView, SubOPDListView, SubOPDCreateView, SubOPDUpdateView, SubOPDDeleteView

urlpatterns = [
    path("opd/", OPDListView.as_view(), name="opd_list"),
    path("opd/add/", OPDCreateView.as_view(), name="opd_add"),
    path("opd/<int:pk>/form/", OPDUpdateView.as_view(), name="opd_update"),
    path("opd/<int:pk>/delete/", OPDDeleteView.as_view(), name="opd_delete"),

    path("sub-opd/", SubOPDListView.as_view(), name="subopd_list"),
    path("sub-opd/add/", SubOPDCreateView.as_view(), name="subopd_add"),
    path("sub-opd/<int:pk>/form/", SubOPDUpdateView.as_view(), name="subopd_update"),
    path("sub-opd/<int:pk>/delete/", SubOPDDeleteView.as_view(), name="subopd_delete"),
]
