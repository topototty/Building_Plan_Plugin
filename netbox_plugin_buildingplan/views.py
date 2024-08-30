from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_tables2 import RequestConfig

from netbox.views import generic
from netbox_plugin_buildingplan.filtersets import BuildingPlanFilter
from netbox_plugin_buildingplan.tables import BuildingPlanTable
from tenancy.models import Tenant
from utilities.views import ViewTab, register_model_view
from netbox_plugin_buildingplan.models import BuildingPlan
from netbox_plugin_buildingplan.forms import (
    BuildingPlanForm,
    BuildingPlanAddForm,
    BuildingPlanFilterForm,
)

# Регистрация представления в виде вкладки для модели Tenant
@register_model_view(Tenant, name="buildingplan_tab")
class BuildingPlanTabView(PermissionRequiredMixin, View):
    """
    Представление для отображения вкладки 'Building Plan' в деталях арендатора (Tenant).
    """

    # Требуемое разрешение для доступа к этому представлению
    permission_required = "netbox_plugin_buildingplan.view_buildingplan"

    # Настройки вкладки
    tab = ViewTab(
        label="Building Plan",  # Метка вкладки, отображаемая в интерфейсе
        permission="tenancy.view_tenant",  # Разрешение, необходимое для отображения вкладки
    )

    def get(self, request, pk):
        """
        Обрабатывает GET-запрос для отображения списка планов здания, связанных с определенным арендатором.
        """
        # Получаем объект Tenant по первичному ключу или возвращаем 404, если не найден
        tenant = get_object_or_404(Tenant, pk=pk)

        # Получаем все планы здания, связанные с данным арендатором
        building_plans = BuildingPlan.objects.filter(tenant=tenant)

        # Инициализируем таблицу с данными планов здания
        table = BuildingPlanTable(data=building_plans)
        table.configure(request)  # Настраиваем таблицу с учетом запроса

        # Рендерим шаблон с переданным контекстом
        return render(
            request,
            "netbox_plugin_buildingplan/building_plan_tab.html",
            context={
                "object": tenant,  # Объект арендатора
                "table": table,    # Таблица с планами здания
                "tab": self.tab,   # Информация о вкладке
            },
        )


class BuildingPlanCreateView(PermissionRequiredMixin, CreateView):
    """
    Представление для создания нового плана здания.
    """

    # Требуемое разрешение для создания плана здания
    permission_required = "netbox_plugin_buildingplan.add_buildingplan"

    # Модель, с которой работаем
    model = BuildingPlan

    # Форма, используемая для создания плана здания
    form_class = BuildingPlanAddForm

    # Шаблон, используемый для отображения формы создания
    template_name = 'netbox_plugin_buildingplan/building_plan_add.html'

    def form_valid(self, form):
        """
        Вызывается, когда отправленная форма валидна.
        Здесь можно добавить дополнительную обработку перед сохранением.
        """
        return super().form_valid(form)  # Сохраняем форму и перенаправляем пользователя

    def get_success_url(self):
        """
        Определяет URL для перенаправления после успешного создания плана здания.
        """
        return reverse('plugins:netbox_plugin_buildingplan:buildingplan_list')  # Перенаправляем на список планов


class BuildingPlanUpdateView(PermissionRequiredMixin, UpdateView):
    """
    Представление для обновления существующего плана здания.
    """

    # Требуемое разрешение для изменения плана здания
    permission_required = "netbox_plugin_buildingplan.change_buildingplan"

    # Модель, с которой работаем
    model = BuildingPlan

    # Форма, используемая для обновления плана здания
    form_class = BuildingPlanForm

    # Шаблон, используемый для отображения формы редактирования
    template_name = "netbox_plugin_buildingplan/building_plan_edit.html"

    def get_success_url(self):
        """
        Определяет URL для перенаправления после успешного обновления плана здания.
        """
        return reverse('plugins:netbox_plugin_buildingplan:buildingplan_list')  # Перенаправляем на список планов


class BuildingPlanDeleteView(PermissionRequiredMixin, DeleteView):
    """
    Представление для удаления существующего плана здания.
    """

    # Требуемое разрешение для удаления плана здания
    permission_required = "netbox_plugin_buildingplan.delete_buildingplan"

    # Модель, с которой работаем
    model = BuildingPlan

    # Шаблон, используемый для подтверждения удаления
    template_name = "netbox_plugin_buildingplan/building_plan_delete.html"

    def get_success_url(self):
        """
        Определяет URL для перенаправления после успешного удаления плана здания.
        """
        return reverse('plugins:netbox_plugin_buildingplan:buildingplan_list')  # Перенаправляем на список планов


class BuildingPlanListView(PermissionRequiredMixin, generic.ObjectListView):
    """
    Представление для отображения списка всех планов здания с возможностью фильтрации.
    """

    # Требуемое разрешение для просмотра списка планов здания
    permission_required = "netbox_plugin_buildingplan.view_buildingplan"

    # Модель, с которой работаем
    model = BuildingPlan

    # Класс таблицы, используемый для отображения данных
    table = BuildingPlanTable

    # Шаблон, используемый для отображения списка
    template_name = 'netbox_plugin_buildingplan/building_plan_list.html'

    # Класс фильтра, используемый для фильтрации данных
    filterset = BuildingPlanFilter

    # Форма фильтрации, отображаемая пользователю
    filterset_form = BuildingPlanFilterForm

    def dispatch(self, request, *args, **kwargs):
        """
        Обрабатывает входящий запрос, применяет фильтрацию и передает управление родительскому методу.
        """
        # Получаем базовый queryset с предвыборкой связанных объектов Tenant для оптимизации запросов
        queryset = BuildingPlan.objects.select_related('tenant').all()

        # Применяем фильтрацию на основе GET-параметров запроса
        self.queryset = self.filterset(request.GET, queryset).qs

        # Продолжаем обработку запроса
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Формирует контекстные данные для передачи в шаблон.
        """
        # Получаем базовые контекстные данные от родительского класса
        context = super().get_context_data(**kwargs)

        # Добавляем в контекст форму фильтрации, заполненную текущими GET-параметрами
        context['filter_form'] = self.filterset_form(self.request.GET)

        return context  # Возвращаем полный контекст для рендеринга шаблона
