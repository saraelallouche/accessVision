from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from accessVisionBack.model import Tracking
from import_export import resources



class TrackingResource(resources.ModelResource):
    class Meta:
        model = Tracking


class TrackingAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = (
        "id",
        "tracking",
        "created_at",
        "updated_at",
    )
    search_fields = ("id", "ip", "tracking")

    save_on_top = True
    save_as = True
    resource_class = TrackingResource


admin.site.register(Tracking, TrackingAdmin)