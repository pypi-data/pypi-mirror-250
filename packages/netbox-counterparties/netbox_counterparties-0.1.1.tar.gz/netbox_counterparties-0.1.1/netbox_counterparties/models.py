from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from utilities.choices import ChoiceSet
from netbox.models import NestedGroupModel, OrganizationalModel, PrimaryModel, NetBoxModel, ChangeLoggedModel
from netbox.models.features import TagsMixin


__all__ = (
    'CounterpartyAssignment',
    'Counterparty',
    'CounterpartyGroup',
    'CounterpartyRole',
)


class CounterpartyMixin(models.Model):
    """
    Enables the assignments of Contacts (via CounterpartyAssignment).
    """
    contacts = GenericRelation(
        to='netbox_counterparties.Counterparty'
    )

    class Meta:
        abstract = True


class CounterpartyPriorityChoices(ChoiceSet):
    PRIORITY_PRIMARY = 'primary'
    PRIORITY_SECONDARY = 'secondary'
    PRIORITY_INACTIVE = 'inactive'

    CHOICES = (
        (PRIORITY_PRIMARY, _('Основной')),
        (PRIORITY_SECONDARY, _('Дополнительный')),
        (PRIORITY_INACTIVE, _('Неактивный')),
    )


class CounterpartyGroup(NestedGroupModel):
    """
    An arbitrary collection of Counterparty.
    """
    class Meta:
        ordering = ['name']
        constraints = (
            models.UniqueConstraint(
                fields=('parent', 'name'),
                name='%(app_label)s_%(class)s_unique_parent_name'
            ),
        )
        verbose_name = 'Группа контрагентов'
        verbose_name_plural = 'Группы контрагентов'

    def get_absolute_url(self):
        return reverse('plugins:netbox_counterparties:counterpartygroup', args=[self.pk])


class CounterpartyRole(OrganizationalModel):
    """
    Functional role for a counterparty assigned to an object.
    """
    def get_absolute_url(self):
        return reverse('plugins:netbox_counterparties:counterpartyrole', args=[self.pk])

    class Meta:
        ordering = ('name',)
        verbose_name = 'Роль контрагента'
        verbose_name_plural = 'Роли контрагентов'


class Counterparty(PrimaryModel):
    """
    A Systems represents an organization served by the NetBox owner. This is typically a customer or an internal
    department.
    """
    group = models.ForeignKey(
        verbose_name="Группа систем",
        to=CounterpartyGroup,
        on_delete=models.SET_NULL,
        related_name='counterparties',
        blank=True,
        null=True
    )
    tenant = models.ForeignKey(
        verbose_name="Учреждения",
        to='tenancy.Tenant',
        on_delete=models.CASCADE,
        related_name='counterparties',
        blank=True,
        null=True
    )
    name = models.CharField(
        verbose_name='ФИО',
        max_length=150
    )
    phone = models.CharField(
        verbose_name='Телефон',
        max_length=50,
        blank=True
    )
    email = models.EmailField(
        verbose_name=_('email'),
        blank=True
    )
    address = models.CharField(
        verbose_name=_('address'),
        max_length=200,
        blank=True
    )
    link = models.URLField(
        verbose_name=_('link'),
        blank=True
    )
    is_active = models.BooleanField(
        verbose_name='Активый',
        default=True
    )
    clone_fields = (
        'group', 'tenant', 'name', 'phone', 'email', 'address', 'link', 'is_active'
    )

    class Meta:
        ordering = ['name']
        constraints = (
            models.UniqueConstraint(
                fields=('group', 'name'),
                name='%(app_label)s_%(class)s_unique_group_name'
            ),
        )
        verbose_name = "Контрагент"
        verbose_name_plural = "Контрагенты"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:netbox_counterparties:counterparty', args=[self.pk])


class CounterpartyAssignment(ChangeLoggedModel, TagsMixin):
    content_type = models.ForeignKey(
        to=ContentType,
        on_delete=models.CASCADE
    )
    object_id = models.PositiveBigIntegerField()
    object = GenericForeignKey(
        ct_field='content_type',
        fk_field='object_id'
    )
    counterparty = models.ForeignKey(
        to=Counterparty,
        on_delete=models.PROTECT,
        related_name='assignments'
    )
    role = models.ForeignKey(
        to=CounterpartyRole,
        on_delete=models.PROTECT,
        related_name='assignments'
    )
    priority = models.CharField(
        verbose_name=_('priority'),
        max_length=50,
        choices=CounterpartyPriorityChoices,
        blank=True
    )

    clone_fields = ('content_type', 'object_id', 'role', 'priority')

    class Meta:
        ordering = ('priority', 'counterparty')
        constraints = (
            models.UniqueConstraint(
                fields=('content_type', 'object_id', 'counterparty', 'role'),
                name='%(app_label)s_%(class)s_unique_object_counterparty_role'
            ),
        )
        verbose_name = 'Назначение котрагента'
        verbose_name_plural = 'Назначения котрагентов'

    def __str__(self):
        if self.priority:
            return f"{self.counterparty} ({self.get_priority_display()}) -> {self.object}"
        return str(f"{self.counterparty} -> {self.object}")

    def get_absolute_url(self):
        return reverse('plugins:netbox_counterparties:counterparty', args=[self.counterparty.pk])

    def to_objectchange(self, action):
        objectchange = super().to_objectchange(action)
        objectchange.related_object = self.object
        return objectchange





