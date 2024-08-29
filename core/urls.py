from django.urls import path
from .views import (
    HomeView, NewReportPage, NewReportView, 
    ReportDetailsView, CategoryFilterView, SubcategoryFilterView, 
    AboutView)


urlpatterns = [
    path('', HomeView, name='home'),
    path('about/', AboutView, name='about-page'),
    path('reports/<int:report_id>', ReportDetailsView, name="report-details"),
    path("new-report-page/", NewReportPage, name='new-report-page'),
    path("new-report", NewReportView, name="new-report"),
    path("reports/category/<int:category_id>", CategoryFilterView, name='category-filter'),
    path("reports/subcategory/<int:subcategory_id>", SubcategoryFilterView, name='subcategory-filter')
]