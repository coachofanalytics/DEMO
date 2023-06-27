import os,requests,openai
import random,string
from django.views.generic import DeleteView, ListView, TemplateView, UpdateView
from accounts.forms import UserForm
from django.http import HttpResponseRedirect, Http404, JsonResponse,HttpResponse
from accounts.models import CustomerUser
from coda_project.settings import SITEURL
import datetime
from django.utils.text import slugify
# from main.models import Assets
# from yourapp.utils import random_string_generator

from django import template

register = template.Library()

@register.filter
def convert_date(date_string):
    return datetime.strptime(date_string, "%m/%d/%Y").date()



def random_string_generator(size=25, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance 
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        try:
            slug = slugify(instance.title)
        except:
            slug = slugify(instance.name)
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=10)
                )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug



def buildmodel(question):
    #fetching api key 
    # https://platform.openai.com/account/api-keys
    # 
    openai.api_key = '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'

    # openai.api_key = os.environ.get('OPENAI_API_KEY')
    print(openai.api_key)

    #Building engine
    request = openai.Completion.create(
        model="text-davinci-001",
        prompt=question,
        temperature=0.4,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    res = request["choices"][0]
    print(res['text'])
    result=res['text']
    return result


def countdown_in_month():
    now = datetime.datetime.now()
    next_month = now.replace(day=28) + datetime.timedelta(days=4)
    next_month = next_month.replace(day=1)

    remaining_time = next_month - now
    remaining_days = remaining_time.days
    remaining_seconds = remaining_time.total_seconds()
    remaining_minutes = remaining_seconds / 60
    remaining_hours = remaining_minutes / 60
    return (
                remaining_days,
                remaining_seconds ,
                remaining_minutes ,
                remaining_hours 
            )

def path_values(request):
    value=request.path.split("/")
    path_values = [i for i in value if i.strip()]
    sub_title=path_values[-1]
    return path_values,sub_title

#===============Downloading Image==================
def download_image(url):
    # Path definition
    image_path = "media/data/image.jpg"
    res = requests.get(url, stream=True)
    if res.status_code == 200:
        with open(image_path, "wb") as f:
            f.write(res.content)
        # print("Image sucessfully Downloaded: ", image_path)
    else:
        print("Image Couldn't be retrieved")
    return image_path

# def image_view(images):
#     images= Assets.objects.all()
#     images= images
#     image_names=Assets.objects.values_list('name',flat=True)
#     return images,image_names



# Interview description data
posts = [
    {
        "Inteview": "First   Interview",
        "Concentration": "Data Analysis",
        "Description": "Understanding SQL,Tableau & Alteryx	",
        "Duration": "5 Days	",
        "Lead": "HR Manager",
    },
    {
        "Inteview": "Second Interview",
        "Concentration": "General Tools& Company Projects",
        "Description": "Understanding Company Projects, Values & Systems	",
        "Duration": "5 Days	",
        "Lead": "HR Manager",
    },
    {
        "Inteview": "Final Interview",
        "Concentration": "Data Analysis 1-1 Sessions",
        "Description": "Measuring,assessing Time sensitivity.",
        "Duration": "7 Days",
        "Lead": "Scrum Master",
    },
]

alteryx_list = [
    {
        "topic": "INSTALLATION",
        "description": "Installing Alteryx",
        "link": "https://docs.google.com/presentation/d/1sTflaF0yS8nYS4Trm9gx0H4HPH0zN7qBu9O27-vMN7A/edit#slide=id.p1",
    },
    {
        "topic": "DAF DATA CLEANING",
        "description": "DAF data cleaning workflow",
        "link": "https://transcripts.gotomeeting.com/#/s/ff2b23e11fadead1e6b4265b043f75ec8300a82d9576d7e6f79ae22568733740",
    },
    {
        "topic": "WHATSAAP MESSAGES",
        "description": "Cleaning Messages",
        "link": "https://transcripts.gotomeeting.com/#/s/8085611d7f07db4434d786635018273ad915c01230fd33202f660fe4c1fd62d5",
    },
    {
        "topic": "ALTERYX PPT",
        "description": "Use the powerpoint to follow along, you will use the same ppt in presenting your work",
        "link": "https://docs.google.com/presentation/d/1v68aYsEXskx0Ze6CEbM9k8HLjMlgHY5ZOOScsGO7j54/edit#slide=id.p1",
    },
]

dba_list = [
    {
        "topic": "INSTALLATION",
        "description": "Installing SQL Database",
        "link": "https://drive.google.com/file/d/148J8xhikG5CqroObDjUtNC3r7vk9HmxF/view?usp=drivesdk",
    },
    {
        "topic": "End to End-SQL",
        "description": "Normalization, Creation and Retrieval of Data",
        "link": "https://transcripts.gotomeeting.com/#/s/ee09457a8bec84b6e27fd0a24bb8e2bdf9186c30b88a1ef48171b2f443e61635",
    },
    {
        "topic": "SQL PPT",
        "description": "Use the powerpoint to follow along, you will use the same ppt in presenting your work",
        "link": "https://docs.google.com/presentation/d/13IQKwFjkkxJckPQWG-Q1ydZPv6tDfhpWUOt6j9mNgvQ/edit",
    },
]

tableau_list = [
    {
        "topic": "INSTALLATION",
        "description": "Installing Tableau",
        "link": "https://www.youtube.com/watch?v=QYnkudCxbmE",
    },
    {
        "topic": "Reporting",
        "description": "Developing an Executive Overview Report",
        "link": "https://drive.google.com/file/d/1yQBiDgt3y1faTfglDtVITEEnyyYIewui/view",
    },
    {
        "topic": "Tableau PPT",
        "description": "Use the powerpoint to follow along, you will use the same ppt in presenting your work",
        "link": "https://docs.google.com/presentation/d/1ASZkzSJBSoOqH6R83ZznChL6ISi5SC5_YI5N2XTZD1w/edit?usp=sharing",
    },
]


# ==============================INTERVIEW DESCRIPTION MODELS=======================================

# Interview description data

TaskInfos = [
    {
        "Inteview": "First   Interview",
        "Concentration": "Data Analysis",
        "Description": "Understanding SQL,Tableau & Alteryx	",
        "Duration": "5 Days	",
        "Lead": "HR Manager",
    },
    {
        "Inteview": "Second Interview",
        "Concentration": "General Tools& Company Projects",
        "Description": "Understanding Company Projects, Values & Systems	",
        "Duration": "5 Days	",
        "Lead": "HR Manager",
    },
    {
        "Inteview": "Final Interview",
        "Concentration": "Data Analysis 1-1 Sessions",
        "Description": "Measuring,assessing Time sensitivity.",
        "Duration": "7 Days",
        "Lead": "Scrum Master",
    },
]


# Interview description data

data_interview = [
    {
        "Inteview": "1. Transcripts",
        # "Concentration": "Data Analysis",
        "Description": "Write Your Responses to 8 Topics",
        "Duration": "5 Days/3 Runs",
        "Lead": "Self/Coach",
        "Link": SITEURL+"/data/iuploads/",
    },
    
    {
        "Inteview": "2. Practice Sessions",
        # "Concentration": "General Tools& Company Projects",
        "Description": "Self recorded practice sessions for all 8 questions",
        "Duration": "5 Days/24 sessions",
        "Lead": "Self/Coach",
        "Link": SITEURL+"/management/sessions",
    },
    {
        "Inteview": "3. Role-Concentration",
        "Description": "Interact with a database of 80 Technical Interview Questions",
        "Duration": "5 Days	",
        "Lead": "Self/Coach",
        "Link": SITEURL+"/data/prepquestions/",
    },
    {
        "Inteview": "4. Mock Interviews",
        # "Concentration": "Data Analysis 1-1 Sessions",
        "Description": "Real Life simulation of mock interview with coach of analytics",
        "Duration": "2 Mock/4 Past Interviews",
        "Lead": "Coach",
        "Link": "https://drive.google.com/file/d/1-R6R-CyHNo6b-MIN33wYwWfsDQP1NB1L/view",
    },
    {
        "Inteview": "5. Job Application & Salary Negotiation",
        # "Concentration": "Data Analysis 1-1 Sessions",
        "Description": "Guide you on how to apply and respond to recruiters",
        "Duration": "14 Days",
        "Lead": "self/Coach",
        "Link": SITEURL+"/data/job_market/",
    },
]

Automation = [
    {
        "title": "Social Media",
        "link":SITEURL+"/marketing/",
        "linkname":"Pics&Messages-Whatsapp",
    },
    {
        "title": "Cash App",
        "link":SITEURL+"/getdata/cashappdata/",
        "linkname":"Cash app",
    },
    {
        "title": "Job Application",
        "link":SITEURL+"/getdata/replies/",
        "linkname":"Reply",
    },
    {
        "title": "ChatGPT",
        "link":"https://chat.openai.com/chat",
        "linkname":"CHATGPT",
    },
]
Stocks = [
    {
        "title": "Cryptomarket",
        "link":SITEURL+"/investing/options/",
        "linkname":"Cryptomarket Data",
    },
    {
        "title": "Credit Spreads",
        "link":SITEURL+"/investing/credit_spread/",
        "linkname":"Credit Spreads Data",
    },
    {
        "title": "Get short Put Data",
        "link":SITEURL+"/investing/shortputdata/",
        "linkname":"Get short Put Data",
    },
    {
        "title": "Get covered Calls Data",
        "link":SITEURL+"/investing/covered_calls/",
        "linkname":"Get covered Calls Data",
    },
]
General = [
    {
        "title": "Images/Assets",
        "link":SITEURL+"/images/",
        "linkname":"Add Images/Assets",
    },
    {
        "title": "Credit Spreads",
        "link":SITEURL+"/investing/credit_spread/",
        "linkname":"Credit Spreads Data",
    },
    {
        "title": "Get short Put Data",
        "link":SITEURL+"/investing/shortput/",
        "linkname":"Get short Put Data",
    },
    {
        "title": "Get covered Calls Data",
        "link":SITEURL+"/investing/covered_calls/",
        "linkname":"Get covered Calls Data",
    },
]
Meetings = [
    {
        "title": "1-1 Session",
        "link":"https://docs.google.com/presentation/d/1NkgvW-ruCwCQTlkO9af75kUdKBGF9Vem/edit#slide=id.p1",
        "linkname":"1-1 Session",
        "video":"https://drive.google.com/file/d/1g0Esp33N6xR3pn7Z9-76yYxS3m_81HWH/view?usp=share_link",
    },

    {
        "title": "General Meeting",
        "link":SITEURL+"/management/companyagenda/",
        "linkname":"General Meeting",
        "video":"https://transcripts.gotomeeting.com/#/s/085feaf847fb42db28a68d5d507b871d4bed978d767e837ad3dfb2e473a57e41",

    },
    {
        "title": "BI Session",
        "link":SITEURL+"/management/companyagenda/",
        "linkname":"BI Session",
        "video":"https://transcripts.gotomeeting.com/#/s/47f94d4d116bd8d2214eea00edc483d9289915496671f9b7c82eda5512634846",
    },
    {
        "title": "SPRINT",
        "link":"https://docs.google.com/spreadsheets/u/5/d/1ILex8zOkh4Vee1dDabIadQTmmoyScaybucUiQirDfFI/edit#gid=1358242624",
        "linkname":"SPRINT",
        "video":"https://transcripts.gotomeeting.com/#/s/1ffa25cf84e5fc1b531df945fa358990166ef871f7c7854402876d22d619bf59",
    },
    {
        "title": "DAF SESSIONS",
        "link":"https://drive.google.com/file/d/1UsSmmJv5_83ZRegObGhgGE3C5eIJ-4E1/view",
        "linkname":"DAF",
        "video":"https://transcripts.gotomeeting.com/#/s/d88210a7703467f606586da252e8cb8349de7dc74e1e4cdec2a74307131985d5",
    },
    {
        "title": "DEPARTMENT",
        "link":SITEURL+"/management/companyagenda/",
        "linkname":"departmental",
        "video":"#",
    },
    {
        "title": "BOG",
        "link":"https://docs.google.com/spreadsheets/d/1wTiUJnhzfJWCw_i5XgH531LvzDhytoLRrU0fwSij88w/edit#gid=1239081146",
        "linkname":"BOG",
        "video":"#",
    },
    {
        "title": "PBR",
        "link":"https://docs.google.com/spreadsheets/d/18D2D0jr5MRGovoDJpfTkks4JxgU32w5x/edit#gid=1089504823",
        "linkname":"PBR",
        "video":"https://drive.google.com/file/d/1hDMaa9b-sjbsHGy7n4upseNdiKnSvAL-/view?usp=sharing",
    },
]

# Big_data = [
#     {
#      "Automation":{
#         "title": "1. Transcripts",
#        "link": "SITEURL+"/data/iuploads/",
#     },
#     "Stocks&Options":{
#         "title": "1. Transcripts",
#        "link": "SITEURL+"/data/iuploads/",
#     },
#     }
# ]
# ==============================Apps and Models===============================
Finance = [
    {
        "title": " Transaction",
        "description": " Upload only a CSV File, Check field formats to minimize errors during upload.",
    },
    {
        "title": " Payment Information",
        "description": " Upload only a CSV File, Check field formats to minimize errors during upload.",
    },
    {
        "title": "Payment History",
        "description": " Upload only a CSV File, Check field formats to minimize errors during upload.",
    },
]
Data = [
    {
        "title": " Categrory",
        "description": " Upload only a CSV File, Check field formats to minimize errors during upload.",
    },
    {
        "title": " SubCategory",
        "description": " Upload only a CSV File, Check field formats to minimize errors during upload.",
    },
    {
        "title": "Links",
        "description": " Upload only a CSV File, Check field formats to minimize errors during upload.",
    },
]
Management = [
    {
        "title": " Task",
        "description": " Upload only a CSV File, Check field formats to minimize errors during upload.",
    },
    {
        "title": " Task History",
        "description": " Upload only a CSV File, Check field formats to minimize errors during upload.",
    },
    {
        "title": "Other",
        "description": " Upload only a CSV File, Check field formats to minimize errors during upload.",
    },
]





#import pdfkit

# def convert_html_to_pdf():
#     html="main/doc_templates/appointment_letter.html"
#     html_str=str(html)
#     pdfkit.from_string(html_str, 'appointment_letter.pdf')
#     print("success")

# def convert_html_to_pdf():
#     html_path = "main/doc_templates/appointment_letter.html"
#     pdf_path = "appointment_letter.pdf"
#     pdfkit.from_file(html_path, pdf_path)
#     print("Success: HTML converted to PDF.")

# def convert_html_to_pdf(request):
#     html_path = "main/doc_templates/letter.html"
#     pdf_path = "appointment_letter.pdf"
#     pdfkit.from_file(html_path, pdf_path)
#     with open(pdf_path, 'rb') as pdf_file:
#         response = HttpResponse(pdf_file.read(), content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename="appointment_letter.pdf"'
#         return response