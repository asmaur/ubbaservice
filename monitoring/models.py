from django.db import models
from django.utils.translation import gettext as _


class Location(models.Model):
    pet = models.ForeignKey(
        "core.Pet",
        related_name="locations",
        on_delete=models.CASCADE
    )
    lon = models.FloatField()
    lat = models.FloatField()
    recorded_at = models.DateTimeField(
        _(""),
        auto_now=False,
        auto_now_add=True
    )
    created_at = models.DateTimeField(_(""), auto_now=False, auto_now_add=True)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'
