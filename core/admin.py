from django.contrib import admin
from .models import *

# Register your models here.
class ReportStatusAdmin(admin.ModelAdmin):
    model = ReportStatus
    list_display = ('id','status', 'description', 'created_at',)

class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ('id','category', 'description', 'created_at',)

class SubcategoryAdmin(admin.ModelAdmin):
    model = Subcategory
    list_display = ('id','subcategory', 'description', 'category', 'created_at',)

class ModeratorApplicationAdmin(admin.ModelAdmin):
    model = ModeratorApplication
    list_display = ('id','user', 'location', 'subcategory', 'status', 'created_at',)
    
class ModeratorAdmin(admin.ModelAdmin):
    model = Moderator
    list_display = ('id','user','location', 'subcategory', 'created_at',)

class ReportAdmin(admin.ModelAdmin):
    model = Report
    list_display = ('id','subcategory', 'description', 'location', 'latitude', 'longitude','status',)

class ModeratorActionAdmin(admin.ModelAdmin):
    model = ModeratorAction
    list_display = ('id','moderator', 'report', 'status', 'action_description', 'created_at',)

class ReportFileAdmin(admin.ModelAdmin):
    model = ReportFile
    list_display = ('id','file', 'report', 'created_at',)


admin.site.register(ReportStatus, ReportStatusAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Moderator, ModeratorAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(ModeratorAction, ModeratorActionAdmin)
admin.site.register(ModeratorApplication, ModeratorApplicationAdmin)
admin.site.register(ReportFile, ReportFileAdmin)

admin.site.site_header = 'Get-It-Done Kenya Admin'
