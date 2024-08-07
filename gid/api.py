from typing import List
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from ninja import NinjaAPI
from ninja.security import HttpBearer
from ninja.errors import HttpError
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_jwt.authentication import JWTAuth
from ninja_extra import NinjaExtraAPI
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError


api = NinjaExtraAPI(
    title='Get-It-Done Kenya', 
    description="""
    A Reporting and Management API designed to facilitate the submission of reports on various issues encountered in Kenya
    """,
    version='1.0'
)
api.register_controllers(NinjaJWTDefaultController)

@api.get('/')
def root(request):
    return {'message': 'Welcome to Get-It-Done Kenya API'}


