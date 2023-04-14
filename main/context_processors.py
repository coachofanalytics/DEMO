from .models import Service,Assets
from .utils import image_view

#availabity of images in this app

def categories (request):
    return {
        'categories': FeaturedCategory.objects.all()
    }
    
def subcategories (request):
    return {
        'subcategories': FeaturedSubCategory.objects.all()
    }

def images(request):
    images,image_names=image_view(request)
    return {
        'images': images,
        "image_names":image_names
    }

def services(request):
    return {
        'services': Service.objects.all()
         }

def googledriveurl(request):
    return {
        'googledriveurl':'http://drive.google.com/uc?export=view&id'
    }