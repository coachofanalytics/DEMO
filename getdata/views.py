# imports added below
import json
import os
import requests
from requests import request 
import threading
import time

from re import M
from django import forms
from django.shortcuts import get_object_or_404, redirect, render
from datetime import datetime,date
from http.client import HTTPResponse
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.views import View
from django.utils.dateformat import format
from django.contrib import admin, messages
from . import forms
from django.urls import path, reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.views.generic import (
	CreateView,
	ListView,
	UpdateView,
	DetailView,
	DeleteView, 
    FormView
)
from main.utils import Finance,Data,Management
from getdata.utils import (
                    get_gmail_service,
                    search_messages,
                    get_message,
                    getdata,
                    GetSubject,
                    get_executed_info

)
from finance.models import (
        Transaction
	)
from .models import CashappMail,stockmarket
from django.contrib.auth import get_user_model

from .forms import CsvImportForm

# User=settings.AUTH_USER_MODEL
User = get_user_model()

# top level variables declaration
# views on ratings data.
def getrating(request):
    return render(request, 'getdata/getrating.html', {'title': 'getrating'})

def index(request):
    return render(request, 'getdata/index.html', {'title': 'index'})

def show(request):  
    employees = Employee.objects.all()  
    return render(request,"accounts/show.html",{'employees':employees})  

def uploaddata(request):  
    # context = {"posts": posts}
    context = {
        "Finance": Finance,
        "Data": Data,
        "Management": Management,
    }
    return render(request,"getdata/uploaddata.html", context) 



# ========================. DISPLAY/LIST VIEWS============================
# class CashappListView(ListView):
#     queryset = CashappMail.objects.all()
#     template_name = "main/snippets_templates/interview_snippets/result.html"

class CashappListView(ListView):
	model = CashappMail
	template_name = "main/snippets_templates/interview_snippets/result.html"
	context_object_name = "cashappdata"
# # ==================GOTOMEETING===========================
# dir_path = os.path.dirname(os.path.realpath(__file__))
# print('---dir_path-- : ',dir_path)
# urlGotoMeeting = "https://api.getgo.com/G2M/rest/historicalMeetings?startDate={}&endDate={}"
# urlToRefresh = 'https://api.getgo.com/oauth/v2/token'
# urlMeetingAttendee = "https://api.getgo.com/G2M/rest/meetings/{}/attendees"
# grant_type = 'refresh_token'
# refresh_token = None
# client_code = None

# # -----

# def refresh_token_function():
#     global refresh_token , client_code

#     # myRefreshJSON =None
#     # print('1. reading client code and refresh token')

#     with open(dir_path+'/gotomeeting/credentialsForRefresh.json','r') as f:
#         myJson = json.load(f)
#         refresh_token = myJson['refresh_token']
#         client_code = myJson['client_code']
#     response = None
#     headers = {
#     'Content-Type': 'application/x-www-form-urlencoded',
#     'Authorization': 'Basic '+client_code
#     }
#     myPayload = "grant_type={}&refresh_token={}".format(grant_type , refresh_token)

#     # print('2. making refresh token request to',urlToRefresh)

#     response = requests.post(url=urlToRefresh , data=myPayload , headers=headers)
#     # print('3. response-code: ',response.status_code)
#     # print("4. saving new tokens in file")
#     with open(dir_path+'/gotomeeting/refresh_tokens.json',"w") as f:
#         f.write(response.text)
#         # print("written to ",'refresh_tokens.json')
    
#     # print('\n---------------done-----------------')

#     ## refreshing tokens every 30 minutes
#     threading.Timer(1800.0, refresh_token_function).start()
#     print("--refreshing tokens at {}--".format(time.ctime()))

# refresh_token_function()

# # method to get meeting response from gotomeeting api


# def getmeetingresponse(startDate , endDate):
#     access_token = None
#     print('-'*50)
#     # print("1. getting access tokens")
#     with open(dir_path+'/gotomeeting/refresh_tokens.json','r') as f:
#         myJson = json.load(f)
#         access_token = myJson['access_token']
#     response = None
#     headers = {
#     'Authorization': 'Bearer '+access_token
#     }
#     # print("2. getting meetings from {} to {}\n".format(startDate , endDate))
#     urlMeeting = urlGotoMeeting.format(''.join([str(startDate),'T12:00:00Z']) ,''.join([str(endDate),'T12:00:00Z']))
#     # print("3. request made : ",urlMeeting)
#     response = requests.request("GET" , url=urlMeeting , headers=headers)
#     # print('4.  response-code: ',response.status_code)
#     # print('5.  rendering with variable data')
#     print('-'*50)
#     # return [response.text]
#     jsonResponse = json.loads(response.text)
#     myCleanResponse = []
#     for meeting in jsonResponse:
#         temp = {}
#         meetingItems = meeting.items()
#         temp.update(meetingItems)
#         if 'recording' in temp.keys():
#             temp['recording'] = temp['recording']['shareUrl']
#             # print('added rec link')
#         else:
#             temp['recording'] = "No recording"

#         temp['startTime'] = temp['startTime'].replace('T',' ')
#         temp['endTime'] = temp['endTime'].replace('T',' ')

