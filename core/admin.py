from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from .forms import TagForm
from django.shortcuts import render, redirect, HttpResponse
import csv
from .models import (
    Tutor,
    Petname,
    Pet,
    Contact,
    Tag,
    Serie,
    Allotment
)
# Register your models here.


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["uuid", "url", "registered", "exported", "allotment", "created_at"]
    list_filter = ["registered", "exported"]
    search_fields = ["uuid"]


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ["name", "nickname", "petname", "tag", "tutor", "castration", "alive", "lost"]
    list_filter = ["castration", "alive", "lost"]
    search_fields = ["name", "nickname", "petname"]

    def get_tutor(self, obj):
        return obj.tutor.name

    def get_veterinarian(self, obj):
        return obj.veterinarian.doctor_name

    def get_tag(self, obj):
        return obj.tag.uuid

    def get_petname(self, obj):
        return obj.petname.petname


admin.site.register(Tutor)
admin.site.register(Petname)
admin.site.register(Contact)
admin.site.register(Serie)
admin.site.register(Allotment)
# admin.site.register(Tag, TagAdmin)
