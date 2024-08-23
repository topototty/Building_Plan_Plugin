from django import forms
from .models import BuildingPlan

class BuildingPlanForm(forms.ModelForm):
    class Meta:
        model = BuildingPlan
        fields = ['image']
