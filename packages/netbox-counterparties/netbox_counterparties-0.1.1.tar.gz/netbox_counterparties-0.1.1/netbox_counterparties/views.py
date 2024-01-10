from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from utilities.utils import count_related
from netbox.views import generic
from utilities.views import register_model_view, ViewTab
from .models import CounterpartyAssignment, CounterpartyGroup, Counterparty, CounterpartyRole
from . import forms, tables, filtersets


class ObjectCounterpartiesView(generic.ObjectChildrenView):
    child_model = CounterpartyAssignment
    table = tables.CounterpartyAssignmentTable
    filterset = filtersets.CounterpartyAssignmentFilterSet
    template_name = 'tenancy/object_counterparties.html'
    tab = ViewTab(
        label='Контрагенты',
        badge=lambda obj: obj.counterparties.count(),
        permission='netbox_counterparties.view_counterpartyassignment',
        weight=5000
    )

    def get_children(self, request, parent):
        return CounterpartyAssignment.objects.restrict(request.user, 'view').filter(
            content_type=ContentType.objects.get_for_model(parent),
            object_id=parent.pk
        )

    def get_table(self, *args, **kwargs):
        table = super().get_table(*args, **kwargs)

        # Hide object columns
        table.columns.hide('content_type')
        table.columns.hide('object')

        return table


class CounterpartyGroupListView(generic.ObjectListView):
    queryset = CounterpartyGroup.objects.add_related_count(
        CounterpartyGroup.objects.all(),
        Counterparty,
        'group',
        'counterparty_count',
        cumulative=True
    )
    filterset = filtersets.CounterpartyGroupFilterSet
    filterset_form = forms.CounterpartyGroupFilterForm
    table = tables.CounterpartyGroupTable


@register_model_view(CounterpartyGroup)
class CounterpartyGroupView(generic.ObjectView):
    queryset = CounterpartyGroup.objects.all()

    def get_extra_context(self, request, instance):
        groups = instance.get_descendants(include_self=True)
        related_models = (
            (Counterparty.objects.restrict(request.user, 'view').filter(group__in=groups), 'group_id'),
        )

        return {
            'related_models': related_models,
        }


@register_model_view(CounterpartyGroup, 'edit')
class CounterpartyGroupEditView(generic.ObjectEditView):
    queryset = CounterpartyGroup.objects.all()
    form = forms.CounterpartyGroupForm


@register_model_view(CounterpartyGroup, 'delete')
class CounterpartyGroupDeleteView(generic.ObjectDeleteView):
    queryset = CounterpartyGroup.objects.all()


class CounterpartyGroupBulkImportView(generic.BulkImportView):
    queryset = CounterpartyGroup.objects.all()
    model_form = forms.CounterpartyGroupImportForm


class CounterpartyGroupBulkEditView(generic.BulkEditView):
    queryset = CounterpartyGroup.objects.add_related_count(
        CounterpartyGroup.objects.all(),
        Counterparty,
        'group',
        'counterparty_count',
        cumulative=True
    )
    filterset = filtersets.CounterpartyGroupFilterSet
    table = tables.CounterpartyGroupTable
    form = forms.CounterpartyGroupBulkEditForm


class CounterpartyGroupBulkDeleteView(generic.BulkDeleteView):
    queryset = CounterpartyGroup.objects.add_related_count(
        CounterpartyGroup.objects.all(),
        Counterparty,
        'group',
        'counterparty_count',
        cumulative=True
    )
    filterset = filtersets.CounterpartyGroupFilterSet
    table = tables.CounterpartyGroupTable


#
# Counterparty roles
#

class CounterpartyRoleListView(generic.ObjectListView):
    queryset = CounterpartyRole.objects.all()
    filterset = filtersets.CounterpartyRoleFilterSet
    filterset_form = forms.CounterpartyRoleFilterForm
    table = tables.CounterpartyRoleTable


@register_model_view(CounterpartyRole)
class CounterpartyRoleView(generic.ObjectView):
    queryset = CounterpartyRole.objects.all()

    def get_extra_context(self, request, instance):
        related_models = (
            (CounterpartyAssignment.objects.restrict(request.user, 'view').filter(role=instance), 'role_id'),
        )

        return {
            'related_models': related_models,
        }


@register_model_view(CounterpartyRole, 'edit')
class CounterpartyRoleEditView(generic.ObjectEditView):
    queryset = CounterpartyRole.objects.all()
    form = forms.CounterpartyRoleForm


@register_model_view(CounterpartyRole, 'delete')
class CounterpartyRoleDeleteView(generic.ObjectDeleteView):
    queryset = CounterpartyRole.objects.all()


