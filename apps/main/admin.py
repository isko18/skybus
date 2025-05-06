from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet
from apps.main.models import City, Driver, People


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('city',)


# Валидация: нельзя больше пассажиров, чем мест
class PeopleInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        if self.instance:
            total = 0
            for form in self.forms:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    total += 1
            if total > self.instance.count:
                raise ValidationError(f"Нельзя добавить больше {self.instance.count} пассажиров.")


class PeopleAdmin(admin.TabularInline):
    model = People
    extra = 0
    formset = PeopleInlineFormSet
    readonly_fields = ('row_number',)
    fields = ('row_number', 'full_name', 'phone')

    def get_max_num(self, request, obj=None, **kwargs):
        return obj.count if obj else 0

    def row_number(self, instance):
        if instance.pk:
            siblings = People.objects.filter(driver=instance.driver).order_by('pk')
            return list(siblings).index(instance) + 1
        return "—"
    row_number.short_description = "№"


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = (
        'full_name_driver',
        # 'phone_number',
        'in_city',
        'to_city',
        'waiting_date',
        'departure_date',
        'date',
        'count',
        'remaining_seats',
    )
    search_fields = ('full_name_driver', 'in_city__city', 'to_city__city')
    list_filter = ['in_city', 'to_city', 'waiting_date', 'departure_date', 'date']
    inlines = [PeopleAdmin]
    readonly_fields = ('telegram_id',)
    

    def remaining_seats(self, obj):
        taken_seats = People.objects.filter(driver=obj).count()
        return obj.count - taken_seats
    remaining_seats.short_description = 'Оставшиеся места'
