from django.db import models
from django.utils.translation import gettext_lazy as _

class City(models.Model):
    city = models.CharField(_("Города"), max_length=50)

    def __str__(self):
        return self.city

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"


class Driver(models.Model):
    full_name_driver = models.CharField(_("ФИО водителя"), max_length=50)
    phone_number = models.CharField(_("Номер телефона"), max_length=50, help_text="Нужно через +996")
    in_city = models.ForeignKey("City", verbose_name=_("От куда"), on_delete=models.SET_NULL, related_name='incity', null=True)
    to_city = models.ForeignKey("City", verbose_name=_("Куда"), on_delete=models.SET_NULL, related_name='tocity', null=True)
    waiting_date = models.DateField(_("Дата ожидания"))
    departure_date = models.DateField(_("Дата отъезда"))
    date = models.TimeField(_("Время"))
    count = models.IntegerField(_("Количество мест"))
    telegram_id = models.BigIntegerField(_("Telegram ID"), blank=True, null=True, unique=True)

    def __str__(self):
        return self.full_name_driver

    class Meta:
        verbose_name = "Водитель"
        verbose_name_plural = "Водители"


class People(models.Model):
    driver = models.ForeignKey("Driver", verbose_name=_("Пассажир"), on_delete=models.SET_NULL, null=True)
    full_name = models.CharField(_("ФИО"), max_length=50)
    phone = models.CharField(_("Номер"), max_length=50)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Пассажир"
        verbose_name_plural = "Пассажиры"
