from django.urls import path
from .views import *

urlpatterns = [
    path('tenants/<int:pk>/building-plan/', BuildingPlanTabView.as_view(), name='buildingplan_tab'),

    path('building-plan_page/', BuildingPlanListView.as_view(), name='buildingplan_list'),
    path('building-plan/add/', BuildingPlanCreateView.as_view(), name='buildingplan_add'),
    path('building-plan/<int:pk>/edit/', BuildingPlanUpdateView.as_view(), name='buildingplan_edit'),
    path('building-plan/<int:pk>/delete/', BuildingPlanDeleteView.as_view(), name='buildingplan_delete'),
]
