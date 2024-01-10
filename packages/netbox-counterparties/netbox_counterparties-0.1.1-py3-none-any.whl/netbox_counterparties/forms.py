from django import forms
from django.utils.translation import gettext as _
# from django.contrib.contenttypes.models import ContentType
from core.models import ContentType
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm, NetBoxModelBulkEditForm, NetBoxModelImportForm
from tenancy.models import Tenant
from netbox.forms.mixins import TagsMixin
from utilities.forms.mixins import BootstrapMixin
from utilities.forms.utils import add_blank_choice
from .models import Counterparty, CounterpartyRole, CounterpartyGroup, CounterpartyAssignment, \
    CounterpartyPriorityChoices

from django.conf import settings
from packaging import version


NETBOX_CURRENT_VERSION = version.parse(settings.VERSION)
if NETBOX_CURRENT_VERSION >= version.parse("3.5"):
    from utilities.forms.fields import (TagFilterField, CommentField, DynamicModelChoiceField, SlugField,
        ContentTypeMultipleChoiceField, DynamicModelMultipleChoiceField, CSVContentTypeField, CSVModelChoiceField)
else:
    from utilities.forms import (TagFilterField, CommentField, DynamicModelChoiceField, DynamicModelMultipleChoiceField,
         ContentTypeMultipleChoiceField, SlugField, CSVContentTypeField, CSVModelChoiceField)


class CounterpartyModelFilterForm(forms.Form):
    counterparty = DynamicModelMultipleChoiceField(
        queryset=Counterparty.objects.all(),
        required=False,
        label='Контрагент'
    )
    counterparty_role = DynamicModelMultipleChoiceField(
        queryset=CounterpartyRole.objects.all(),
        required=False,
        label='Роль Контрагента'
    )
    counterparty_group = DynamicModelMultipleChoiceField(
        queryset=CounterpartyGroup.objects.all(),
        required=False,
        label="Группа Контрагента"
    )
    counterparty_tenant = DynamicModelMultipleChoiceField(
            queryset=Tenant.objects.all(),
            required=False,
            null_option='None',
            label="Учнеждение"
        )


class CounterpartyGroupForm(NetBoxModelForm):
    parent = DynamicModelChoiceField(
        label='Родительская группа',
        queryset=CounterpartyGroup.objects.all(),
        required=False
    )
    slug = SlugField()

    fieldsets = (
        (_('Группа контрагента'), (
            'parent', 'name', 'slug', 'description', 'tags',
        )),
    )

    class Meta:
        model = CounterpartyGroup
        fields = ('parent', 'name', 'slug', 'description', 'tags')


class CounterpartyRoleForm(NetBoxModelForm):
    slug = SlugField()

    fieldsets = (
        (_('Роль контрагента'), (
            'name', 'slug', 'description', 'tags',
        )),
    )

    class Meta:
        model = CounterpartyRole
        fields = ('name', 'slug', 'description', 'tags')


class CounterpartyForm(NetBoxModelForm):
    group = DynamicModelChoiceField(
        label=_('Группа'),
        queryset=CounterpartyGroup.objects.all(),
        required=False
    )
    tenant = DynamicModelChoiceField(label='Учреждение', queryset=Tenant.objects.all())
    comments = CommentField()

    fieldsets = (
        (_('Контрагент'), ('group', 'tenant', 'name', 'phone', 'email', 'address', 'link', 'description',
                             'is_active', 'tags')),
    )

    class Meta:
        model = Counterparty
        fields = (
            'group', 'tenant', 'name', 'phone', 'email', 'address', 'link', 'description', 'comments',
            'is_active', 'tags',
        )
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class CounterpartyAssignmentForm(BootstrapMixin, TagsMixin, forms.ModelForm):
    group = DynamicModelChoiceField(
        label=_('Группа'),
        queryset=CounterpartyGroup.objects.all(),
        required=False,
        initial_params={
            'counterparties': '$counterparty'
        }
    )
    counterparty = DynamicModelChoiceField(
        label=_('Контрагент'),
        queryset=Counterparty.objects.all(),
        query_params={
            'group_id': '$group'
        }
    )
    role = DynamicModelChoiceField(
        label=_('Роль'),
        queryset=CounterpartyRole.objects.all()
    )

    class Meta:
        model = CounterpartyAssignment
        fields = (
            'content_type', 'object_id', 'group', 'counterparty', 'role', 'priority', 'tags'
        )
        widgets = {
            'content_type': forms.HiddenInput(),
            'object_id': forms.HiddenInput(),
        }


class CounterpartyFilterForm(NetBoxModelFilterSetForm):
    model = Counterparty
    # fieldsets = (
    #     (None, ('q', 'filter_id', 'tag', 'system_group_id', 'tenant_id')),
    # )
    tag = TagFilterField(model)

    group_id = DynamicModelMultipleChoiceField(
        queryset=CounterpartyGroup.objects.all(),
        required=False,
        null_option='None',
        label='Группа'
    )
    tenant_id = DynamicModelMultipleChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        null_option='None',
        query_params={
            'group_id': '$tenant_group_id'
        },
        label='Учреждение'
    )


class CounterpartyGroupFilterForm(NetBoxModelFilterSetForm):
    model = CounterpartyGroup
    parent_id = DynamicModelMultipleChoiceField(
        queryset=CounterpartyGroup.objects.all(),
        required=False,
        label=_('Родительская группа')
    )
    tag = TagFilterField(model)


