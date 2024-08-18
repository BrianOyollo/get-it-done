from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db import transaction
from ninja import Router, ModelSchema, Schema
from ninja_jwt.authentication import JWTAuth
from ninja.errors import HttpError
from typing import List
from datetime import datetime
from ..models import Moderator, ModeratorApplication, ModeratorAction, Subcategory
from .subcategories import SubcategoryResponseSchema

router = Router(tags=['moderators'])
User = get_user_model()

# =========================== SCHEMAS =========================
class FullUserResponseSchema(ModelSchema):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone_number','first_name', 'last_name',)
class UserResponse(ModelSchema):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number',)

class NewModeratorApplicationSchema(Schema):
    user_id:int
    first_name:str
    last_name:str
    location:str
    subcategory_id:int

class ModeratorApplicationResponseSchema(Schema):
    id:int
    user:UserResponse
    first_name:str
    last_name:str
    location:str
    subcategory:SubcategoryResponseSchema
    created_at:datetime

class ModeratorResponseSchema(Schema):
    id:int
    user:FullUserResponseSchema
    subcategory:SubcategoryResponseSchema
    created_at:datetime

# ============================ ROUTES =========================


@router.get("/", auth=JWTAuth(), response=List[ModeratorResponseSchema])
def moderators(request):
    if not request.user.is_superuser:
        raise HttpError(403, "Permission denied")
    
    try:
        moderators = Moderator.objects.all()
        return moderators
    
    except Exception as e:
        raise HttpError(500, "Error retrieving moderators")


@router.get("/applications", auth=JWTAuth(), response=List[ModeratorApplicationResponseSchema])
def moderator_applications(request):
    if not request.user.is_superuser:
        raise HttpError(403, 'You are not allowed to view this page')
    
    try:
        applications = ModeratorApplication.objects.all()
        return applications
    
    except Exception as e:
        raise HttpError(500, 'Error retrieving moderator applications')
    
@router.get("/{moderator_id}", auth=JWTAuth(), response=ModeratorResponseSchema)
def moderator(request, moderator_id:int):
    if not request.user.is_superuser:
        raise HttpError(403, "Permission denied")
    
    try:
        moderator = Moderator.objects.get(pk=moderator_id)
        return moderator
    
    except Exception as e:
        raise HttpError(500, "Error retrieving moderators")
    


@router.delete("/{moderator_id}/delete", auth=JWTAuth())
def delete_moderator(request, moderator_id:int):
    if not request.user.is_superuser:
        raise HttpError(403, "Permission denied")
    
    try:
        moderator = Moderator.objects.get(pk=moderator_id)
        with transaction.atomic():
            moderator.user.is_moderator = False
            moderator.user.save()
            moderator.delete()
        return HttpResponse("Moderator deleted", status=204)
    
    except Moderator.DoesNotExist:
        raise HttpError(404, "Moderator does not exist")

    except Exception as e:
        raise HttpError(500, "Error deleting moderator")
            


@router.post("/applications/new", auth=JWTAuth(), response=ModeratorApplicationResponseSchema) 
def new_moderator_application(request, payload:NewModeratorApplicationSchema):
    if not request.user.is_authenticated:
        raise HttpError(403, "Permission denied")
    
    if request.user.is_moderator:
        raise HttpError(403, "Permission denied")
    
    try:
        user = User.objects.get(pk=payload.user_id)
        subcategory = Subcategory.objects.get(pk=payload.subcategory_id)
        application = ModeratorApplication.objects.create(
            user = user,
            first_name = payload.first_name,
            last_name = payload.last_name,
            location = payload.location,
            subcategory = subcategory
        )

        return application
    except User.DoesNotExist:
        raise HttpError(404, "User does not exist")
    except Subcategory.DoesNotExist:
        raise HttpError(404, "Subcategory does not exist")
    except Exception as e:
        raise HttpError(500, "Error submitting application")


@router.get("/applications/{application_id}", auth=JWTAuth(),  response=ModeratorApplicationResponseSchema)
def moderator_application(request, application_id:int):
    try:
        application = ModeratorApplication.objects.get(pk=application_id)
        if request.user == application.user or request.user.is_superuser:
            return application
        else:
            raise HttpError(403, "Permission denied")

    except ModeratorApplication.DoesNotExist:
        raise HttpError(404, "Application does not exist")
    
    except Exception as e:
        raise HttpError(500, 'Error retrieving moderator application')



@router.post("/applications/{application_id}/approve", auth=JWTAuth(), response=ModeratorResponseSchema)
def approve_moderator_application(request, application_id:int):
    if not request.user.is_superuser:
        raise HttpError(403, "Permission denied")
    
    try:
        application = ModeratorApplication.objects.get(pk=application_id)
        with transaction.atomic():
            # update user
            applicant = application.user
            applicant.first_name = application.first_name
            applicant.last_name = application.last_name
            applicant.is_moderator = True
            applicant.save()

            # create moderator
            moderator, created = Moderator.objects.get_or_create(user=applicant, location=application.location, subcategory=application.subcategory)

            # update application status
            application.status = 'Approved'
            application.save()

        return moderator
    
    except ModeratorApplication.DoesNotExist:
        raise HttpError(404, "Application does not exist")
    
    except Exception as e:
        raise HttpError(500,f"Error approving application:{e}")
    

    
