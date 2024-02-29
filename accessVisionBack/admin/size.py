from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from accessVisionBack.model import Size
from import_export import resources



class SizeResource(resources.ModelResource):
    class Meta:
        model = Size


class SizeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
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
    resource_class = SizeResource


admin.site.register(Size, SizeAdmin)