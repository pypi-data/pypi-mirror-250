import django_tables2 as tables
from django.utils.translation import gettext_lazy as _
from django_tables2.utils import Accessor
from netbox.tables import NetBoxTable, columns
from utilities.tables import linkify_phone
from .models import CounterpartyAssignment, CounterpartyRole, Counterparty, CounterpartyGroup


__all__ = (
    'CounterpartyAssignmentTable',
    'CounterpartyGroupTable',
    'CounterpartyRoleTable',
    'CounterpartyTable',
    'CounterpartyColumnMixin',
)


class CounterpartyGroupTable(NetBoxTable):
    name = columns.MPTTColumn(
        verbose_name=_('Название группы'),
        linkify=True
    )
    counterparty_count = columns.LinkedCountColumn(
        viewname='plugins:netbox_counterparties:counterparty_list',
        url_params={'group_id': 'pk'},
        verbose_name='Контрагенты'
    )
    tags = columns.TagColumn(
        url_name='plugins:netbox_counterparties:сounterpartygroup_list'
    )

    class Meta(NetBoxTable.Meta):
        model = CounterpartyGroup
        fields = (
            'pk', 'name', 'counterparty_count', 'description', 'slug', 'tags', 'created', 'last_updated', 'actions',
        )
        default_columns = ('pk', 'name', 'counterparty_count', 'description')


class CounterpartyRoleTable(NetBoxTable):
    name = tables.Column(
        verbose_name=_('Название роли'),
        linkify=True
    )
    tags = columns.TagColumn(
        url_name='plugins:netbox_counterparties:counterpartyrole_list'
    )

    class Meta(NetBoxTable.Meta):
        model = CounterpartyRole
        fields = ('pk', 'name', 'description', 'slug', 'tags', 'created', 'last_updated', 'actions')
        default_columns = ('pk', 'name', 'description')


class CounterpartyTable(NetBoxTable):
    name = tables.Column(
        verbose_name=_('ФИО'),
        linkify=True
    )
    group = tables.Column(
        verbose_name=_('Группа'),
        linkify=True
    )
    phone = tables.Column(
        verbose_name=_('Телефон'),
        linkify=linkify_phone,
    )
    comments = columns.MarkdownColumn(
        verbose_name=_('Комментарий'),
    )
    assignment_count = columns.LinkedCountColumn(
        viewname='plugins:netbox_counterparties:counterpartyassignment_list',
        url_params={'counterparty_id': 'pk'},
        verbose_name=_('Связь')
    )
    tags = columns.TagColumn(
        url_name='plugins:netbox_counterparties:counterparty_list'
    )

    class Meta(NetBoxTable.Meta):
        model = Counterparty
        fields = (
            'pk', 'name', 'group', 'tenant', 'phone', 'email', 'address', 'link', 'description', 'comments',
            'assignment_count', 'tags', 'created', 'last_updated',
        )
        default_columns = ('pk', 'name', 'group', 'assignment_count', 'tenant', 'phone', 'email')


class CounterpartyAssignmentTable(NetBoxTable):
    content_type = columns.ContentTypeColumn(
        verbose_name=_('Тип объекта')
    )
    object = tables.Column(
        verbose_name=_('Объект'),
        linkify=True,
        orderable=False
    )
    counterparty = tables.Column(
        verbose_name=_('Контрагент'),
        linkify=True
    )
    role = tables.Column(
        verbose_name=_('Роль'),
        linkify=True
    )
    counterparty_phone = tables.Column(
        accessor=Accessor('counterparty__phone'),
        verbose_name=_('Телефон')
    )
    counterparty_email = tables.Column(
        accessor=Accessor('counterparty__email'),
        verbose_name=_('counterparty Email')
    )
    counterparty_address = tables.Column(
        accessor=Accessor('counterparty__address'),
        verbose_name=_('Адрес')
    )
    counterparty_link = tables.Column(
        accessor=Accessor('counterparty__link'),
        verbose_name=_('Ссылка')
    )
    counterparty_description = tables.Column(
        accessor=Accessor('counterparty__description'),
        verbose_name=_('Описание')
    )
    tags = columns.TagColumn(
        url_name='plugins:netbox_counterparties:counterpartyassignment_list'
    )
    actions = columns.ActionsColumn(
        actions=('edit', 'delete')
    )

    class Meta(NetBoxTable.Meta):
        model = CounterpartyAssignment
        fields = (
            'pk', 'content_type', 'object', 'counterparty', 'role', 'priority', 'counterparty_phone',
            'counterparty_email', 'counterparty_address', 'counterparty_link', 'counterparty_description', 'tags',
            'actions'
        )
        default_columns = (
            'pk', 'content_type', 'object', 'counterparty', 'role', 'priority', 'counterparty_email',
            'counterparty_phone'
        )


class CounterpartyColumnMixin(tables.Table):
    counterparties = columns.ManyToManyColumn(
        verbose_name='Контрагенты',
        linkify_item=True,
        transform=lambda obj: obj.contact.name
    )