#         temp['startTime'] = temp['startTime'].replace('.+0000','')
#         temp['endTime'] = temp['endTime'].replace('.+0000','')
#         myCleanResponse.append(temp)

#     return myCleanResponse








# ''' for gotomeeting data '''
# # starts here ----------

# def meetingFormView(request):
#     # testing purpose hardcoding allDataJsons
#     allDataJsons = []
#     # print('1->',request.POST)
#     # print('2->',request.POST.mycity)
#     if request.method=='POST':
#         print('here')
#         print('1->',request.POST)
#         startDate = request.POST['startDate']
#         endDate = request.POST['endDate']
#         # print('2->',request.POST['startDate'])
#         # print('3->',request.POST['endDate'])
#         allDataJsons = []
#         # filePath = dir_path+"/gotomeeting/meetings_2.json"
#         allDataJsons = getmeetingresponse(startDate , endDate)
#         result = {
#             'data' : allDataJsons,
#             'message' : "meetings between {} and {}".format( startDate , endDate)
#         }
#         # print('5-> result : ',result)

#         return render(request, 'getdata/meetingList.html',result) #returns the index.html template

#     return render(request, 'getdata/meetingForm.html') #returns the index.html template

# def gotomeetingresult(request):
#     print('you are here at ',request.path)
#     # print('result - \n',result)
#     return render(request, 'getdata/meetingList.html') #returns the index.html template


# # ends here --------

# ## additions to view gotomeeting meeting in detail

# # meetingView6
# def meetingView6(request,meeting_id):
#     print("\n\n view6 : you have request meeting details for path  : ",request.path)
#     mID = int(meeting_id)
#     with open(dir_path+'/gotomeeting/refresh_tokens.json','r') as f:
#         myJson = json.load(f)
#         access_token = myJson['access_token']
#     strResponse = None
#     headers = {
#     'Authorization': 'Bearer '+access_token
#     }
#     meeting = urlMeetingAttendee.format(mID)
#     print(f"fetching meeting {mID} details ->> {meeting} ")

#     responseMeeting = requests.get(url=meeting,headers=headers)
#     jsonResp = json.loads(responseMeeting.text)
#     # print("-->> foo : ",foo)
#     template_name = 'getdata/meetingDetails.html'
#     # context_object_name = 'result'
#     result = {"data":'meeting details id = {}'.format(meeting_id)}
#     # myQuerySet = meetingView3.get_queryset()
#     # {{ request.GET.urlencode }}
#     cleanResponse = []
#     for meeting in jsonResp:
#         temp = {}
#         meetingItems = meeting.items()
#         temp.update(meetingItems)
#         temp['joinTime'] = temp['joinTime'].replace('T',' ')
#         temp['leaveTime'] = temp['leaveTime'].replace('T',' ')

#         cleanResponse.append(temp)

#     result['info'] = cleanResponse

#     return render(request , template_name , result)

# ========================================UPLOADING DATA SECTION========================


	
# def get_urls(self):
#     urls = super().get_urls()
#     new_urls = [
#         path("upload-csv/", self.upload_csv),
#     ]
#     return new_urls + urls

def upload_csv(request):

    if request.method == "POST":
        csv_file = request.FILES["csv_upload"]

        if not csv_file.name.endswith(".csv"):
            messages.warning(
                request, "The wrong file type was uploaded, it should be a csv file"
            )
            return render(request, "getdata/uploaddata.html")
            # return HttpResponseRedirect(request.path_info)

        # file= csv_file.read().decode("utf-8")
        file = csv_file.read().decode("ISO-8859-1")
        file_data = file.split("\n")
        csv_data = [line for line in file_data if line.strip() != ""]
        print(csv_data)
        for x in csv_data:
            fields = x.split(",")
            created = Transaction.objects.update_or_create(
                activity_date=fields[0],
                sender=fields[1],
                receiver=fields[2],
                phone=fields[3],
                qty=fields[4],
                amount=fields[5],
                payment_method=fields[6],
                department=fields[7],
                category=fields[8],
                type=fields[9],
                description=fields[10],
                receipt_link=fields[11],
            )
        url = reverse("main:layout")
        return HttpResponseRedirect(url)
    form = CsvImportForm()
    data = {"form": form}
    # return render(request, "admin/csv_upload.html", data)
    return render(request, "getdata/uploaddata.html", data)


def options(request):
    service = get_gmail_service()
    messages = search_messages(service= service, query= 'Robinhood')
    for message in messages[:100]:
        msg_id = message['id']
        print(msg_id)
        data = get_message(service=service, msg_id=msg_id)
        soup = getdata(data)
        if soup == 0:
            continue
        try:
            subjectname = GetSubject(soup)
            if subjectname == None:
                continue
        except:
            continue

        if subjectname == 'Option Order Executed':
            get_executed_info(soup, subjectname)
            os.remove(data)
        else:
            os.remove(data)
        # return render(request, "getdata\options.html")
        return redirect("getdata:stockmarket")

class OptionList(ListView):
    model=stockmarket
    template_name="getdata\options.html"
    context_object_name = "stocks"

