import os,requests
import json
import logging
# from django.core.management import call_command
from django.db.models import IntegerField, F,Sum, Q
from django.db.models.functions import Cast
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, render
from marketing.models import Ads,Whatsapp_Groups,Whatsapp_dev
from coda_project import settings
from .forms import WhatsappForm,AdsForm
from django.urls import reverse
from mail.custom_email import send_email
from main.utils import path_values
from marketing.utils import Run_Command, populate_table_from_json_file
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
        CreateView,
        UpdateView,
    )

from django.contrib.auth import get_user_model
# from .utils import update_ads_by_pricing
#from main.permission import check_payment_history_permission

User=get_user_model()
logger = logging.getLogger(__name__)
#====================General===========================
@login_required
def fetch_whatsapp_groups(request):
    file_path='media/marketing/whatsapp_groups/Whatsapp_Groups_11232023_v1.txt'
    populate_table_from_json_file(file_path)
    return redirect('marketing:whatsapp_list')
	
@login_required
def marketing(request):
    social_media_cards = [
        {
            'title': 'Whatsapp',
            'description': 'Managing WhatsApp groups.',
            'menu_items': [
                {'text': 'Run to Publish', 'url': reverse('marketing:whatsapp')},
                {'text': 'Add New Group', 'url': reverse('marketing:whatsapp_new')},
                {'text': 'See Groups', 'url': reverse('marketing:whatsapp_list', kwargs={'title': 'all'})},
                {'text': 'Populate Groups', 'url': reverse('marketing:whatsappgroups') if request.user.is_superuser else reverse('finance:pay')},
                {'text': 'PPT-Automation', 'url': 'https://docs.google.com/presentation/d/1JBWX_QI6BBJrJhtZdahYRzFpFRXpe-lK/edit#slide=id.p2'}
            ]
        },
        {
            'title': 'Facebook',
            'description': 'Managing Facebook',
            'menu_items': [
                {'text': 'Run to Publish', 'url': 'https://www.facebook.com/chris.maghas/'},
                {'text': 'Our Page', 'url': 'https://www.facebook.com/coachchrismaghas/'},
                {'text': 'PPT-Automation', 'url': '#'}
            ]
        },
        {
            'title': 'Twitter',
            'description': 'Managing Twitter',
            'menu_items': [
                {'text': 'Run to Publish', 'url': '#'},
                {'text': 'twitter Page', 'url': 'https://twitter.com/CrownData'},
                {'text': 'PPT-Automation', 'url': '#'}
            ]
        },
    ]
    context={
        "title": "Marketing",
        'social_media_cards': social_media_cards,
    }
    return render(request, "marketing/socialmedia.html",context)
#====================Social Media===========================

#====================AD MANAGEMENT===========================
class AdsCreateView(LoginRequiredMixin, CreateView):
    model = Ads
    success_url = "marketing/adslist/"  
    form_class=AdsForm
    # fields = "__all__"

    def get_success_url(self):
        return reverse("marketing:ads_list")
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user.is_superuser
        return kwargs

    # def form_valid(self, form):
    #     form.instance.my_user = self.request.user
    #     if not self.request.user.is_superuser:
            
    #         if not self.request.user.is_superuser:
    #             is_featured, is_active = update_ads_by_pricing(form.instance.my_user)
    #             form.instance.is_featured = is_featured
    #             form.instance.is_active = is_active

    #     return super().form_valid(form)


class AdsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ads # Whatsapp 
    form_class=AdsForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user.is_superuser
        return kwargs
    
    # def form_valid(self, form):
    #     form.instance.username = self.request.user
        
    #     if not self.request.user.is_superuser:
    #         is_featured, is_active = update_ads_by_pricing(form.instance.my_user)
    #         form.instance.is_featured = is_featured
    #         form.instance.is_active = is_active
            
    #     return super().form_valid(form)

    def get_success_url(self):
        return reverse("marketing:ads_list")

    def test_func(self):
        # plan = self.get_object()
        if self.request.user.is_superuser:
            return True
        elif self.request.user:
            return True
        return False

@login_required
def delete_ads(request,id):
    ad = Ads.objects.get(pk=id)
    if request.user.is_superuser:
        ad.delete()
    return redirect('marketing:ads_list')

@login_required
def ads(request):
    if request.user.is_superuser:
        
        ad_items=Ads.objects.all()
    else:
        ad_items=Ads.objects.filter(my_user=request.user)
    context={
            "ad_items":ad_items
    }
    return render(request, 'marketing/adlist.html',context)

