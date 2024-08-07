from django.contrib import admin
from .models import *

# Register your models here.
class ReportStatusAdmin(admin.ModelAdmin):
    model = ReportStatus
    list_display = ('status', 'description', 'created_at',)

class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ('category', 'description', 'created_at',)

class SubcategoryAdmin(admin.ModelAdmin):
    model = Subcategory
    list_display = ('subcategory', 'description', 'category', 'created_at',)

class ModeratorAdmin(admin.ModelAdmin):
    model = Moderator
    list_display = ('user','location', 'subcategory', 'created_at',)

class ReportAdmin(admin.ModelAdmin):
    model = Report
    list_display = ('subcategory', 'description', 'location', 'latitude', 'longitude',)

class ModeratorActionAdmin(admin.ModelAdmin):
    model = ModeratorAction
    list_display = ('moderator', 'report', 'status', 'action_description', 'created_at',)

class ReportFileAdmin(admin.ModelAdmin):
    model = ReportFile
    list_display = ('file', 'report', 'created_at',)


admin.site.register(ReportStatus, ReportStatusAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Moderator, ModeratorAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(ModeratorAction, ModeratorActionAdmin)
admin.site.register(ReportFile, ReportFileAdmin)

admin.site.site_header = 'Get-It-Done Kenya Admin'
