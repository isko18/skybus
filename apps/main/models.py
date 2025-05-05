from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class City(models.Model):
    city = models.CharField(_("Города"), max_length=50)
    
class People(models.Model):
    full_name = models.CharField(_("ФИО"), max_length=50)
    phone = models.CharField(_("Номер"), max_length=50)
    

class Driver(models.Model):
    full_name_driver = models.CharField(_("ФИО водителя"), max_length=50)
    in_city = models.ForeignKey("City", verbose_name=_("От куда"), on_delete=models.CASCADE)
    to_city = models.ForeignKey("City", verbose_name=_("Куда"), on_delete=models.CASCADE)
    waiting_date = models.DateField(_("Дата ожидания"), auto_now=False, auto_now_add=False)
    departure_date = models.DateField(_("Дата отъезда"), auto_now=False, auto_now_add=False)
    date = models.DateTimeField(_("Время"), auto_now=False, auto_now_add=False)
    count = models.IntegerField(_("Количество мест"))
    
    