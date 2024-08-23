import random

from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from tenancy.models import Tenant
from utilities.views import ViewTab, register_model_view
from netbox_plugin_buildingplan.models import BuildingPlan
from netbox_plugin_buildingplan.forms import BuildingPlanForm

class HelloWorldView(PermissionRequiredMixin, View):
    """
    Display the "Hello, World!" page
    """
    # This allows only users having View access to prefixes.
    # If you don't need this kind of control, just remove this and
    # the PermissionRequiredMixin from the class.
    permission_required = "ipam.view_prefix"

    def get(self, request):
        # This is our code that gets run every time the page is visited
        number = random.randint(0, 999999)
        # Let's also see the query parameters
        query_params = str(dict(request.GET))
        # Now let's render the page output, using our variables
        return render(
            request,
            "netbox_plugin_buildingplan/helloworld.html",
            {
                "number": number,
                "query_params": query_params,
            },
        )

@register_model_view(Tenant, name="building-plan-tab")
class BuildingPlanTabView(PermissionRequiredMixin, View):
    permission_required = "tenancy.view_tenant"
    tab = ViewTab(
        label="Building Plan",
        permission="tenancy.view_tenant",
    )

    def get(self, request, pk):
        tenant = get_object_or_404(Tenant, pk=pk)
        building_plan = BuildingPlan.objects.filter(tenant=tenant).first()
        form = BuildingPlanForm(instance=building_plan)

        return render(
            request,
            "netbox_plugin_buildingplan/building_plan_tab.html",
            context={
                "object": tenant,
                "building_plan": building_plan,
                "form": form,
                "tab": self.tab,
            },
        )


class BuildingPlanCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "tenancy.add_tenant"
    model = BuildingPlan
    form_class = BuildingPlanForm

    def form_valid(self, form):
        form.instance.tenant = get_object_or_404(Tenant, pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('plugins:netbox_plugin_buildingplan:building-plan-tab', kwargs={'pk': self.kwargs['pk']})


class BuildingPlanUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "tenancy.change_tenant"
    model = BuildingPlan
    form_class = BuildingPlanForm

    def get_object(self):
        tenant_id = self.kwargs.get('pk')
        return get_object_or_404(BuildingPlan, tenant_id=tenant_id)

    def get_success_url(self):
        return reverse('plugins:netbox_plugin_buildingplan:building-plan-tab', kwargs={'pk': self.kwargs['pk']})


class BuildingPlanDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "tenancy.delete_tenant"
    model = BuildingPlan

    def get_object(self):
        tenant_id = self.kwargs.get('pk')
        return get_object_or_404(BuildingPlan, tenant_id=tenant_id)

    def get_success_url(self):
        return reverse('plugins:netbox_plugin_buildingplan:building-plan-tab', kwargs={'pk': self.kwargs['pk']})


class BuildingPlanListView(PermissionRequiredMixin, View):
    permission_required = "tenancy.view_tenant"

    def get(self, request):
        building_plans = BuildingPlan.objects.all()
        return render(
            request,
            "netbox_plugin_buildingplan/building_plan_list.html",
            context={
                "building_plans": building_plans,
            },
        )