class CounterpartyRoleBulkImportView(generic.BulkImportView):
    queryset = CounterpartyRole.objects.all()
    model_form = forms.CounterpartyRoleImportForm


class CounterpartyRoleBulkEditView(generic.BulkEditView):
    queryset = CounterpartyRole.objects.all()
    filterset = filtersets.CounterpartyRoleFilterSet
    table = tables.CounterpartyRoleTable
    form = forms.CounterpartyRoleBulkEditForm


class CounterpartyRoleBulkDeleteView(generic.BulkDeleteView):
    queryset = CounterpartyRole.objects.all()
    filterset = filtersets.CounterpartyRoleFilterSet
    table = tables.CounterpartyRoleTable


#
# Counterparties
#

class CounterpartyListView(generic.ObjectListView):
    queryset = Counterparty.objects.annotate(
        assignment_count=count_related(CounterpartyAssignment, 'counterparty')
    )
    filterset = filtersets.CounterpartyFilterSet
    filterset_form = forms.CounterpartyFilterForm
    table = tables.CounterpartyTable


@register_model_view(Counterparty)
class CounterpartyView(generic.ObjectView):
    queryset = Counterparty.objects.all()


@register_model_view(Counterparty, 'edit')
class CounterpartyEditView(generic.ObjectEditView):
    queryset = Counterparty.objects.all()
    form = forms.CounterpartyForm


@register_model_view(Counterparty, 'delete')
class CounterpartyDeleteView(generic.ObjectDeleteView):
    queryset = Counterparty.objects.all()


class CounterpartyBulkImportView(generic.BulkImportView):
    queryset = Counterparty.objects.all()
    model_form = forms.CounterpartyImportForm


class CounterpartyBulkEditView(generic.BulkEditView):
    queryset = Counterparty.objects.annotate(
        assignment_count=count_related(CounterpartyAssignment, 'counterparty')
    )
    filterset = filtersets.CounterpartyFilterSet
    table = tables.CounterpartyTable
    form = forms.CounterpartyBulkEditForm


class CounterpartyBulkDeleteView(generic.BulkDeleteView):
    queryset = Counterparty.objects.annotate(
        assignment_count=count_related(CounterpartyAssignment, 'counterparty')
    )
    filterset = filtersets.CounterpartyFilterSet
    table = tables.CounterpartyTable

#
# Counterparty assignments
#


class CounterpartyAssignmentListView(generic.ObjectListView):
    queryset = CounterpartyAssignment.objects.all()
    filterset = filtersets.CounterpartyAssignmentFilterSet
    filterset_form = forms.CounterpartyAssignmentFilterForm
    table = tables.CounterpartyAssignmentTable
    actions = ('export', 'bulk_edit', 'bulk_delete')


@register_model_view(CounterpartyAssignment, 'edit')
class CounterpartyAssignmentEditView(generic.ObjectEditView):
    queryset = CounterpartyAssignment.objects.all()
    form = forms.CounterpartyAssignmentForm
    template_name = 'netbox_counterparties/counterpartyassignment_edit.html'

    def alter_object(self, instance, request, args, kwargs):
        if not instance.pk:
            # Assign the object based on URL kwargs
            content_type = get_object_or_404(ContentType, pk=request.GET.get('content_type'))
            instance.object = get_object_or_404(content_type.model_class(), pk=request.GET.get('object_id'))
        return instance

    def get_extra_addanother_params(self, request):
        return {
            'content_type': request.GET.get('content_type'),
            'object_id': request.GET.get('object_id'),
        }


class CounterpartyAssignmentBulkEditView(generic.BulkEditView):
    queryset = CounterpartyAssignment.objects.all()
    filterset = filtersets.CounterpartyAssignmentFilterSet
    table = tables.CounterpartyAssignmentTable
    form = forms.CounterpartyAssignmentBulkEditForm


class CounterpartyAssignmentBulkImportView(generic.BulkImportView):
    queryset = CounterpartyAssignment.objects.all()
    model_form = forms.CounterpartyAssignmentImportForm


class CounterpartyAssignmentBulkDeleteView(generic.BulkDeleteView):
    queryset = CounterpartyAssignment.objects.all()
    filterset = filtersets.CounterpartyAssignmentFilterSet
    table = tables.CounterpartyAssignmentTable


@register_model_view(CounterpartyAssignment, 'delete')
class CounterpartyAssignmentDeleteView(generic.ObjectDeleteView):
    queryset = CounterpartyAssignment.objects.all()

