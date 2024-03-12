from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.admin import SimpleListFilter
from django.utils import timezone
from .models import ContactMessage

class ContactMessageFilter(admin.SimpleListFilter):
    title = _('Timestamp')  
    parameter_name = 'timestamp'  

    def lookups(self, request, model_admin):
        return (
            ('today', _('Today')),
            ('this_week', _('This Week')),
            ('this_month', _('This Month')),
        )

    def queryset(self, request, queryset):
        now = timezone.now()
        if self.value() == 'today':
            start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
            return queryset.filter(timestamp__gte=start_of_day)
        elif self.value() == 'this_week':
            start_of_week = now - timezone.timedelta(days=now.weekday())
            start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
            return queryset.filter(timestamp__gte=start_of_week)
        elif self.value() == 'this_month':
            start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            return queryset.filter(timestamp__gte=start_of_month)
        return queryset
