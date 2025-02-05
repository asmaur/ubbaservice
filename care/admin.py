from django.contrib import admin
from .models import (
    Veterinarian,
    Contact,
    VaccinationCard,
    Photo
)
# Register your models here.

admin.site.register(Veterinarian)
admin.site.register(Contact)
admin.site.register(Photo)
admin.site.register(VaccinationCard)
