# imports added below
import os
import json
import requests
from django.http import JsonResponse
from selenium import webdriver
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect, Http404, JsonResponse,HttpResponse,HttpResponseBadRequest
from django.contrib import admin, messages
from django.urls import path, reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import (
	ListView,
	DetailView,
)
from main.utils import App_Categories,Automation,Stocks,General,path_values,convert_date
from getdata.utils import (
					fetch_and_insert_data,populate_table_from_json_file
)
from finance.models import (Transaction, Payment_History)

from investing.models import OverBoughtSold
from marketing.models import Whatsapp_Groups
from main.models import ServiceCategory

#importing Options play funcationality

from .models import CashappMail,ReplyMail,GotoMeetings,Logs
from django.contrib.auth import get_user_model
from .forms import CsvImportForm
from coda_project.settings import EMAIL_INFO,source_target

# User=settings.AUTH_USER_MODEL
User = get_user_model()
__smtp_user = EMAIL_INFO


# top level variables declaration
# views on ratings data.
def index(request):
	return render(request, 'getdata/index.html', {'title': 'index'})

def getrating(request):
    return render(request, 'getdata/getrating.html', {'title': 'getrating'})

@login_required
def fetch_whatsapp_groups(request):
    file_path='media/marketing/whatsapp_groups/Whatsapp_Groups_11232023_v1.txt'
    populate_table_from_json_file(file_path)
    # context={
    #     'title': 'Fetching Whatsapp Groups From Text File',
    #     'message':'We are done populating your database table'
    # }
    # return render(request, "main/errors/generalerrors.html", context)
    return redirect('marketing:whatsapp_list')
	

def uploaddata(request):  
	# context = {"posts": posts}
	context = {
        "App_Categories": App_Categories,
	}
	return render(request,"getdata/uploaddata.html", context) 

def update_link(service_array, user_payment_history, service_categories):
	updated_automation = []
	for automation_service in service_array:
		
		if automation_service['service_category_slug'] and automation_service['service_category_slug'] in service_categories.keys():

			# import pdb; pdb.set_trace()
			if user_payment_history.filter(plan = service_categories[automation_service['service_category_slug']]).exists():
				
				updated_automation.append(automation_service)	
			
			else:

				automation_service['link'] = automation_service['service_url']
				updated_automation.append(automation_service)
			
		else:
			updated_automation.append(automation_service)
	return updated_automation

@login_required
def bigdata(request):
	if request.user.category != 2:
		payment_history = Payment_History.objects.filter(customer_id=request.user)
		service_categories = dict(ServiceCategory.objects.values_list('slug', 'id'))

		context={
			"title":  "data",
			"Automation": update_link(Automation, payment_history, service_categories),
			"Stocks":Stocks,
			"General":update_link(General	, payment_history, service_categories),
		}
	else:
		context={
			"title": "data",
			"Automation":Automation,
			"Stocks":Stocks,
			"General":General,
		}
		
	return render(request, "getdata/bigdata.html",context)


# ========================. DISPLAY/LIST VIEWS============================
# class CashappListView(ListView):
#     queryset = CashappMail.objects.all()
#     template_name = "main/snippets_templates/interview_snippets/result.html"

class CashappListView(ListView):
	model = CashappMail
	template_name = "main/snippets_templates/interview_snippets/result.html"
	context_object_name = "cashappdata"

class CashappMailDetailSlugView(DetailView):
	queryset = CashappMail.objects.all()
	template_name = "getdata/detail.html"
 
	def get_context_data(self, *args, **kwargs):
		context = super(CashappMailDetailSlugView, self).get_context_data(*args, **kwargs)
		return context
 
	def get_object(self, *args, **kwargs):
		request = self.request
		slug = self.kwargs.get('slug')
 
		#instance = get_object_or_404(CashappMail, slug=slug, active=True)
		try:
			instance = CashappMail.objects.get(slug=slug, active=True)
		except CashappMail.DoesNotExist:
			raise Http404("Not found..")
		except CashappMail.MultipleObjectsReturned:
			qs = CashappMail.objects.filter(slug=slug, active=True)
			instance = qs.first()
		except:
			raise Http404("Uhhmmm ")
		return instance

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

from django.shortcuts import redirect


# def initiate_oauth(request):
#     # Your application's configuration
#     CLIENT_ID = os.environ.get('GOTO_CLIENT_ID')
#     REDIRECT_URI = "https://www.codanalytics.net/"

