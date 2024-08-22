from django.http import HttpResponse
from ninja import Router, ModelSchema, Schema
from ninja_jwt.authentication import JWTAuth
from ninja.errors import HttpError
from typing import List
from django.shortcuts import get_object_or_404
from core.models import Category, Subcategory

router = Router(tags=['report category'])

# =============== SCHEMAS ==============================

class CategoryResponseSchema(ModelSchema):
    class Meta:
        model = Category
        fields = ('id', 'category', 'description',)

class NewCategorySchema(ModelSchema):
    class Meta:
        model = Category
        fields = ('category', 'description',)

class EditCategorySchema(Schema):
    category:str | None=None
    description:str | None=None

class SubcategoryResponseSchema(Schema):
    id:int
    subcategory: str
    description: str

class FullCategoryResponseSchema(Schema):
    id:int
    category: str
    description: str
    subcategories:List[SubcategoryResponseSchema]

# =============== ROUTES ===============================
@router.get("/", response=List[CategoryResponseSchema])
def categories(request):
    try:
        categories = Category.objects.all()
        return categories
    except Exception as e:
        raise HttpError(500, 'Error retrieving categories')
    

@router.post('/new', auth=JWTAuth(), response=CategoryResponseSchema)
def new_category(request, payload:NewCategorySchema): 
    if not request.user.is_superuser:
        raise HttpError(403, 'Request denied: Only admins can add new categories.')
    
    try:
        category = Category(**payload.dict())
        category.save()
        return category
    except Exception as e:
        raise HttpError(500, "Error saving category")


@router.get('/{category_id}', response=FullCategoryResponseSchema)
def category(request, category_id:int):
    try:
        category = Category.objects.get(pk=category_id)
        return category
    except Category.DoesNotExist:
        raise HttpError(404, "Category not found")
    except Exception as e:
        raise HttpError(500, 'Error retrieving category')

@router.put("/{category_id}/edit", auth=JWTAuth(), response=CategoryResponseSchema)
def edit_category(request, category_id:int, payload:EditCategorySchema):
    if not request.user.is_superuser:
        raise HttpError(403, 'Request denied: Only admins can edit categories.')
    
    category = get_object_or_404(Category, pk=category_id)
    try:
        for attr, value in payload.model_dump(exclude_unset=True).items():
            setattr(category, attr, value)

        category.save()
        return category
    
    except Exception as e:
        raise HttpError(500, "Error updating category")
    

@router.delete("/{category}/delete", auth=JWTAuth())
def delete_category(request, category:int):
    if not request.user.is_superuser:
        raise HttpError(403, 'Request denied: Only admins can delete a category')
    
    try:
        category = get_object_or_404(Category, id=category)
        category.delete()
        return HttpResponse("Category deleted", status=201)
    except Exception as e:
        raise HttpError(500, "Error deleting category")