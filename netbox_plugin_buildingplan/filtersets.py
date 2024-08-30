import django_filters
from tenancy.models import Tenant
from netbox_plugin_buildingplan.models import BuildingPlan

class BuildingPlanFilter(django_filters.FilterSet):
    tenant = django_filters.ModelChoiceFilter(
        queryset=Tenant.objects.all(),
        to_field_name="id",  # Используем "id" для фильтрации по идентификатору
        label="Tenant",
    )

    name = django_filters.CharFilter(
        lookup_expr="icontains",
        label="Plan Name",
    )

    class Meta:
        model = BuildingPlan
        fields = ['tenant', 'name']