#     # Generate the authorization URL dynamically
#     auth_url = f"https://api.getgo.com/oauth/v2/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}"

#     # Redirect the user to the GoToMeeting's OAuth2 page
#     return redirect(auth_url)
@login_required
def initiate_oauth(request):
	# Your application's configuration
	CLIENT_ID = 'a75f876d-cb58-404c-b5c0-4e91d9bc4052' # os.environ.get('GOTO_CLIENT_ID')
	REDIRECT_URI =  "http://localhost:8000/getdata/obtain_tokens/"

	# Generate the authorization URL dynamically
	auth_url = f"https://api.getgo.com/oauth/v2/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}"

	# Redirect the user to the GoToMeeting's OAuth2 page
	return redirect(auth_url)

@login_required
def obtain_tokens(request):
	# Obtain the authorization code from the request parameters
	code = request.GET.get('code')
	# code='eyJraWQiOiI2MjAiLCJhbGciOiJSUzUxMiJ9.eyJzYyI6ImNhbGwtY29udHJvbC52MS5jYWxscy5jb250cm9sIGNhbGxzLnYyLmluaXRpYXRlIGNvbGxhYjogY3IudjEucmVhZCBmYXgudjEubm90aWZpY2F0aW9ucy5tYW5hZ2UgZmF4LnYxLnJlYWQgZmF4LnYxLndyaXRlIGlkZW50aXR5OiBpZGVudGl0eTpzY2ltLm9yZyBtZXNzYWdpbmcudjEubm90aWZpY2F0aW9ucy5tYW5hZ2UgbWVzc2FnaW5nLnYxLnJlYWQgbWVzc2FnaW5nLnYxLnNlbmQgbWVzc2FnaW5nLnYxLndyaXRlIHJlYWx0aW1lLnYyLm5vdGlmaWNhdGlvbnMubWFuYWdlIHN1cHBvcnQ6IHVzZXJzLnYxLmxpbmVzLnJlYWQgd2VicnRjLnYxLnJlYWQgd2VicnRjLnYxLndyaXRlIiwic3ViIjoiMTA1MzgxODUyNTQ4NTQ2NDU5MCIsImF1ZCI6ImE3NWY4NzZkLWNiNTgtNDA0Yy1iNWMwLTRlOTFkOWJjNDA1MiIsIm9nbiI6InB3ZCIsImxzIjoiMTA3NjgwNDItYzI2Ny00NjcxLWE2MGMtZmVhYTk1ODcyYTAxIiwidHlwIjoiYyIsImV4cCI6MTY5Mzg4OTU0MSwiaWF0IjoxNjkzODg4OTQxLCJ1cmkiOiJodHRwczpcL1wvd3d3LmNvZGFuYWx5dGljcy5uZXRcLyIsImp0aSI6IjNjYTEzMDZjLTQ4YmEtNGE4My1hODNlLTY3ZDc3ZTIxODMxMyJ9.a7I6bRkafGA7cfr4Del0tc4IHErFCUp2D2E_zjd9aq-9sEek8GIiK0FH2W7eDg0SB5sL-Tet-KlEutK7Jw1zWTXKHZgGHeURfx3JNXdvmpYGI1XBZiNEALbXC8X-kB1njfMdpnSJbUonQ0qYRcbqzlIfIeaCFm3tnSujn0QvK9DbzGUDWfZDT5_xxRRQEl-B06VKU9CZ_hrsh2GEyEVVQ5SuUZlq8Nxivkp7phSt5ErMpYBjvd1POZ8JTCkucylQA3tWo7531AYES4ZpQM5BJ51S2XtmTLYqr1o5mS-xVdxI27LwLeBBHJeHA3xp39DvW5C2rbmygCOHAMCPY3UHew'
	# code = os.environ.get('GOTO_CLIENT_CODE')
	# print("code======>",code)
	
	if not code:
		return HttpResponseBadRequest("Missing code parameter")

	# Your application's configuration
	CLIENT_ID = 'a75f876d-cb58-404c-b5c0-4e91d9bc4052' #os.environ.get('GOTO_CLIENT_ID')
	CLIENT_SECRET ='ykEQJ5Rd8xx8sPOD1W5KTJnO' #os.environ.get('GOTO_SECRET_KEY')
	REDIRECT_URI = "http://localhost:8000/getdata/obtain_tokens/" #os.environ.get('CODA_REDIRECT_URI')

	# Payload for the token request
	payload = {
		'grant_type': 'authorization_code',
		'client_id': CLIENT_ID,
		'client_secret': CLIENT_SECRET,
		'code': code,
		'redirect_uri': REDIRECT_URI
	}

	# Make the token request
	response = requests.post('https://api.getgo.com/oauth/v2/token', data=payload)
	# print("status======>",response.status_code)
	# Error handling for the HTTP request

	if response.status_code != 200:
		return HttpResponseBadRequest(f"Error obtaining tokens: {response.text}")


	tokens = response.json()
	refresh_token = tokens.get('refresh_token')

	# Return the refresh token as a JsonResponse, or you can save it, etc.
	return JsonResponse({"refresh_token": refresh_token})

