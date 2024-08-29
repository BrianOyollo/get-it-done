from django.shortcuts import render
from django.db import transaction
from django.shortcuts import get_object_or_404

from .models import Report, ReportStatus, ReportFile, Subcategory, Category
from .forms import NewReportForm

# Create your views here.
def HomeView(request):
    #TODO: checkout select_related and prefetch_related for query optimization

    reports = Report.objects.all()
    subcategories = Subcategory.objects.all()
    categories = Category.objects.all()
    if request.htmx:
        return render(request, 'home.html#HomePage-partial',{
            'reports':reports,
            'all_reports_count': reports.count(),
            'categories':categories,
            'subcategories':subcategories,
        })
    else:
        return render(request, 'home.html', {
            'reports':reports,
            'all_reports_count': reports.count(),
            'categories':categories,
            'subcategories':subcategories,
        })

def AboutView(request):
    if request.htmx:
        return render(request, 'about.html#AboutPage-partial')
    else:
        return render(request, 'about.html')

def CategoryFilterView(request, category_id):
    category = Category.objects.get(pk=category_id)
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    all_reports_count = Report.objects.all().count()
    reports = Report.objects.filter(subcategory__category=category).all()

    if request.htmx:
        return render(request, 'home.html#HomePage-partial',{
                'reports':reports,
                'all_reports_count':all_reports_count,
                'categories':categories,
                'subcategories':subcategories,
            })
    else:
        return render(request, 'home.html',{
            'reports':reports,
            'categories':categories,
            'all_reports_count':all_reports_count,
            'subcategories':subcategories,
        })
    
def SubcategoryFilterView(request, subcategory_id):
    subcategory = Subcategory.objects.get(pk=subcategory_id)
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    all_reports_count = Report.objects.all().count()
    reports = Report.objects.filter(subcategory=subcategory).all()

    if request.htmx:
        return render(request, 'home.html#HomePage-partial',{
                'reports':reports,
                'all_reports_count':all_reports_count,
                'categories':categories,
                'subcategories':subcategories,
            })
    else:
        return render(request, 'home.html',{
            'reports':reports,
            'categories':categories,
            'all_reports_count':all_reports_count,
            'subcategories':subcategories,
        })

def ReportDetailsView(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    if request.htmx:
        return render(request, 'report-details.html#ReportDetails-partial',{
            'report':report,
        })
    else:
        return render(request, 'report-details.html',{
            'report':report,
        })
    
def NewReportPage(request):
    form = NewReportForm()
    if request.htmx:
        return render(request, 'new_report.html#NewReport-partial',{
            'form':form,
        })
    else:
        return render(request, 'new_report.html', {
            'form':form,
        })

def NewReportView(request):
    if request.method == "POST":
        form = NewReportForm(request.POST, request.FILES)
        if form.is_valid():
            report_description = form.cleaned_data['description']
            subcategory_id = form.cleaned_data['subcategory']
            location = form.cleaned_data['location']
            responsible_party = form.cleaned_data['responsible_party']
            responsible_party_contact = form.cleaned_data['responsible_party_contact']
            reporter_name = form.cleaned_data['reporter_name']
            reporter_contact = form.cleaned_data['reporter_contact']
            latitude = form.cleaned_data['latitude']
            longitude = form.cleaned_data['longitude']
            files = request.FILES.getlist('files')

            
            subcategory = Subcategory.objects.get(pk=subcategory_id)
            pending_status = ReportStatus.objects.get(status="Pending")
            with transaction.atomic():
                new_report = Report.objects.create(
                    description = report_description,
                    location = location,
                    latitude = latitude,
                    longitude = longitude,
                    subcategory = subcategory,
                    status = pending_status,
                    responsible_party = responsible_party,
                    responsible_party_contact = responsible_party_contact,
                    reporter_name = reporter_name,
                    reporter_contact = reporter_contact
                )

                for file in files:
                    ReportFile.objects.create(file=file, report=new_report)

            reports = Report.objects.all()
            return render(request, 'submission_success.html#ReportSubmissionSuccess-partial')
    else:
        form = NewReportForm()
        return render(request, 'new_report.html#NewReport-partial',{
            'form':form,
        })
    

        
