from django.contrib import admin
from .models import Contact, Feedback, GalleryImage, Quote

admin.site.site_header = "sagarmali"
admin.site.site_title = "sagarmali"
admin.site.index_title = "sagarmali Panel"
admin.site.register(Quote)
admin.site.register(Contact)
admin.site.register(Feedback)


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ("title", "display_order", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("title", "description")
    ordering = ("display_order", "-created_at")