@login_required
def refresh_token_function(request):
	global refresh_token , client_code

	# myRefreshJSON =None
	# print('1. reading client code and refresh token')

	# to get the current working directory
	dir_path = str(os.getcwd())

	with open(dir_path+'/getdata/gotomeeting/credentialsForRefresh.json','r') as f:
		myJson = json.load(f)
		refresh_token = myJson['refresh_token']
		client_code = myJson['client_code']
	response = None
	headers = {
	'Content-Type': 'application/x-www-form-urlencoded',
	'Authorization': 'Basic '+client_code
	}

	myPayload = "grant_type={}&refresh_token={}".format('refresh_token' , refresh_token)

	# print('2. making refresh token request to',urlToRefresh)
	response = requests.post(url='https://authentication.logmeininc.com/oauth/token' , data=myPayload , headers=headers)
	# print('3. response-code: ',response.status_code)
	# print("4. saving new tokens in file")
	with open(dir_path+'/getdata/gotomeeting/refresh_tokens.json',"w") as f:
		f.write(response.text)
		# print("written to ",'refresh_tokens.json')
	
	# print('\n---------------done-----------------')



	## refreshing tokens every 30 minutes
	# threading.Timer(1800.0, refresh_token_function).start()
	# print("--refreshing tokens at {}--".format(time.ctime()))

	return HttpResponse("token saved successfully")


@login_required
def getmeetingresponse(startDate , endDate):
	access_token = None
	startDateTime="{}T00:00:00Z".format(startDate)
	endDateTime="{}T23:59:00Z".format(endDate)
	print('-'*50)
	dir_path = str(os.getcwd())
	print(dir_path)
	# print("1. getting access tokens")
	with open(dir_path+'/getdata/gotomeeting/refresh_tokens.json','r') as f:
		myJson = json.load(f)
		access_token = myJson.get('access_token', None)
		if not access_token:
			# Handle the error: log it, raise an exception, or return an error response.
			print("Error: Missing access_token in refresh_tokens.json")
			return redirect('main:hendler500')
	response = None
	headers = {
	'Authorization': 'Bearer '+access_token
	}
	urlGotoMeeting = "https://api.getgo.com/G2M/rest/historicalMeetings?startDate={}&endDate={}"
	# print("2. getting meetings from {} to {}\n".format(startDate , endDate))
	from datetime import datetime
	from pytz import utc
	urlMeeting = urlGotoMeeting.format(startDateTime,endDateTime)

	# print("3. request made : ",urlMeeting)
	response = requests.request("GET" , url=urlMeeting , headers=headers)
	# print('4.  response-code: ',response.status_code)
	# print('5.  rendering with variable data')
	print('-'*50)
	jsonResponse = json.loads(response.text)
	myCleanResponse = []
	attendees1 = []
	for meeting in jsonResponse:
		# print("meetings============>",meeting)
		""" ======== Code For Get attendeeName ========="""
		meeting_id = meeting['meetingId']
		start_time = meeting['startTime']
		urlGotoOneMeetingDetail = f"https://api.getgo.com/G2M/rest/meetings/{meeting_id}/attendees"
		meetingresponse = requests.request("GET" , url=urlGotoOneMeetingDetail , headers=headers)
		attendees_response = json.loads(meetingresponse.text)
		attendee_names = [attendee.get("attendeeName") for attendee in attendees_response]
		
		""" =========== End of Code ============="""
		temp = {}
		meetingItems = meeting.items()
		temp.update(meetingItems)
		if 'recording' in temp.keys():
			temp['recording'] = temp.get('recording').get('shareUrl')
			# print('added rec link')
		else:
			temp['recording'] = "No recording"
		temp['meeting_email'] = temp.get('email')
		temp['startTime'] = temp.get('startTime').replace('T',' ')
		temp['endTime'] = temp.get('endTime').replace('T',' ')

		temp['startTime'] = temp.get('startTime').replace('.+0000','')
		temp['endTime'] = temp.get('endTime').replace('.+0000','')
		temp['attendeeNames'] = [attendee.get('attendeeName') for attendee in attendees_response 
								if attendee.get('startTime') == start_time[:19]] or None
		temp['attendee_Info'] = []
		for attendee in attendees_response:
			if attendee.get('startTime') == start_time[:19]:
				attendee_info = {
					"attendee_duration": attendee.get("duration"),
					"attendee_email": attendee.get("attendeeEmail"),
					"attendee_name": attendee.get("attendeeName")
				}
				temp['attendee_Info'].append(attendee_info)
		
		myCleanResponse.append(temp)
	# return HttpResponse(myCleanResponse)
	return myCleanResponse

	
