from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers

from netbox.api.serializers import WritableNestedSerializer
from ..models import *

__all__ = [
    'NestedCounterpartySerializer',
    'NestedCounterpartyAssignmentSerializer',
    'NestedCounterpartyGroupSerializer',
    'NestedCounterpartyRoleSerializer',
]


@extend_schema_serializer(
    exclude_fields=('counterparty_count',),
)
class NestedCounterpartyGroupSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_counterparties-api:counterpartygroup-detail')
    counterparty_count = serializers.IntegerField(read_only=True)
    _depth = serializers.IntegerField(source='level', read_only=True)

    class Meta:
        model = CounterpartyGroup
        fields = ['id', 'url', 'display', 'name', 'slug', 'counterparty_count', '_depth']


class NestedCounterpartyRoleSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_counterparties-api:counterpartyrole-detail')

    class Meta:
        model = CounterpartyRole
        fields = ['id', 'url', 'display', 'name', 'slug']


class NestedCounterpartySerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_counterparties-api:counterparty-detail')

    class Meta:
        model = Counterparty
        fields = ['id', 'url', 'display', 'name']


class NestedCounterpartyAssignmentSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_counterparties-api:counterpartyassignment-detail')
    counterparty = NestedCounterpartySerializer()
    role = NestedCounterpartyRoleSerializer

    class Meta:
        model = CounterpartyAssignment
        fields = ['id', 'url', 'display', 'counterparty', 'role', 'priority']
