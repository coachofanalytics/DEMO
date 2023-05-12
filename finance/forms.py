from django import forms
from django.forms import Textarea
from django.db.models import Q
from pyexpat import model
from accounts.models import User

from .models import (
    Transaction,
    Inflow
)

# class TransactionForm(forms.ModelForm):
#     class Meta:
#         model = Transaction
#         fields = [
#             "id",
#             "sender",
#             "receiver",
#             "phone",
#             "department",
#             "category",
#             "type",
#             "payment_method",
#             "qty",
#             "amount",
#             "transaction_cost",
#             "description",
#             "receipt_link",
#         ]
#         labels = {
#             "sender": "Your full Name",
#             "receiver": "Enter Receiver Name",
#             "phone": "Receiver Phone",
#             "department": "Department",
#             "category": "Category",
#             "type": "Type",
#             "payment_method": "Payment Method",
#             "qty": "Quantity",
#             "amount": "Unit Price",
#             "transaction_cost": "Transaction Cost",
#             "description": "Description",
#             "receipt_link": "Link",
#         }
#         widgets = {"description": Textarea(attrs={"cols": 30, "rows": 1})}

#     def __init__(self, *args, **kwargs):
#         super(TransactionForm, self).__init__(*args, **kwargs)
#         self.fields["payment_method"].empty_label = "Select"

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