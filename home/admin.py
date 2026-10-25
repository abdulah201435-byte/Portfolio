from django.contrib import admin
from .models import Service, Skill, Project, ProjectScreenshot, Review, ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created", "handled")
    list_editable = ("handled",)
    readonly_fields = ("name", "email", "message", "created")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "icon", "order", "visible")
    list_editable = ("order", "visible")


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "cat", "icon", "order", "visible")
    list_editable = ("order", "visible")
    list_filter = ("cat",)


class ScreenshotInline(admin.TabularInline):
    model = ProjectScreenshot
    extra = 3


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "date", "status", "order", "visible")
    list_editable = ("order", "visible")
    inlines = [ScreenshotInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created", "approved")
    list_editable = ("approved",)
    list_filter = ("approved",)