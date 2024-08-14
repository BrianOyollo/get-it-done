from django.http import HttpResponse
from ninja import Router, ModelSchema, Schema
from ninja_jwt.authentication import JWTAuth
from ninja.errors import HttpError
from typing import List
from django.shortcuts import get_object_or_404
from ..models import ReportStatus

router = Router(tags=['report status'])

# =============== SCHEMAS ==============================

class ReportStatusSchema(ModelSchema):
    class Meta:
        model = ReportStatus
        fields = ('id', 'status', 'description',)

class NewReportStatusSchema(ModelSchema):
    class Meta:
        model = ReportStatus
        fields = ('status', 'description',)
    
class EditReportStatusSchema(Schema):
    status:str | None=None
    description:str | None=None


# =============== ROUTES ===============================

@router.get('/', response=List[ReportStatusSchema])
def report_statuses(request):
    try:
        report_statuses = ReportStatus.objects.all()
        return report_statuses
    except Exception as e:
        raise HttpError(500, 'Error retrieving report statuses')

@router.post('/new', auth=JWTAuth(), response=ReportStatusSchema)
def new_report_status(request, payload:NewReportStatusSchema): 
    if not request.user.is_superuser:
        raise HttpError(403, 'Only admins can create report statuses.')
    
    try:
        report_status = ReportStatus(**payload.dict())
        report_status.save()
        return report_status
    except Exception as e:
        raise HttpError(500, "Error saving report")


@router.get('/{status_id}', response=ReportStatusSchema)
def report_status(request, status_id:int):
    try:
        report_status = ReportStatus.objects.get(pk=status_id)
        return report_status
    except ReportStatus.DoesNotExist:
        raise HttpError(404, "Status not found")
    except Exception as e:
        raise HttpError(500, 'Error retrieving report status')

@router.put("/{status_id}/edit", auth=JWTAuth(), response=ReportStatusSchema)
def edit_report_status(request, status_id:int, payload:EditReportStatusSchema):
    if not request.user.is_superuser:
        raise HttpError(403, 'Only admins can edit report statuses.')
    
    try:
        report_status = get_object_or_404(ReportStatus, pk=status_id)
        for attr, value in payload.model_dump(exclude_unset=True).items():
            setattr(report_status, attr, value)

        report_status.save()
        return report_status
    
    except Exception as e:
        raise HttpError(500, "Error updating report status")
    

@router.delete("/{status_id}/delete", auth=JWTAuth())
def delete_report_status(request, status_id:int):
    if not request.user.is_superuser:
        raise HttpError(403, 'Only admins can delete report statuses.')
    
    try:
        report_status = get_object_or_404(ReportStatus, id=status_id)
        report_status.delete()
        return HttpResponse("Status deleted", status=201)
    except Exception as e:
        raise HttpError(500, "Error deleting report status")
