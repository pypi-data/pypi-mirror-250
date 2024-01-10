from netbox.api.routers import NetBoxRouter
from . import views

app_name = 'netbox_counterparties'

router = NetBoxRouter()
router.register('counterparty-groups', views.CounterpartyGroupViewSet)
router.register('counterparty-roles', views.CounterpartyRoleViewSet)
router.register('counterparties', views.CounterpartyViewSet)
router.register('counterparty-assignments', views.CounterpartyAssignmentViewSet)

urlpatterns = router.urls
