from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from accessVisionBack.model import Element
from import_export import resources



class ElementResource(resources.ModelResource):
    class Meta:
        model = Element


class ElementAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "size",
        "created_at",
        "updated_at",
    )
    search_fields = ("id", "name")

    save_on_top = True
    save_as = True
    resource_class = ElementResource


admin.site.register(Element, ElementAdmin)