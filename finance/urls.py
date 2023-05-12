from django.urls import path
from . import views
from .views import (
                    PaymentCreateView,#PaymentListView,
                    TransanctionDetailView,TransactionListView,
                    TransactionUpdateView,TransactionDeleteView,
                    UserInflowListView,InflowDetailView,InflowUpdateView,InflowDeleteView,
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
    path('transaction/<int:pk>/delete/', TransactionDeleteView.as_view(template_name="finance/payments/transaction_confirm_delete.html"), name='transaction-delete'),
     #-----------CASHINFLOW---------------------------------------
    path('inflow_entry/', views.inflow, name='entry_inflow'),
    #path('inflow/', InflowListView.as_view(), name='inflow-list'),
    path('inflows/', views.inflows, name='inflow-list'),
    path('user_inflow/<str:username>', views.userlist, name='userinflow'),
    #path('inflow/new/', InflowCreateView.as_view(), name='inflow-create'),
    # path('inflow/<int:pk>/views.', InflowDetailView.as_view(), name='inflow-detail'),
    # path('inflow/<str:username>/', inflow_detail, name='userinflow'),
    path('inflow/<int:pk>/delete/', InflowDeleteView.as_view(), name='inflow-delete'),
    path('inflow/<int:pk>/update/', InflowUpdateView.as_view(), name='inflow-update'),
    #=============================CLIENT CONTRACT FORM SUBMISSIONS=====================================
    path('contract_form/', views.contract_form_submission, name='finance-contract_form_submission'),
    path('mycontract/<str:username>/', views.mycontract, name='mycontract'),
    path('new_contract/<str:username>/', views.newcontract, name='newcontract'),
    #Pay URLS
    # path('userpay/', views.userpay, name='userpay'),
    path('pay/', views.pay, name='pay'),
    path('payment/<int:service>/', views.pay, name='service_pay'),
    path('payment_method/<str:method>/', views.payment, name='payment_method'),
    path("payment_complete/", views.paymentComplete, name="payment_complete"),
    path('payments/', views.payments, name='payments'),
    path('pay/<int:pk>/', views.PaymentInformationUpdateView.as_view(), name='updatepay'),
    
    path('defaultpayments/', DefaultPaymentListView.as_view(template_name='finance/payments/defaultpayments.html'), name='defaultpayments'),
    path('newpayment/', PaymentCreateView.as_view(template_name='finance/payments/payment_form.html'), name='newpayment'),
    path('payment/<int:pk>/update/', DefaultPaymentUpdateView.as_view(template_name='finance/payments/payment_form.html'), name='payment-update'),
    #Pay configs URLS
    # path('newpaymentconfigs/',views.PaymentConfigCreateView.as_view(template_name='finance/payments/payment_form.html'), name='newpaymentconfigs'),
    # path('paymentconfigs/', views.PaymentConfigListView.as_view(), name='paymentconfigs'),
    # path('paymentconfigs/<int:pk>/update/', views.PaymentConfigUpdateView.as_view(template_name='finance/payments/payment_form.html'), name='paymentconfigs-update'),

]