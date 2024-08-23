from django.urls import path
from .views import *


urlpatterns = [
    path("helloworldpage/", HelloWorldView.as_view(), name="hello_world"),
    path('buildingplan_page/', BuildingPlanListView.as_view(), name='building_plan_list'),
    path('tenants/<int:pk>/building-plan/', BuildingPlanTabView.as_view(), name='building-plan-tab'),
    path('tenants/<int:pk>/building-plan/add/', BuildingPlanCreateView.as_view(), name='add_building_plan'),
    path('tenants/<int:pk>/building-plan/edit/', BuildingPlanUpdateView.as_view(), name='edit_building_plan'),
    path('tenants/<int:pk>/building-plan/delete/', BuildingPlanDeleteView.as_view(), name='delete_building_plan'),
]
