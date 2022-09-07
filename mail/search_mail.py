import  os
import  logging
logger = logging.getLogger(__name__)

from django.http import HttpResponse

from gapi.gservices import get_service, search_messages, get_message
from getdata.models import CashappMail


def parse_mail(request):
    search_query = 'from:cash@square.com is:unread'

    service = get_service()  # default service with default scope, gmail-v1
    if not service:
        return HttpResponse('No service!')

    search_results = search_messages(service, search_query)
    search_results_len = len(search_results)
    logger.debug(f'search_results_len: {search_results_len}')

    if not search_results:
        return HttpResponse('No results found!')

    for result in search_results:
        msg_dict = get_message(service=service, msg_id=result.get('id'))
        # print(f'msg_dict: {msg_dict}')
        # logger.debug(f'msg_dict: {msg_dict}')

        try:
            CashappMail.objects.create(
                id=msg_dict.get('id'),
                from_mail=msg_dict.get('from_mail'),
                to_mail=msg_dict.get('to_mail'),
                subject=msg_dict.get('subject'),
                file_name=msg_dict.get('file_name'),
                full_path=msg_dict.get('full_path'),
                text_mail=msg_dict.get('text_mail'),
                received_date=msg_dict.get('received_date')
            )
        except Exception as e:
            logger.error('error on adding new record!')
            logger.error('error msg is ' + str(e))
            logger.error(f'msg id is: msg_dict.get("id")')
            # return HttpResponse("Error on createing a record!")

    return HttpResponse(f'{search_results_len} results processed!')
