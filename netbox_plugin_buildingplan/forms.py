from django import forms

from netbox.forms import NetBoxModelFilterSetForm
from .models import BuildingPlan, Tenant

class BuildingPlanForm(forms.ModelForm):
    class Meta:
        model = BuildingPlan
        fields = ['name', 'image']

class BuildingPlanAddForm(forms.ModelForm):
    tenant = forms.ModelChoiceField(queryset=Tenant.objects.all(), label='Tenant')
    name = forms.CharField(label='Plan Name')
    image = forms.ImageField(label='Building Plan Image')

    class Meta:
        model = BuildingPlan
        fields = ['tenant', 'name', 'image']


class BuildingPlanFilterForm(forms.ModelForm):
    tenant = forms.ModelChoiceField(queryset=Tenant.objects.all(), required=False, label="Tenant")
    name = forms.CharField(required=False, label="Plan Name")

    class Meta:
        model = BuildingPlan
        fields = ['tenant', 'name']