#====================WHATSAPP MANAGEMENT===========================
class whatsappCreateView(LoginRequiredMixin, CreateView):
    model = Whatsapp_Groups
    success_url = "/marketing/whatsapplist/"  
    form_class=WhatsappForm
    # fields = "__all__"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    

class whatsappUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Whatsapp_Groups
    form_class = WhatsappForm

    def form_valid(self, form):
        form.instance.username = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # Replace 'all' with the appropriate title value you need to pass
        return reverse("marketing:whatsapp_list", kwargs={'title': 'all'})

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        elif self.request.user:
            return True
        return False


@login_required
def delete_whatsapp(request,slug):
    whatsapp_record = Whatsapp_Groups.objects.get(pk=slug)
    if request.user.is_superuser:
        whatsapp_record.delete()
    return redirect('marketing:whatsapp_list')

@login_required
def whatsapp_groups(request, title):
    CATEGORY_CHOICES = [
        "all",
        "Finance",
        "IT",
        "Internal",
        "Political",
        "Business",
        "other",
    ] 
    TYPE_CHOICES = [
        "all",
        "investments",
        "data_analysis",
        "coda",
        "Job_Support",
        "interview",
        "mentorship",
        "automation",
        "other",
    ]

    # Annotate groups with participant count
    annotated_whatsapp_groups = Whatsapp_Groups.objects.annotate(
        participant_count=Cast('participants', IntegerField())
    )
    
    if request.method == 'POST':
       
        selected_option = request.POST.get('dropdown_option')
        category = request.POST.get('category', 'all')
        ads_type = request.POST.get('ads_type', 'all') 
        action = request.POST.get('action', 'search')
        
        if category != "all":
            annotated_whatsapp_groups = annotated_whatsapp_groups.filter(category=category)

        if ads_type != "all":
            annotated_whatsapp_groups = annotated_whatsapp_groups.filter(type=ads_type)

        if action != "search":
            
            action = request.POST.get('action', 'search') == 'true'
            if selected_option == 'is_active':
                annotated_whatsapp_groups.update(is_active=action)
            elif selected_option == 'is_featured':
                annotated_whatsapp_groups.update(is_featured=action)            

    # Fetch groups based on title
    if title == 'active_groups':
        whatsapp_groups = annotated_whatsapp_groups.filter(is_active=True)

    elif title == 'featured_groups':
        whatsapp_groups = annotated_whatsapp_groups.filter(is_featured=True)

    elif title == 'silver':
        # Filter groups with participant count between 150 and 500
        whatsapp_groups = annotated_whatsapp_groups.filter(participant_count__gte=150, participant_count__lte=500)

    elif title == 'basic':
        # Filter groups with participant count less than 150
        whatsapp_groups = annotated_whatsapp_groups.filter(participant_count__lt=150)

    else:
        # Default case: Fetch all groups and order by participant count
        whatsapp_groups = annotated_whatsapp_groups

    # Calculate the total participants across all fetched groups
    total_participants = whatsapp_groups.aggregate(total=Sum('participant_count'))['total'] if whatsapp_groups else 0
    
    # Prepare the context data for rendering
    context = {
        "whatsapp_items": whatsapp_groups.order_by('-participant_count'),
        "total_participants": total_participants,
        "category_choices": CATEGORY_CHOICES,
        "ads_type_choices": TYPE_CHOICES
    }
    return render(request, 'marketing/groups.html', context)


# @login_required
# def whatsapp_groups(request):
#     # whatsaapitems=Whatsapp_Groups.objects.all().order_by('participants')
#     whatsapp_groups = Whatsapp_dev.objects.annotate(
#     participant_count=Cast('participants', IntegerField())).order_by('-participant_count')
#     total_participants = Whatsapp_dev.objects.aggregate(
#     total=Sum(Cast('participants', IntegerField()))
#     )['total']
#     print(total_participants)
#     context={
#             "whatsaapitems":whatsapp_groups,
#             "total_participants":total_participants
#     }
#     return render(request, 'marketing/groups.html',context)


@login_required(login_url="accounts:account-login")
def refresh_whatsapp_groups(request):
    # Trigger the management command
    if request.user.is_superuser:
        Run_Command('fetch_whatsapp_groups')
        return redirect('marketing:whatsapp_list')
    else:
        return redirect('marketing:whatsapp_list')

