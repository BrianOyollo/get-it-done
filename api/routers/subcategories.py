from django.http import HttpResponse
from ninja import Router, ModelSchema, Schema
from ninja_jwt.authentication import JWTAuth
from ninja.errors import HttpError
from typing import List
from django.shortcuts import get_object_or_404
from core.models import Category, Subcategory

router = Router(tags=['report subcategory'])

# =============== SCHEMAS ==============================
class CategoryResponseSchema(ModelSchema):
    class Meta:
        model = Category
        fields = ('id', 'category',)

class SubcategoryResponseSchema(ModelSchema):
    class Meta:
        model = Subcategory
        fields = ('id','subcategory', 'description','category',)

class FullSubcategoryResponseSchema(Schema):
    id:int
    subcategory:str
    description: str
    category:CategoryResponseSchema

class NewSubcategorySchema(ModelSchema):
    class Meta:
        model = Subcategory
        fields = ('category','subcategory', 'description',)

class EditSubcategorySchema(Schema):
    subcategory:str | None=None
    description:str | None=None

# =============== ROUTES ===============================

@router.get("/", response=List[FullSubcategoryResponseSchema])
def subcategories(request):
    try:
        subcategories = Subcategory.objects.all()
        return subcategories
    except Exception as e:
        raise HttpError(500, 'Error retrieving subcategories')
    

@router.post('/new', auth=JWTAuth(), response=SubcategoryResponseSchema)
def new_subcategory(request, payload:NewSubcategorySchema): 
    if not request.user.is_superuser:
        raise HttpError(403, 'Request denied: Only admins can add new subcategories')

    try:
        category = get_object_or_404(Category, pk=payload.category)
        subcategory, created = Subcategory.objects.get_or_create(
            category=category, 
            description=payload.description, 
            subcategory=payload.subcategory
        )
        return subcategory
    except Category.DoesNotExist:
        raise HttpError(404, "Category not found")
    except Exception as e:
        raise HttpError(500, f"Error saving subcategory")


@router.get("/{subcategory_id}", response=FullSubcategoryResponseSchema)
def subcategory(request, subcategory_id:int):
    try:
        subcategory = Subcategory.objects.get(pk=subcategory_id)
        return subcategory
    except Subcategory.DoesNotExist:
        raise HttpError(404, "Subcategory not found")
    except Exception as e:
        raise HttpError(500, 'Error retrieving subcategory')


@router.put("/{subcategory_id}/edit", auth=JWTAuth(), response=SubcategoryResponseSchema)
def edit_subcategory(request, subcategory_id:int, payload:EditSubcategorySchema):
    if not request.user.is_superuser:
        raise HttpError(403, 'Request denied: Only admins can edit subcategories')
    
    subcategory = get_object_or_404(Subcategory, pk=subcategory_id)
    try:
        for attr, value in payload.model_dump(exclude_unset=True).items():
            setattr(subcategory, attr, value)

        subcategory.save()
        return subcategory
    
    except Exception as e:
        raise HttpError(500, f"Error updating subcategory:{e}")
    

@router.delete("/{subcategory_id}/delete", auth=JWTAuth())
def delete_subcategory(request, subcategory_id:int):
    if not request.user.is_superuser:
        raise HttpError(403, 'Request denied: Only admins can delete subcategories')
    
    try:
        subcategory = get_object_or_404(Subcategory, pk=subcategory_id)
        subcategory.delete()
        return HttpResponse("Subcategory deleted", status=201)
    except Subcategory.DoesNotExist:
        raise HttpError(404, "Subcategory not found")
    except Exception as e:
        raise HttpError(500, "Error deleting subcategory")