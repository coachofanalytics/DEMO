from django.urls import path
from . import views
from .views import (
                    PaymentCreateView,#PaymentListView,
                    TransanctionDetailView,TransactionListView,
                    TransactionUpdateView,
                    DefaultPaymentUpdateView,DefaultPaymentListView,
                    
)
app_name = 'finance'
urlpatterns = [
    #=============================FINANCES=====================================
    
    path('finance_report/', views.finance_report, name='finance_report'),
    path('transact/', views.transact, name='finance-transact'),
    path('transaction/', TransactionListView.as_view(), name='transaction-list'),
    path('transaction/<int:pk>/', TransanctionDetailView.as_view(), name='transaction-detail'),
    path('transaction/<int:pk>/update/', TransactionUpdateView.as_view(template_name="finance/payments/transaction_form.html"), name='transaction-update'),
  
    #=============================CLIENT CONTRACT FORM SUBMISSIONS=====================================
    path('contract_form/', views.contract_form_submission, name='finance-contract_form_submission'),
    path('mycontract/<str:username>/', views.mycontract, name='mycontract'),
   
    path('pay/', views.pay, name='pay'),
    path('payment/<int:service>/', views.pay, name='service_pay'),
    path('payment_method/<str:method>/', views.payment, name='payment_method'),
    path("payment_complete/", views.paymentComplete, name="payment_complete"),
    path('payments/', views.payments, name='payments'),
    path('pay/<int:pk>/', views.PaymentInformationUpdateView.as_view(), name='updatepay'),
    
    path('defaultpayments/', DefaultPaymentListView.as_view(template_name='finance/payments/defaultpayments.html'), name='defaultpayments'),
    path('newpayment/', PaymentCreateView.as_view(template_name='finance/payments/payment_form.html'), name='newpayment'),
    path('payment/<int:pk>/update/', DefaultPaymentUpdateView.as_view(template_name='finance/payments/payment_form.html'), name='payment-update'),
    # path('paypal/<int:transaction_id>/', views.paypal_payment, name='paypal_payment'),
    # path('paypal/execute/', views.paypal_execute, name='paypal_execute'),
    # path('mpesa/<int:transaction_id>/', views.mpesa_payment, name='mpesa_payment'),
    # path('mpesa/callback/', views.mpesa_callback, name='mpesa_callback'),
   
]