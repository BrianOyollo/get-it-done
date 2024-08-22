from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db import transaction
from ninja import Router, ModelSchema, Schema, File
from ninja.files import UploadedFile
from ninja_jwt.authentication import JWTAuth
from ninja.errors import HttpError
from typing import List
from datetime import datetime
from core.models import  Report, Subcategory, ReportStatus, ModeratorAction
from .subcategories import SubcategoryResponseSchema
from .statuses import ReportStatusSchema

router = Router(tags=['reports'])
User = get_user_model()

# ======================================= SCHEMAS =================================

class ReporterSchema(ModelSchema):
    class Meta:
        model = User
        fields = ('id','username')

class ReportResponseSchema(Schema):
    id: int
    description: str
    location: str
    latitude: float|None=None
    longitude: float|None=None
    subcategory: SubcategoryResponseSchema
    status: ReportStatusSchema
    responsible_party: str|None=None
    responsible_party_contact: str|None=None
    reporter_name: str|None=None
    reporter_contact: str|None=None
    reporter_confirm_fix_time: datetime|None=None
    created_at:datetime


class NewReportSchema(Schema):
    description: str
    location: str
    latitude: float|None=None
    longitude: float|None=None
    subcategory_id: int
    responsible_party: str|None=None
    responsible_party_contact: str|None=None
    reporter_name: str|None=None
    reporter_contact: str|None=None
    created_at:datetime


class ReportStatusChangeSchema(Schema):
    action_description: str|None=None

class FormTrials(Schema):
    first_name:str
    surname:str
    email:str
# ======================================= ROUTES ===================================
@router.get("/", response=List[ReportResponseSchema])
def reports(request):
    try:
        reports = Report.objects.all()
        return reports
    except Exception as e:
        raise HttpError(500, "Error retrieving reports")
    

@router.post("/new", response=ReportResponseSchema)
def new_report(request, payload:NewReportSchema):
    try:
        subcategory = Subcategory.objects.get(pk=payload.subcategory_id)
        pending_status = ReportStatus.objects.get(status="Pending")

        report = Report.objects.create(
            description = payload.description,
            location = payload.location,
            latitude = payload.latitude,
            longitude = payload.longitude,
            subcategory = subcategory,
            status = pending_status,
            responsible_party = payload.responsible_party,
            responsible_party_contact = payload.responsible_party_contact, 
            reporter_name = payload.reporter_name,
            reporter_contact = payload.reporter_contact
        )
        return report
    
    except Subcategory.DoesNotExist:
        raise HttpError(500, f"Subcategory with id {id} does not exist")
    except Exception as e:
        raise HttpError(500, "Error submit report")

@router.post("/upload-files")
def fileupload(request, user:FormTrials, file: UploadedFile = File(...)):
    user = user.model_dump()
    return {
        'user':user,
        'filename':file.name,
        'size':file.size,
    } 

@router.post("/{report_id}", response=ReportResponseSchema)
def report(request, report_id):
    try:
        report = Report.objects.get(pk=report_id)
        return report
    except Report.DoesNotExist:
        raise HttpError(404, "Report not found")
    except Exception as e:
        raise HttpError(500,"Error retrieving report")


@router.post("/{report_id}/update-status", auth=JWTAuth(), response=ReportResponseSchema)
def update_report_status(request, report_id, status_id, payload:ReportStatusChangeSchema):
    user =  request.user
    if not user.is_moderator:
        raise HttpError(403, "Request denied: Only moderators can update report statuses")
    
    try:
        status = ReportStatus.objects.get(pk=status_id)
        report = Report.objects.get(pk=report_id)

        if not user.is_superuser:
            if user.moderator.subcategory != report.subcategory:
                return HttpResponse(f"Request denied: You can only update reports under {user.moderator.subcategory}", status=403)
        
        with transaction.atomic():
            report.status = status
            report.save()
            ModeratorAction.objects.create(
                moderator = user.moderator,
                report = report,
                status = status,
                action_description = payload.action_description
            )
        return report
    
    except ReportStatus.DoesNotExist:
        raise HttpError(404, "Status not found")
    except Report.DoesNotExist:
        raise HttpError(404, "Report not found")
    except Exception as e:
        raise HttpError(500,f"Error updating status")


@router.delete("/{report_id}/delete", auth=JWTAuth())
def delete_report(request, report_id):
    if not request.user.is_superuser:
        raise HttpError(403, "Request denied: Only admins can delete reports")
    
    try:
        report = Report.objects.get(pk=report_id)
        report.delete()
        return HttpResponse("Report deleted", status=204)
    except Report.DoesNotExist:
        raise HttpError(404, "Report not found")
    except Exception as e:
        raise HttpError(500, "Error deleting report")



