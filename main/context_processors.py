from .models import Service, SubService

def services_context(request):
    service = Service.objects.all()
    subservice = SubService.objects.all()
    for srv in service:
        for sub in srv.subservices.all():
            print(f'{srv}={sub}')
    return {
        'subservice': subservice,
        'service': service
    }
