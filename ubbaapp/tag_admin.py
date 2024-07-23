from django.contrib import admin, messages
from django.urls import path
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.contrib.sites.shortcuts import get_current_site
import uuid
import csv
from openpyxl import Workbook
from core.forms import TagForm, ExportTagForm
from core.models import Tag


class TagBulkCreate(admin.AdminSite):
    index_template = "admin/custom_index.html"

    def get_urls(self,):
        return [
            path(
                "tag-bulk-create/",
                self.admin_view(self.bulk_create),
                name="bulk_create",
            ),
            path(
                "export-to-csv/",
                self.admin_view(self.export_to_csv),
                name="export_to_csv",
            ),
        ] + super().get_urls()

    def generateUUID(self):
        return uuid.uuid4().hex[:15].upper()

    def export_as_csv(self, request, number):
        meta = Tag._meta
        field_names = [field.name for field in meta.fields if field.name not in ("id", "registered","exported", "created_at", "allotment")]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
        writer.writerow(field_names)
        queryset = Tag.objects.filter(exported=False)[:number]
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])

        return response

    def export_to_excel(self, request, number):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename=tags_from_{timezone.now()}.xlsx'

        wb = Workbook()
        ws = wb.active
        ws.title = "Tags Urls"

        # Add headers
        headers = ["uuid", "Url"]
        ws.append(headers)

        # Add data from the model
        tags = Tag.objects.filter(exported=False)[:number]
        for tag in tags:
            ws.append([tag.uuid, tag.url])
            tag.exported = True
            tag.save()

        # Save the workbook to the HttpResponse
        wb.save(response)
        return response

    def bulk_create(self, request):
        if request.method == "POST":
            form = TagForm(request.POST)
            if form.is_valid():
                alot = form.cleaned_data["allotment"]
                quantity = form.cleaned_data["quantity"]

                for i in range(0, quantity):
                    tag_id = self.generateUUID()
                    Tag.objects.create(
                        uuid=tag_id,
                        url=f"{get_current_site(request)}/pets/{tag_id}",
                        allotment=alot,
                        created_at=timezone.now()
                    )
                return HttpResponseRedirect("/admin/core/tag/")
        else:
            form = TagForm()
        context = dict(
            page_name="Create Bulk tags",
            app_list=self.get_app_list(request),
            opts=Tag._meta,
            **self.each_context(request),
            title="Tag Bulk Create",
            form=form,
        )
        return TemplateResponse(request, "admin/tag.html", context)

    def export_to_csv(self, request):
        if request.method == "POST":
            form = ExportTagForm(request.POST)
            if form.is_valid():
                quantity = form.cleaned_data["quantity"]
                # self.export_as_csv(request, number=quantity)
                messages.success(request, "Tags data exported successfully.")
                # return self.export_as_csv(request, number=quantity)
                return self.export_to_excel(request, quantity)
                return
        else:
            form = ExportTagForm()

        context = dict(
            page_name="Export tags",
            app_list=self.get_app_list(request),
            opts=Tag._meta,
            **self.each_context(request),
            title="Export Tags",
            form=form,
        )
        return TemplateResponse(request, "admin/export.html", context)
