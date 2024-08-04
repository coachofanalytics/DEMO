from .models import Service, SubService

def services_context(request):
    service = Service.objects.all()
    subservice = SubService.objects.all()
    return {
        'subservice': subservice,
        'service': service
    }
