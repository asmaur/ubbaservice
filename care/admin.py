from django.contrib import admin
from .models import (
    Veterinarian,
    Contact,
)
# Register your models here.

admin.site.register(Veterinarian)
admin.site.register(Contact)
