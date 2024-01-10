from netbox.search import SearchIndex
from .models import CounterpartyRole, Counterparty, CounterpartyGroup
from django.conf import settings

# If we run NB 3.4+ register search indexes 
if settings.VERSION >= '3.4.0':
    class CounterpartyGroupIndex(SearchIndex):
        model = CounterpartyGroup
        fields = (
            ('name', 100),
            ('slug', 110),
            ('description', 500),
        )

    class CounterpartyIndex(SearchIndex):
        model = Counterparty
        fields = (
            ('name', 100),
            ('phone', 300),
            ('email', 300),
            ('address', 300),
            ('link', 300),
            ('description', 500),
            ('comments', 5000),
        )

    class CounterpartyRoleIndex(SearchIndex):
        model = CounterpartyRole
        fields = (
            ('name', 100),
            ('slug', 110),
            ('description', 500),
        )

    # Register indexes
    indexes = [CounterpartyGroupIndex, CounterpartyIndex, CounterpartyRoleIndex]