# ''' for gotomeeting data '''

def save_meeting_data(meeting_data):
	for meeting_info in meeting_data:
		# Extract meeting information
		meeting_topic = meeting_info.get('subject', '')
		meeting_id = meeting_info.get('meetingId', '')
		meeting_type = meeting_info.get('meetingType', '')
		recording = meeting_info.get('recording', '')
		meeting_start_time = meeting_info.get('startTime', '')
		meeting_end_time = meeting_info.get('endTime', '')
		meeting_duration = int(meeting_info.get('duration', '0'))
		meeting_email = meeting_info.get('meeting_email', '')
		attendee_names = meeting_info.get('attendeeNames', [])
		attendee_info = meeting_info.get('attendee_Info', [])

		# Create a meeting record for each attendee
		for attendee_name, attendee_data in zip(attendee_names, attendee_info):
			attendee_email = attendee_data.get('attendee_email', '')
			attendee_duration = int(attendee_data.get('attendee_duration', '0'))

			# Create a new record for each attendee
			GotoMeetings.objects.create(
				meeting_topic=meeting_topic,
				meeting_id=meeting_id,
				meeting_type=meeting_type,
				recording=recording,
				meeting_start_time=meeting_start_time,
				meeting_end_time=meeting_end_time,
				meeting_duration=meeting_duration,
				meeting_email=meeting_email,
				attendee_name=attendee_name,
				attendee_email=attendee_email,
				attendee_duration=attendee_duration
			)
# # starts here ----------

def meetingFormView(request):
	# testing purpose hardcoding allDataJsons
	allDataJsons = []
	# print('1->',request.POST)
	# print('2->',request.POST.mycity)
	if request.method=='POST':
		print('here')
		print('1->',request.POST)
		startDate = request.POST['startDate']
		endDate = request.POST['endDate']
		# print('2->',request.POST['startDate'])
		# print('3->',request.POST['endDate'])
		allDataJsons = []
		# filePath = dir_path+"/gotomeeting/meetings_2.json"
		allDataJsons = getmeetingresponse(startDate , endDate)
		# save data in my model 
		print('allDataJsons++++++++++++',allDataJsons)
		save_meeting_obj = save_meeting_data(allDataJsons)
		result = {
			'data' : allDataJsons,
			'message' : "meetings between {} and {}".format( startDate , endDate)
		}
		# print('5-> result : ',result)

		return render(request, 'getdata/meetingList.html',result) #returns the index.html template

	return render(request, 'getdata/meetingForm.html') #returns the index.html template
	
	
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

#     with open(dir_path+'/gotomeeting/credentialsForRefresh.json', encoding='utf-8') as f:
#         myJson = json.load(f)
#         refresh_token = myJson['refresh_token']
#         client_code = myJson['client_code']
#     response = None
#     headers = {
#     'Content-Type': 'application/x-www-form-urlencoded',
#     'Authorization': 'Basic '+client_code
#     }
#     myPayload = "grant_type={}&refresh_token={}".format(grant_type , refresh_token)

