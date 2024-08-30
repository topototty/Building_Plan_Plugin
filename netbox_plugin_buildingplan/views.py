from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_tables2 import RequestConfig

from netbox.views import generic
from netbox_plugin_buildingplan.filtersets import  BuildingPlanFilter
from netbox_plugin_buildingplan.tables import BuildingPlanTable
from tenancy.models import Tenant
from utilities.views import ViewTab, register_model_view
from netbox_plugin_buildingplan.models import BuildingPlan
from netbox_plugin_buildingplan.forms import BuildingPlanForm, BuildingPlanAddForm, BuildingPlanFilterForm


@register_model_view(Tenant, name="buildingplan_tab")
class BuildingPlanTabView(PermissionRequiredMixin, View):
    permission_required = "netbox_plugin_buildingplan.view_buildingplan"
    tab = ViewTab(
        label="Building Plan",
        permission="tenancy.view_tenant",
    )

    def get(self, request, pk):
        tenant = get_object_or_404(Tenant, pk=pk)
        building_plans = BuildingPlan.objects.filter(tenant=tenant)
        table = BuildingPlanTable(data=building_plans)
        table.configure(request)

        return render(
            request,
            "netbox_plugin_buildingplan/building_plan_tab.html",
            context={
                "object": tenant,
                "table": table,
                "tab": self.tab,
            },
        )

class BuildingPlanCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "netbox_plugin_buildingplan.add_buildingplan"
    model = BuildingPlan
    form_class = BuildingPlanAddForm
    template_name = 'netbox_plugin_buildingplan/building_plan_add.html'

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('plugins:netbox_plugin_buildingplan:buildingplan_list')

class BuildingPlanUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "netbox_plugin_buildingplan.change_buildingplan"
    model = BuildingPlan
    form_class = BuildingPlanForm
    template_name = "netbox_plugin_buildingplan/building_plan_edit.html"

    def get_success_url(self):
        return reverse('plugins:netbox_plugin_buildingplan:buildingplan_list')


class BuildingPlanDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "netbox_plugin_buildingplan.delete_buildingplan"
    model = BuildingPlan
    template_name = "netbox_plugin_buildingplan/building_plan_delete.html"

    def get_success_url(self):
        return reverse('plugins:netbox_plugin_buildingplan:buildingplan_list')


class BuildingPlanListView(PermissionRequiredMixin, generic.ObjectListView):
    permission_required = "netbox_plugin_buildingplan.view_buildingplan"
    model = BuildingPlan
    table = BuildingPlanTable
    template_name = 'netbox_plugin_buildingplan/building_plan_list.html'
    filterset = BuildingPlanFilter
    filterset_form = BuildingPlanFilterForm

    def dispatch(self, request, *args, **kwargs):
        queryset = BuildingPlan.objects.select_related('tenant').all()
        self.queryset = self.filterset(request.GET, queryset).qs
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.filterset_form(self.request.GET)
        return context