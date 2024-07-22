from django.http import JsonResponse
import os,requests
import json
import logging
from django.urls import reverse
from finance.models import Payment_History
# from main.models import PricingSubPlan
from marketing.models import Whatsapp_Groups, Whatsapp_dev


logger = logging.getLogger(__name__)

def best_employee(task_obj):
    sum_of_tasks = task_obj.annotate(sum=Sum('point'))
    # logger.debug(f'sum_of_tasks: {sum_of_tasks}')
    max_point = sum_of_tasks.aggregate(max=Max('sum')).get('max')
    # logger.debug(f'max_point: {max_point}')
    best_users = tuple(sum_of_tasks.filter(sum=max_point).values_list('employee__username'))
    # logger.debug(f'best_users: {best_users}')
    return best_users


def build_message_payload(ad):
    image_url = ad.image_name.image_url
    full_image_url = f'http://drive.google.com/uc?export=view&id={image_url}'
    message = ad.message
    link = ad.link
    topic = ad.ad_title if ad.ad_title else ''
    company = ad.company if ad.company else ''
    short_name = ad.short_name if ad.short_name else ''
    signature = ad.signature if ad.signature else ''
    video_link = f"Here is the recorded video:{ad.video_link}" if ad.video_link else ''
    join_link = f"Join Zoom Meeting \n:{ad.meeting_link}" if ad.video_link else ''
    company_site = ad.company_site  # Assuming this is always present

    post = f'{company}({short_name})\n\n{topic}\n{message}\n\n.{video_link}{join_link},Questions, Please reach us: {company_site}\n{signature}'

    if image_url:
        message_type = "media"
        message_content = full_image_url
        filename = "image.jpg"
    else:
        message_type = "text"
        message_content = f'{message}\nvisit us at {link}'
        filename = None

    payload = {
        "type": message_type,
        "message": message_content,
        "text": post if message_type == "media" else None,
        "filename": filename if message_type == "media" else None
    }
    return payload

def send_message(product_id, screen_id, token, group_id, message_payload):
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "x-maytapi-key": token,
    }
    url = f"https://api.maytapi.com/api/{product_id}/{screen_id}/sendMessage"
    try:
        response = requests.post(url, headers=headers, data=json.dumps(message_payload))
        if response.status_code != 200:
            logger.error(f"Error sending message to group {group_id}: {response.text}")
    except requests.RequestException as e:
        logger.error(f"Request failed: {e}")


# def update_ads_by_pricing(user):
     
#     gold_subplan = PricingSubPlan.objects.filter(title__iexact='gold', my_pricing__title='whatsapp')
#     silver_subplan = PricingSubPlan.objects.filter(title__iexact='silver', my_pricing__title='whatsapp')

#     if gold_subplan.exists():
#         gold_subplan = gold_subplan.first().id
#     else:
#         gold_subplan = 999
    
#     if silver_subplan.exists():
#         silver_subplan = silver_subplan.first().id
#     else:
#         silver_subplan = 999
    
#     if Payment_History.objects.filter(customer=user, subplan=gold_subplan).exists():
#         is_featured = True
#         is_active = True
    
#     elif Payment_History.objects.filter(customer=user, subplan=silver_subplan).exists():
#         is_featured = False
#         is_active = True
    
#     else:
#         is_featured = False
#         is_active = False
    

#     return is_featured, is_active

def populate_table_from_json_file(file_path):
    try:
        # Read the text file containing JSON data
        with open(file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
        #  Extract data into a list of dictionaries
        data_list = [{
        	# 'id': item.get('id', 'default_id'),
            # 'id': item.get('id', 'default_id')[:-15] + '-' + item.get('id', 'default_id')[-15:] if item.get('id', None) and len(item.get('id', '')) > 15 else item.get('id', 'default_id'), 
            'id': item['id'][:-15] + ('-' if '-' not in item['id'][-15:] else '') + item['id'][-15:],
        	'name': item.get('name', 'default_name'), 
        	'participants': len(item.get('participants', []))
        } for item in json_data['data']]

        # Delete all existing entries in the table
        # Whatsapp_Groups.objects.all().delete()
        # return

        # Insert or update data from data_list
        # for data in data_list:
        #     Whatsapp_Groups.objects.create(
        #         group_id=data['id'],
        #         group_name=data['name'],
        #         participants=data['participants']
        #     )
        for data in data_list:
            Whatsapp_Groups.objects.update_or_create(
                group_id=data['id'],
                defaults={
                    'group_name': data['name'],
                    'participants': data['participants']
                }
            )

    except FileNotFoundError:
        return JsonResponse({'error': 'File not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)

  

class Run_Command():
    help = 'Fetch WhatsApp groups and populate the database'

    def handle(self, *args, **kwargs):
        # Your code to fetch WhatsApp groups here
        whatsapp_groups_data = self.fetch_whatsapp_groups()

        # Iterate over the fetched data and add new groups to the database
        for group_data in whatsapp_groups_data:
            self.create_or_update_group(group_data)

    def fetch_whatsapp_groups(self):
        # Use the requests library to fetch WhatsApp groups from the API
        product_id = os.environ.get('MAYTAPI_PRODUCT_ID')
        screen_id = os.environ.get('MAYTAPI_SCREEN_ID')
        token = os.environ.get('MAYTAPI_TOKEN')
        url = f"https://api.maytapi.com/api/{product_id}/{screen_id}/getGroups"
        headers = {"x-maytapi-key": token}
        response = requests.get(url, headers=headers)

        # Check for errors and return the data as a list of dictionaries
        if response.status_code == 200:
            return response.json()
        else:
            self.stdout.write(self.style.ERROR(f"Failed to fetch WhatsApp groups. Status code: {response.status_code}"))
            return []

    def create_or_update_group(self, group_data):
        # Check if the group already exists in the database
        group_id = group_data.get("group_id")
        if Whatsapp_dev.objects.filter(group_id=group_id).exists():
            print(group_id)
            self.stdout.write(self.style.SUCCESS(f"Group with ID {group_id} already exists. Skipping."))
        else:
            # Create a new Whatsapp_Groups object with the fetched data
            Whatsapp_dev.objects.create(
                group_id=group_data.get("group_id"),
                slug=group_data.get("slug"),
                group_name=group_data.get("group_name"),
                participants=group_data.get("participants"),
                category=group_data.get("category"),
                type=group_data.get("type"),
            )
            self.stdout.write(self.style.SUCCESS(f"Added new group with ID {group_id} to the database."))
    
    