# @login_required(login_url="accounts:account-login")
# def refresh_whatsapp_groups(request):
#     Run_Command('fetch_whatsapp_groups')
#     return redirect('marketing:whatsapp_list')


@login_required(login_url="accounts:account-login")
def runwhatsapp(request):
    product_id = os.environ.get('MAYTAPI_PRODUCT_ID')
    screen_id = os.environ.get('MAYTAPI_SCREEN_ID')
    token = os.environ.get('MAYTAPI_TOKEN')
    title = 'WHATSAPP'
    # ads_items = Ads.objects.filter(is_active=True, image_name__is_active=True)
    #ads_items = Ads.objects.filter(image_name__is_active=True, my_user=request.user).filter(Q(is_active=True) | Q(is_featured=True))
    
    ads_items = Ads.objects.filter(is_active=True).filter(Q(is_active=True) | Q(is_featured=True))
    
    print("ads_items==========>",ads_items)
  
    
    for ad in ads_items:
        # whatsapp_groups = Whatsapp_Groups.objects.filter(type=ad.image_name.category,is_active=True)
        # whatsapp_groups = Whatsapp_Groups.objects.filter(type=ad.image_name.name,is_active=True)
    
        if ad.is_featured:
            whatsapp_groups = Whatsapp_Groups.objects.filter(type=ad.image_name.name).filter(Q(is_active=True) | Q(is_featured=True))
        elif ad.is_active:
            whatsapp_groups = Whatsapp_Groups.objects.filter(type=ad.image_name.name).filter(is_active=True)
        else:
            whatsapp_groups = Whatsapp_Groups.objects.filter(type=ad.image_name.name).annotate(
                participant_count=Cast('participants', IntegerField())
            ).filter(participant_count__lt=150)
        # print("whatsapp_groups==========>",whatsapp_groups)
        group_ids = list(whatsapp_groups.values_list('group_id', flat=True))
        group_names = list(whatsapp_groups.values_list('group_name', flat=True))
        print("whatsapp_NAMES==========>",group_names)
        
        image_url = ad.image_name.image_url
        full_image__url=f'http://drive.google.com/uc?export=view&id={image_url}'
        message = ad.message
        company_description = ad.description if ad.description else ''
        link = ad.link
        # topic=ad.ad_title if ad.ad_title else 'General'
        topic=ad.bulletin if ad.bulletin else 'General'
        company=ad.company if ad.company else 'CROWN DATA ANALYSIS & CONSULTING LLC'
        short_name=ad.short_name if ad.short_name else 'CODA'
        signature=ad.signature if ad.signature else 'Chris Maghas-AI|Automation Expert'
        company_site=ad.company_site if ad.signature else 'www.codanalytics.net/accounts/join'
        video_link= f"Here is the recorded video:{ad.video_link}" if ad.video_link else ''
        join_link= f"Join Zoom Meeting \n:{ad.meeting_link}" if ad.meeting_link else ''
        post= f'{company}-{short_name}\n\n{company_description}\n\n{topic}\n\n{message}\n\n{video_link}\n{join_link}\n\nFor questions, please reach us at: {company_site}\n{signature}'

        for group_id in group_ids:
            # Validate data
            if not group_id:
                logger.error("Group ID is missing.")
                continue

            if not full_image__url:
                logger.error(f"image__url content is missing for group {group_id}.")
                continue

            if not post:
                logger.error(f" post is missing for group {group_id}.")
                continue

            if image_url:
                message_type = "media"
                message_content = full_image__url
                filename = "image.jpg"

                payload = {
                    "to_number": group_id,
                    "type": message_type,
                    "message": message_content,
                    "text":post #f'{message}\nvisit us at {link}'
                }
            else:
                message_type = "text"
                message_content = post # f'{message}\nvisit us at {link}'
                filename = None

                payload = {
                    "to_number": group_id,
                    "type": message_type,
                    "message": message_content,
                    "filename": filename,
                }
            headers = {
                "accept": "application/json",
                "Content-Type": "application/json",
                "x-maytapi-key": token,
            }
            url = f"https://api.maytapi.com/api/{product_id}/{screen_id}/sendMessage"
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            if response.status_code != 200:
                error_message=f"Error sending message to group {group_id}. Details: {response.content}"
                logger.error(error_message)
                print(error_message)

    message = f"Hi, {request.user}, your ads have been sent to your selected groups"
    context = {"title": title, "message": message}
    return render(request, "main/errors/generalerrors.html", context)


