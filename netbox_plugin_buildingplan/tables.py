import django_tables2 as tables 
from netbox.tables import NetBoxTable 
from .models import BuildingPlan 
from netbox.tables import columns  

# Определяем класс таблицы для отображения данных BuildingPlan.
class BuildingPlanTable(NetBoxTable):
    # Столбец с названием плана, который открывает изображение плана в модальном окне при клике.
    name = tables.TemplateColumn(
        template_code=(
            '<a href="#" data-bs-toggle="modal" data-bs-target="#imageModal{{ record.id }}">{{ record.name }}</a>'  # Ссылка, открывающая модальное окно.
            '<div class="modal fade" id="imageModal{{ record.id }}" tabindex="-1" aria-labelledby="imageModalLabel{{ record.id }}" aria-hidden="true">'
            '  <div class="modal-dialog modal-lg">'
            '    <div class="modal-content">'
            '      <div class="modal-header">'
            '        <h5 class="modal-title" id="imageModalLabel{{ record.id }}">{{ record.name }}</h5>'  # Заголовок модального окна с названием плана.
            '        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>'  # Кнопка для закрытия модального окна.
            '      </div>'
            '      <div class="modal-body">'
            '        <img src="{{ record.image.url }}" alt="{{ record.name }}" class="img-fluid">'  # Отображение изображения плана.
            '      </div>'
            '      <div class="modal-footer">'
            '        <a href="{{ record.image.url }}" type="button" class="btn btn-secondary">Open</a>'  # Ссылка для открытия изображения в новом окне.
            '      </div>'
            '    </div>'
            '  </div>'
            '</div>'
        ),
        verbose_name='Plan Name'  # Название столбца в заголовке таблицы.
    )

    # Столбец для отображения имени арендатора.
    tenant_name = tables.Column(accessor='tenant.name', verbose_name='Tenant')

    # Столбец для отображения группы арендатора.
    tenant_group = tables.Column(accessor='tenant.group.name', verbose_name='Tenant Group')

    # Столбец для отображения описания арендатора.
    description = tables.Column(accessor='tenant.description', verbose_name='Description')

    # Столбец для действий, таких как редактирование и удаление записей.
    actions = columns.ActionsColumn(
        actions=('edit', 'delete'),  # Определяем доступные действия: редактирование и удаление.
    )

    # Метаданные таблицы.
    class Meta(NetBoxTable.Meta):
        model = BuildingPlan  # Указываем модель, с которой связана таблица.
        fields = ('name', 'tenant_name', 'tenant_group', 'description')  # Определяем, какие поля модели будут отображаться в таблице.
        default_columns = ('name', 'tenant_name', 'tenant_group', 'description')  # Определяем, какие столбцы будут отображаться по умолчанию.