class CounterpartyGroupImportForm(NetBoxModelImportForm):
    parent = CSVModelChoiceField(
        label=_('Родительская группа'),
        queryset=CounterpartyGroup.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Родительская группа')
    )
    slug = SlugField()

    class Meta:
        model = CounterpartyGroup
        fields = ('name', 'slug', 'parent', 'description', 'tags')


class CounterpartyGroupBulkEditForm(NetBoxModelBulkEditForm):
    parent = DynamicModelChoiceField(
        label=_('Родительская группа'),
        queryset=CounterpartyGroup.objects.all(),
        required=False
    )
    description = forms.CharField(
        label=_('Описание'),
        max_length=200,
        required=False
    )

    model = CounterpartyGroup
    fieldsets = (
        (None, ('parent', 'description')),
    )
    nullable_fields = ('parent', 'description')


class CounterpartyRoleFilterForm(NetBoxModelFilterSetForm):
    model = CounterpartyRole
    tag = TagFilterField(model)


class CounterpartyRoleImportForm(NetBoxModelImportForm):
    slug = SlugField()

    class Meta:
        model = CounterpartyRole
        fields = ('name', 'slug', 'description')


class CounterpartyRoleBulkEditForm(NetBoxModelBulkEditForm):
    description = forms.CharField(
        label=_('Описание'),
        max_length=200,
        required=False
    )

    model = CounterpartyRole
    fieldsets = (
        (None, ('description',)),
    )
    nullable_fields = ('description',)


class CounterpartyImportForm(NetBoxModelImportForm):
    group = CSVModelChoiceField(
        label=_('Группа'),
        queryset=CounterpartyGroup.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('Группа')
    )

    class Meta:
        model = Counterparty
        fields = ('name', 'tenant', 'phone', 'email', 'address', 'link', 'group', 'description', 'comments', 'tags')


class CounterpartyBulkEditForm(NetBoxModelBulkEditForm):
    group = DynamicModelChoiceField(
        label=_('Группа'),
        queryset=CounterpartyGroup.objects.all(),
        required=False
    )
    tenant = DynamicModelChoiceField(
        label=_('Учреждение'),
        queryset=Tenant.objects.all(),
        required=False
    )
    phone = forms.CharField(
        label=_('Телефон'),
        max_length=50,
        required=False
    )
    email = forms.EmailField(
        label=_('Email'),
        required=False
    )
    address = forms.CharField(
        label=_('Адрес'),
        max_length=200,
        required=False
    )
    link = forms.URLField(
        label=_('Ссылка'),
        required=False
    )
    description = forms.CharField(
        label=_('Описание'),
        max_length=200,
        required=False
    )
    comments = CommentField()

    model = Counterparty
    fieldsets = (
        (None, ('group', 'tenant', 'phone', 'email', 'address', 'link', 'description')),
    )
    nullable_fields = ('group', 'tenant', 'phone', 'email', 'address', 'link', 'description', 'comments')


class CounterpartyAssignmentFilterForm(NetBoxModelFilterSetForm):
    model = CounterpartyAssignment
    fieldsets = (
        (None, ('q', 'filter_id', 'tag')),
        (_('Связь'), ('content_type_id', 'group_id', 'counterparty_id', 'role_id', 'priority')),
    )
    content_type_id = ContentTypeMultipleChoiceField(
        queryset=ContentType.objects.all(),
        # limit_choices_to=ContentType.objects.with_feature('counterparties'),
        required=False,
        label=_('Тип объекта')
    )
    group_id = DynamicModelMultipleChoiceField(
        queryset=CounterpartyGroup.objects.all(),
        required=False,
        label=_('Группа')
    )
    counterparty_id = DynamicModelMultipleChoiceField(
        queryset=Counterparty.objects.all(),
        required=False,
        label=_('Контрагент')
    )
    role_id = DynamicModelMultipleChoiceField(
        queryset=CounterpartyRole.objects.all(),
        required=False,
        label=_('Роль')
    )
    priority = forms.MultipleChoiceField(
        label=_('Приоритет'),
        choices=CounterpartyPriorityChoices,
        required=False
    )
    tag = TagFilterField(model)


class CounterpartyAssignmentBulkEditForm(NetBoxModelBulkEditForm):
    counterparty = DynamicModelChoiceField(
        label=_('Контрагент'),
        queryset=Counterparty.objects.all(),
        required=False
    )
    role = DynamicModelChoiceField(
        label=_('Роль'),
        queryset=CounterpartyRole.objects.all(),
        required=False
    )
    priority = forms.ChoiceField(
        label=_('Приоритет'),
        choices=add_blank_choice(CounterpartyPriorityChoices),
        required=False
    )

    model = CounterpartyAssignment
    fieldsets = (
        (None, ('counterparty', 'role', 'priority')),
    )
    nullable_fields = ('priority',)


class CounterpartyAssignmentImportForm(NetBoxModelImportForm):
    content_type = CSVContentTypeField(
        queryset=ContentType.objects.all(),
        help_text=_("One or more assigned object types")
    )
    counterparty = CSVModelChoiceField(
        queryset=Counterparty.objects.all(),
        to_field_name='name',
        help_text=_('Assigned Counterparty')
    )
    role = CSVModelChoiceField(
        queryset=CounterpartyRole.objects.all(),
        to_field_name='name',
        help_text=_('Assigned role')
    )

    class Meta:
        model = CounterpartyAssignment
        fields = ('content_type', 'object_id', 'counterparty', 'priority', 'role')
