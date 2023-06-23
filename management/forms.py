from django import forms
from django.forms import Textarea
from data.models import DSU
from management.models import TaskLinks, Policy, Requirement, Task
from finance.models import Transaction, Inflow
from accounts.models import Department
from application.models import UserProfile


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ["name", "slug", "description", "is_active", "is_featured"]
        widgets = {"description": Textarea(attrs={"cols": 40, "rows": 2})}

    def __init__(self, *args, **kwargs):
        super(DepartmentForm, self).__init__(*args, **kwargs)
        self.fields["name"].empty_label = "Select"


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction

        fields = [
            "id",
            "sender",
            "receiver",
            "phone",
            "department",
            "category",
            "type",
            "payment_method",
            "qty",
            "amount",
            "transaction_cost",
            "description",
            "receipt_link",
        ]
        labels = {
            "sender": "Your full Name",
            "receiver": "Enter Receiver Name",
            "phone": "Receiver Phone",
            "department": "Department",
            "category": "Category",
            "type": "Type",
            "payment_method": "Payment Method",
            "qty": "Quantity",
            "amount": "Unit Price",
            "transaction_cost": "Transaction Cost",
            "description": "Description",
            "receipt_link": "Link",
        }
        widgets = {"description": Textarea(attrs={"cols": 30, "rows": 1})}

    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields["payment_method"].empty_label = "Select"


class InflowForm(forms.ModelForm):
    class Meta:
        model = Inflow
        fields = [
            "receiver",
            "phone",
            "category",
            "task",
            "method",
            "period",
            "qty",
            "amount",
            "transaction_cost",
            "description",
        ]
        labels = {
            "receiver": "Enter Receiver Name",
            "phone": "Receiver Phone",
            "department": "Department",
            "category": "Category",
            "task": "Task",
            "method": "Payment Method",
            "period": "Period",
            "qty": "Quantity",
            "amount": "Unit Price",
            "transaction_cost": "Transaction Cost",
            "description": "Comments",
        }
        widgets = {"description": Textarea(attrs={"cols": 30, "rows": 1})}

    def __init__(self, *args, **kwargs):
        super(InflowForm, self).__init__(*args, **kwargs)
        self.fields["method"].empty_label = "Select"


class PolicyForm(forms.ModelForm):
    class Meta:
        model = Policy
        fields = [
            "staff",
            # "first_name",
            # "last_name",
            "department",
            "day",
            "type",
            "description",
            "link",
            "policy_doc",
            "is_active",
            "is_featured",
            "is_internal",
        ]
        labels = {
            "staff": "User Name",
            "link": "Paste Link",
            "day": "Review Day",
            # "first_name": "First Name",
            # "last_name": "Last Name",
            "type": "Policy Type",
            "department": "Department",
            "description": "Description",
            "policy_doc": "Attach Policy",
        }
        widgets = {"description": Textarea(attrs={"cols": 75, "rows": 3})}



class ManagementForm(forms.ModelForm):
    class Meta:
        model = DSU
        # fields =['client','category','question_type','doc','link']
        fields = [
            "trained_by",
            "client_name",
            "type",
            "category",
            "task",
            "plan",
            "challenge",
            "uploaded",
        ]
        labels = {
            "type": "Client/Staff?",
            "client_name": "Manager",
            "trained_by": "Staff/Employee",
            "category": "Category",
            "task": "What Did You Work On?",
            "plan": "What is your next plan of action on areas that you have not touched on?",
            "challenge": "What specific questions/Challenges are you facing?",
            "uploaded": "Have you uploaded any DAF evidence/1-1 sessions?",
        }


class RequirementForm(forms.ModelForm):
    class Meta:
        model = Requirement
        fields = [
            # "created_by",
            "creator",
            "assigned_to",
            "requestor",
            "status",
            "company",
            "category",
            "app",
            "delivery_date",
            "duration",
            "what",
            "why",
            "how",
            "comments",
            "doc",
            "pptlink",
            "videolink",
            "is_active",
            "is_tested",
        ]

        labels = {
            "creator": "Creator",
            "assigned_to": "assigned_to",
            "requestor ": "Who needs it/beneficiary?",
            "app": "Specify app if Website",
            "company": "company",
            "category": "Select a category",
            "what": "Describe the Requirement",
            "why": "Why do they need it ?",
            "delivery_date": "When should this be delivered",
            "how": "Mode of delivery(website/Report/database?",
            "duration": "how long will it take to work on this requirement",
            "doc": "Upload Supporting Document",
            "pptlink": "Add link",
            "pptlink": "Add Video link",
        }
    # def __init__(self, **kwargs):
    #     super(RequirementForm, self).__init__(**kwargs)
    #     self.fields["created_by"].queryset = CustomerUser.objects.filter(
    #         is_staff=True
    #         # Q(is_staff=True)
    #     )


class EvidenceForm(forms.ModelForm):
    class Meta:
        model = TaskLinks
        fields = [
            "task",
            "added_by",
            "link_name",
            "linkpassword",
            "description",
            "doc",
            "link",
            "linkpassword",
            "is_active",
            "is_featured",
        ]

        labels = {
            "task ": "Task Name",
            "added_by": "Your Username",
            "link_name": "Enter link name",
            "linkpassword": "If Links Needs Password Enter Password here:",
            "description": "What is this link/Evidence about",
            "doc": "Upload file/document if possible",
            "link": "Upload link/paste your link below",
            "linkpassword": "Provide Password if necessary",
            # "is_active ":"Is this link still active "
        }
        widgets = {"description": Textarea(attrs={"cols": 60, "rows": 2})}

        #  If you have to exclude some features you put them here
        # exclude = (
        #     "user",
        #     "recurring",
        # )

        # Forms updated by Karki

    # def __init__(self, **kwargs):
    #     super(EvidenceForm, self).__init__(**kwargs)
    #     self.fields["added_by"].queryset = CustomerUser.objects.filter(is_staff=True)


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
                   "group",
                    "category",
                    "employee",
                    "activity_name",
                    "description",
                    "point",
                    "mxpoint",
                    "mxearning",
        ]

        widgets = {"description": Textarea(attrs={"cols": 60, "rows": 2})}


class EmployeeContractForm(forms.ModelForm):
    national_id_no = forms.CharField(required=True)
    emergency_name = forms.CharField(required=True)
    emergency_address = forms.CharField(required=True)
    emergency_citizenship = forms.CharField(required=True)
    emergency_email = forms.CharField(required=True)
    emergency_phone = forms.CharField(required=True)
    emergency_national_id_no = forms.CharField(required=True)

    class Meta:
        model = UserProfile
        fields = ('national_id_no', 'id_file', 'emergency_name', 'emergency_address', 'emergency_citizenship', 'emergency_email', 'emergency_phone', 'emergency_national_id_no')


class MonthForm(forms.Form):
    MONTHS = (
        ('0', 'Month'),
        ('1', 'January'),
        ('2', 'February'),
        ('3', 'March'),
        ('4', 'April'),
        ('5', 'May'),
        ('6', 'June'),
        ('7', 'July'),
        ('8', 'August'),
        ('9', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December'),
    )

    YEAR = (
        ('0', 'Year'),
        ('2022', '2022'),
        ('2023', '2023'),
    )
    month = forms.ChoiceField(choices=MONTHS)
    year = forms.ChoiceField(choices=YEAR)
