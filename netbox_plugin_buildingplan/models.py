from django.db import models
from django.urls import reverse
from netbox.models import NetBoxModel
from tenancy.models import Tenant

class BuildingPlan(NetBoxModel):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="building_plan")
    name = models.CharField(max_length=255, verbose_name="Plan Name")
    image = models.ImageField(upload_to='building_plans/')

    def __str__(self):
        return f"Building Plan for {self.tenant.name}"

    def get_absolute_url(self):
        return reverse('plugins:netbox_plugin_buildingplan:buildingplan_edit', kwargs={'pk': self.pk})
