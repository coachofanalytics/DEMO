from django import forms
from django.forms import Textarea
from django.db.models import Q
from pyexpat import model
from accounts.models import User

from .models import (
    Transaction,
   
)



class InflowForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields= "__all__"
        # fields = [
        #     "receiver",
        #     "phone",
        #     "category",
        #     "task",
        #     "method",
        #     "period",
        #     "qty",
        #     "amount",
        #     "transaction_cost",
        #     "description",
        # ]
        labels = {
            "receiver": "Enter Receiver Name",
            "phone": "Receiver Phone",
            "sender_phone": "Sender's Number",
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