#     print('2. making refresh token request to',urlToRefresh)

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
#     print("1. getting access tokens")
#     with open(dir_path+'/gotomeeting/refresh_tokens.json','r') as f:
#         myJson = json.load(f)
#         access_token = myJson['access_token']
#     response = None
#     headers = {
#     'Authorization': 'Bearer '+access_token
#     }
#     print("2. getting meetings from {} to {}\n".format(startDate , endDate))
#     urlMeeting = urlGotoMeeting.format(''.join([str(startDate),'T12:00:00Z']) ,''.join([str(endDate),'T12:00:00Z']))
#     print("3. request made : ",urlMeeting)
#     response = requests.request("GET" , url=urlMeeting , headers=headers)
#     print('4.  response-code: ',response.status_code)
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

	
def get_urls(self):
	urls = super().get_urls()
	new_urls = [
		path("upload-csv/", self.upload_csv),
	]
	return new_urls + urls


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
	return render(request, "getdata/uploaddata.html", data)


# from django.contrib import messages

def stocks_upload_csv(request):
	context = {
		"categories": App_Categories,
	}
	if request.method == "POST":
		# Retrieve the uploaded CSV file
		csv_file = request.FILES.get("csv_upload")

		# Check if it's a CSV file
		if not csv_file.name.endswith(".csv"):
			messages.warning(request, "Not a CSV file")
			return render(request, "getdata/uploaddata.html", context)
		try:
			# Read the CSV file
			file = csv_file.read().decode("ISO-8859-1")
			file_data = file.split("\n")
			csv_data = [line for line in file_data if line.strip() != ""]
		   
			# Create a set to store unique symbols
			unique_symbols = set()
			for x in csv_data:
				fields = x.split(",")
				symbol = fields[0]

				# Check if the symbol is unique
				if symbol not in unique_symbols:
					unique_symbols.add(symbol)

					# Create or update the record
					created = OverBoughtSold.objects.update_or_create(
							symbol=fields[0],
							description=fields[1],
							last=fields[2],
							volume=fields[3],
							RSI=fields[4],
							EPS=fields[5],
							PE=fields[6],
							rank=fields[7],
							profit_margins=fields[8],
					)

			messages.success(request, "Data populated successfully")
			return redirect('investing:overboughtsold',symbol=None )
		
		except Exception as e:
			messages.warning(request, str(e))
			return render(request, "getdata/uploaddata.html", context)

	if request.method == 'GET':
		return render(request, "getdata/uploaddata.html", context)
	
def groups_upload_csv(request):
    context = {
        "categories": App_Categories,
    }
    if request.method == "POST":
        # Retrieve the uploaded CSV file
        csv_file = request.FILES.get("csv_upload")

        # Check if it's a CSV file
        if not csv_file.name.endswith(".csv"):
            messages.warning(request, "Not a CSV file")
            return render(request, "getdata/uploaddata.html", context)
        try:
            # Read the CSV file
            file = csv_file.read().decode("ISO-8859-1")
            file_data = file.split("\n")
            csv_data = [line for line in file_data if line.strip() != " "]
            print(csv_data)
            
            # Create a set to store unique symbols
            unique_ids = set()
            for x in csv_data:
                print(x)
                fields = x.split(",")
                
                group_id = fields[0]

                # Check if the symbol is unique
                if group_id not in unique_ids:
                    unique_ids.add(group_id)
                    print(group_id)

                    # Create or update the record
                    created = Whatsapp_Groups.objects.update_or_create(
                            group_id=fields[0],
                            group_name=fields[1],
                            type=fields[2],
                    )

            messages.success(request, "Data populated successfully")
            return redirect('marketing:whatsapp_groups_list',id=None )
        
        except Exception as e:
            messages.warning(request, str(e))
            return render(request, "getdata/uploaddata.html", context)

    if request.method == 'GET':
        return render(request, "getdata/uploaddata.html", context)
	
def selinum_test(request):
	# to test on server
	chrome_options = webdriver.ChromeOptions()
	chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
	chrome_options.add_argument("--headless")
	chrome_options.add_argument("--disable-dev-shm-usage")
	chrome_options.add_argument("--no-sandbox")
	driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

	# Navigate to Google's homepage
	driver.get("https://www.google.com/")

	# Get the page title
	title = driver.title
	return HttpResponse(title)

def LogsViewSet(request):
	logs = Logs.objects.all().order_by("-id")
	if request.user.is_superuser:
		return render(request, "getdata/logs.html", {"logs": logs})
	else:
		return redirect("main:layout")
	

def refetch_data(request):
	fetch_and_insert_data()
	previous_path = request.META.get('HTTP_REFERER', '')
	return redirect(previous_path)
