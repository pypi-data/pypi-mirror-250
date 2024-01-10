from rest_framework import serializers
from django.contrib.auth.models import ContentType
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field

from utilities.api import get_serializer_for_model
from netbox.constants import NESTED_SERIALIZER_PREFIX
from netbox.api.fields import ChoiceField, ContentTypeField
from netbox.api.serializers import (NetBoxModelSerializer, WritableNestedSerializer, NestedGroupModelSerializer,
                                    NestedGroupModelSerializer, NetBoxModelSerializer)
from tenancy.api.nested_serializers import NestedTenantSerializer

from .nested_serializers import *
from ..models import Counterparty, CounterpartyRole, CounterpartyGroup, CounterpartyAssignment, \
    CounterpartyPriorityChoices


class CounterpartyGroupSerializer(NestedGroupModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_counterparties-api:counterpartygroup-detail')
    parent = NestedCounterpartyGroupSerializer(required=False, allow_null=True, default=None)
    counterparty_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = CounterpartyGroup
        fields = [
            'id', 'url', 'display', 'name', 'slug', 'parent', 'description', 'tags', 'custom_fields', 'created',
            'last_updated', 'counterparty_count', '_depth',
        ]


class CounterpartyRoleSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_counterparties-api:counterpartyrole-detail')

    class Meta:
        model = CounterpartyRole
        fields = [
            'id', 'url', 'display', 'name', 'slug', 'description', 'tags', 'custom_fields', 'created', 'last_updated',
        ]


class CounterpartySerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_counterparties-api:counterparty-detail')
    group = NestedCounterpartyGroupSerializer(required=False, allow_null=True, default=None)
    tenant = NestedTenantSerializer(required=False, allow_null=True, default=None)

    class Meta:
        model = Counterparty
        fields = [
            'id', 'url', 'display', 'group', 'name', 'tenant', 'phone', 'email', 'address', 'link', 'description',
            'comments', 'tags', 'custom_fields', 'created', 'last_updated',
        ]


class CounterpartyAssignmentSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_counterparties-api:counterpartyassignment-detail')
    content_type = ContentTypeField(
        queryset=ContentType.objects.all()
    )
    object = serializers.SerializerMethodField(read_only=True)
    counterparty = NestedCounterpartySerializer()
    role = NestedCounterpartyRoleSerializer(required=False, allow_null=True)
    priority = ChoiceField(choices=CounterpartyPriorityChoices, allow_blank=True, required=False, default=lambda: '')

    class Meta:
        model = CounterpartyAssignment
        fields = [
            'id', 'url', 'display', 'content_type', 'object_id', 'object', 'counterparty', 'role', 'priority', 'tags',
            'created', 'last_updated',
        ]

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_object(self, instance):
        serializer = get_serializer_for_model(instance.content_type.model_class(), prefix=NESTED_SERIALIZER_PREFIX)
        context = {'request': self.context['request']}
        return serializer(instance.object, context=context).data

