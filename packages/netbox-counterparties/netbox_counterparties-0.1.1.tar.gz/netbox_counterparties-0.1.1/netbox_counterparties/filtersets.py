import django_filters
from django.db.models import Q
from django.utils.translation import gettext as _

from extras.filters import TagFilter
from netbox.filtersets import ChangeLoggedModelFilterSet, OrganizationalModelFilterSet, NetBoxModelFilterSet
from utilities.filters import ContentTypeFilter, TreeNodeMultipleChoiceFilter
from .models import *


__all__ = (
    'CounterpartyAssignmentFilterSet',
    'CounterpartyFilterSet',
    'CounterpartyGroupFilterSet',
    'CounterpartyModelFilterSet',
    'CounterpartyRoleFilterSet',
)


#
# Counterpartys
#

class CounterpartyGroupFilterSet(OrganizationalModelFilterSet):
    parent_id = django_filters.ModelMultipleChoiceFilter(
        queryset=CounterpartyGroup.objects.all(),
        label=_('Группа контрагентов (ID)'),
    )
    parent = django_filters.ModelMultipleChoiceFilter(
        field_name='parent__slug',
        queryset=CounterpartyGroup.objects.all(),
        to_field_name='slug',
        label=_('Группа контрагентов (slug)'),
    )

    class Meta:
        model = CounterpartyGroup
        fields = ['id', 'name', 'slug', 'description']


class CounterpartyRoleFilterSet(OrganizationalModelFilterSet):

    class Meta:
        model = CounterpartyRole
        fields = ['id', 'name', 'slug', 'description']


class CounterpartyFilterSet(NetBoxModelFilterSet):
    group_id = TreeNodeMultipleChoiceFilter(
        queryset=CounterpartyGroup.objects.all(),
        field_name='group',
        lookup_expr='in',
        label=_('Группа контрагентов (ID)'),
    )
    group = TreeNodeMultipleChoiceFilter(
        queryset=CounterpartyGroup.objects.all(),
        field_name='group',
        lookup_expr='in',
        to_field_name='slug',
        label=_('Группа контрагентов (slug)'),
    )

    class Meta:
        model = Counterparty
        fields = ['id', 'name', 'phone', 'email', 'address', 'link']

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(phone__icontains=value) |
            Q(email__icontains=value) |
            Q(address__icontains=value) |
            Q(link__icontains=value) |
            Q(comments__icontains=value)
        )


class CounterpartyAssignmentFilterSet(ChangeLoggedModelFilterSet):
    q = django_filters.CharFilter(
        method='search',
        label=_('Поиск'),
    )
    content_type = ContentTypeFilter()
    counterparty_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Counterparty.objects.all(),
        label=_('Контрагент (ID)'),
    )
    role_id = django_filters.ModelMultipleChoiceFilter(
        queryset=CounterpartyRole.objects.all(),
        label=_('Контрагент роль (ID)'),
    )
    role = django_filters.ModelMultipleChoiceFilter(
        field_name='role__slug',
        queryset=CounterpartyRole.objects.all(),
        to_field_name='slug',
        label=_('Контрагент роль (slug)'),
    )
    tag = TagFilter()

    class Meta:
        model = CounterpartyAssignment
        fields = ['id', 'content_type_id', 'object_id', 'priority', 'tag']

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(сounterparty__name__icontains=value) |
            Q(role__name__icontains=value)
        )


class CounterpartyModelFilterSet(django_filters.FilterSet):
    contact = django_filters.ModelMultipleChoiceFilter(
        field_name='counterparties__contact',
        queryset=Counterparty.objects.all(),
        label=_('Counterparty'),
    )
    contact_role = django_filters.ModelMultipleChoiceFilter(
        field_name='counterparties__role',
        queryset=CounterpartyRole.objects.all(),
        label=_('Counterparty Role')
    )
    contact_group = TreeNodeMultipleChoiceFilter(
        queryset=CounterpartyGroup.objects.all(),
        field_name='counterparties__counterparty__group',
        lookup_expr='in',
        label=_('Counterparty group'),
    )