# @login_required(login_url="accounts:account-login")
# def runwhatsapp(request):
#     product_id = os.environ.get('MAYTAPI_PRODUCT_ID')
#     screen_id = os.environ.get('MAYTAPI_SCREEN_ID')
#     token = os.environ.get('MAYTAPI_TOKEN')
#     title = 'WHATSAPP'

#     ads_items = Ads.objects.filter(is_active=True).prefetch_related('image_name')
#     for ad in ads_items:
#         whatsapp_groups = Whatsapp_Groups.objects.filter(type=ad.image_name.category)
#         group_ids = list(whatsapp_groups.values_list('group_id', flat=True))

#         message_payload = build_message_payload(ad)

#         for group_id in group_ids:
#             send_message(product_id, screen_id, token, group_id, message_payload)

#     messages.success(request, "Your messages have been sent to your groups.")
#     return render(request, "main/errors/generalerrors.html", {"title": title})

def send_email_ads(request):
    path_list,sub_title,pre_sub_title=path_values(request)
    subject='NEXT CLASSES!SIGN UP!'
    url='marketing/marketing_ads.html'
    message=''
    error_message=f'Hi,{request.user.first_name}, there seems to be an issue on our end.kindly contact us directly for payment details.'
    context_data = 'services(request)'
    # user_category = request.user.category
    # Retrieve the list of users based on their category
    # users_to_email = User.objects.filter(category=user_category)
    users_to_email = User.objects.filter(is_staff=True,is_active=True)
    # print(users_to_email)
    plans = context_data.get('plans')
    pricing_info = context_data.get('pricing_info')
    context={
                "SITEURL": settings.SITEURL,
                'subtitle': sub_title,
                # "services": plans,
                'services': pricing_info,
                
                'message':message,
                'error_message':error_message,
                'contact_message':'info@codanalytics.net',
            }
    try:
        # Send email to each user in the selected category
        # for user in users_to_email:
        #     context['user'] = user.first_name
        #     send_email(
        #         category=user.category,  
        #         to_email=[user.email],
        #         subject=subject,
        #         html_template=url,
        #         context=context
        #     )

        # return render(request, "marketing/marketing_ads.html", context)
        return render(request, "marketing/newad.html", context)
    except Exception as e:
        print(f"An error occurred: {e}")
        # return render(request, "marketing/marketing_ads.html", context)
        return render(request, "marketing/trainingad.html", context)
    

def send_training_ad(request):
    subject='DATA ANALYSIS|SCIENCE|AI COURSE'
    title2='TIMELINE,LOCATION & OUTCOMES'
    # url='email/marketing/trainingad.html'
    url='email/marketing/trainad.html'
    image_url='https://www.codanalytics.net/static/main/image/ittraining.jpg'
    image_url2='https://www.codanalytics.net/static/main/image/interviews.png'
    image_url3='https://www.codanalytics.net/static/main/image/jobsupport.jpg'
    
    message = (
        f'Hi {request.user.first_name}, Your message was successfully sent. To confirm, please check '
        f'sent mails of finance@codanalytics.net. Thank You.'
    )

    error_message=f'Hi,{request.user.first_name}, there seems to be an issue on our end.kindly contact us directly for payment details.'
    context_data = 'services(request)'
    # users_to_email = User.objects.filter(is_staff=True,is_active=True,is_superuser=True)
    users_to_email = User.objects.all()
    plans = context_data.get('plans')
    pricing_info = context_data.get('pricing_info')
    start_date,end_date='get_15th_of_next_month()'

    context={
                "SITEURL": settings.SITEURL,
                "purpose": "marketing",
                "title": subject,
                'title2': title2,
                'services': pricing_info,
                # 'courses':courses,
                'message':message,
                'error_message':error_message,
                'image_url':image_url,
                'image_url2':image_url2,
                'image_url3':image_url3,
                'start_date':start_date,
                'end_date':end_date,
            }
    try:
        # Send email to each user in the selected category
        for user in users_to_email:
            context['user'] = user.first_name
            send_email(
                category=user.category,  
                to_email=[user.email],
                subject=subject,
                html_template=url,
                context=context
            )
        return render(request, 'main/messages/message.html', context)
        # return render(request, url, context)
    except Exception as e:
        error_message = (
            f'Hi {request.user.first_name}, Your message was unsuccessful. '
            f'Please try again or contact info@codanalytics.net. Thank You. '
            f'Error: {e}'
        )
        return render(request, 'main/messages/message.html', {"message": error_message})