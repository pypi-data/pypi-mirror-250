from rest_framework.routers import APIRootView
from netbox.api.viewsets import NetBoxModelViewSet, MPTTLockedMixin

from .. import models, filtersets
from . import serializers


class CounterpartiesRootView(APIRootView):
    """
    Counterparties API root view
    """
    def get_view_name(self):
        return 'Counterparties'


class CounterpartyGroupViewSet(MPTTLockedMixin, NetBoxModelViewSet):
    queryset = models.CounterpartyGroup.objects.add_related_count(
        models.CounterpartyGroup.objects.all(),
        models.Counterparty,
        'group',
        'counterparty_count',
        cumulative=True
    ).prefetch_related('tags')
    serializer_class = serializers.CounterpartyGroupSerializer
    filterset_class = filtersets.CounterpartyGroupFilterSet


class CounterpartyRoleViewSet(NetBoxModelViewSet):
    queryset = models.CounterpartyRole.objects.prefetch_related('tags')
    serializer_class = serializers.CounterpartyRoleSerializer
    filterset_class = filtersets.CounterpartyRoleFilterSet


class CounterpartyViewSet(NetBoxModelViewSet):
    queryset = models.Counterparty.objects.prefetch_related('group', 'tags')
    serializer_class = serializers.CounterpartySerializer
    filterset_class = filtersets.CounterpartyFilterSet


class CounterpartyAssignmentViewSet(NetBoxModelViewSet):
    queryset = models.CounterpartyAssignment.objects.prefetch_related('object', 'counterparty', 'role')
    serializer_class = serializers.CounterpartyAssignmentSerializer
    filterset_class = filtersets.CounterpartyAssignmentFilterSet
