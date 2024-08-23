from django.db import models
from tenancy.models import Tenant

class BuildingPlan(models.Model):
    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE, related_name="building_plan")
    image = models.ImageField(upload_to='building_plans/')

    def __str__(self):
        return f"Building Plan for {self.tenant.name}"
