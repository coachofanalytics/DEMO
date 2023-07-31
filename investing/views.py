from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import user_passes_test
from django.urls import reverse
import math
from django.db.models import Q,Max,F
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model
from django.views.generic import ListView, DetailView, UpdateView
from datetime import date,datetime,time,timezone
from .utils import compute_pay,get_over_postions,investment_test,computes_days_expiration,get_user_investment
from .forms import (
    CoveredCallsForm,
    ShortPutForm,
    CreditSpreadForm,
    InvestmentForm,
    InvestmentRateForm
)
from .models import (
    stockmarket,
    ShortPut,
    covered_calls,
    credit_spread,
    Investments,
    Investment_rates,
    Oversold
)
from django.db.models import Q
from accounts.models import CustomerUser
from getdata.utils import (
    main_shortput,
)
from main.utils import path_values



User=get_user_model

# Create your views here.
def home(request):
    return render(request, 'main/home_templates/investing_home.html', {'title': 'home'})

def coveredcalls(request):
    return render(request, 'investing/covered_call.html', {'title': 'covered Calls'})

def training(request):
    return render(request, 'investing/training.html', {'title': 'training'})

@login_required
def newinvestment(request):
    if request.method == 'POST':
        form = InvestmentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.client=request.user
            instance.save()
            # return redirect('investing:user_investments', request.user) 
            return redirect('finance:newoptioncontract', request.user) 
    else:
        form = InvestmentForm()
    return render(request, 'investing/investment_form.html', {'form': form})

@login_required
def newinvestmentrate(request):
    if request.method == 'POST':
        form = InvestmentRateForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return redirect('investing:investments') 
    else:
        form = InvestmentRateForm()
    return render(request, 'main/snippets_templates/generalform.html', {'form': form})


def investments(request):
    investments=Investments.objects.all()
    latest_investment = Investments.objects.latest('investment_date')
    total_amt=0
    for amt  in investments:
        total_amt=total_amt+amt.amount
        print(total_amt)
    amount_invested=float(total_amt)*float(0.33)
    amount = float(total_amt)
    returns=compute_pay(amount)
    print(amount,amount_invested,returns)
    context={
        "investments":investments,
        "latest_investment":latest_investment,
        "amount":amount,
        "amount_invested":amount_invested,
         'title': 'training',
         'returns': returns
    }
    return render(request, 'investing/clients_investments.html',context)


def user_investments(request, username=None, *args, **kwargs):
    user = get_object_or_404(CustomerUser, username=username)
    investments = Investments.objects.filter(client=user)
    latest_investment_rates = Investment_rates.objects.order_by('-created_date').first()
    # latest_investment_rates if Investment_rates.exists() else None
    (total_amount,protected_capital,amount_invested,
     bi_weekly_returns,number_positions,minimum_duration
     )=get_user_investment(investments,latest_investment_rates)
    
    context = {
        "investments": investments,
        # "latest_investment": latest_investment if investments.exists() else None,
        "title": "training",
        "amount": total_amount,
        "protected_capital": protected_capital,
        "number_positions": number_positions,
        "amount_invested": amount_invested,
        "minimum_duration": minimum_duration,
        "returns": bi_weekly_returns
    }
    return render(request, 'investing/clients_investments.html', context)

# def user_investments(request, username=None, *args, **kwargs):
#     user = get_object_or_404(CustomerUser, username=username)
#     investments = Investments.objects.filter(client=user)
#     # investment_test()
#     # Check if any investments exist for the user
#     if investments.exists():
#         latest_investment_rate = Investment_rates.objects.aggregate(latest_created_date=Max('created_date'))
#         latest_created_date = latest_investment_rate['latest_created_date']
#         latest_investment_rates = Investment_rates.objects.filter(created_date=latest_created_date).first()
#         minimum_amount = latest_investment_rates.base_amount
#         base_return = latest_investment_rates.initial_return
#         inc_rate = latest_investment_rates.increment_rate
#         increment_threshold_amt = latest_investment_rates.increment_threshold
#         decrease_threshold_amt = latest_investment_rates.decrease_threshold
#         rate_investment = latest_investment_rates.investment_rate
#         minimum_duration = latest_investment_rates.duration
#         total_amt=0
#         for amt  in investments:
#             total_amt=total_amt+amt.amount
#             print(total_amt)
#         amount_invested=float(total_amt)*float(rate_investment)
#         total_amount = float(total_amt)
#         amount = float(amount_invested)
#         protected_capital=total_amount-amount
#         number_positions = math.floor(amount / 1000)
#         returns = compute_pay(amount,minimum_amount, base_return, inc_rate, increment_threshold_amt, decrease_threshold_amt)

#     else:
#         # Set default values for amount and returns or display an appropriate message
#         amount_invested=0.0
#         protected_capital=0.0
#         total_amount = 0.0
#         returns = 0.0
#         number_positions = 0
#         minimum_duration = 0
#         print("No investments found for the user.")

#     context = {
#         "investments": investments,
#         # "latest_investment": latest_investment if investments.exists() else None,
#         "title": "training",
#         "amount": total_amount,
#         "protected_capital": protected_capital,
#         "number_positions": number_positions,
#         "amount_invested": amount_invested,
#         "minimum_duration": minimum_duration,
#         "returns": returns
#     }
#     return render(request, 'investing/clients_investments.html', context)

def options_play_shortput(request):
    # Call the main_shortput function to retrieve the data
    message = 'we are done processing your request'
    data = main_shortput(request)
    # Loop through the data and insert it into the database
    created_count = 0
    for row in data:
        symbol = row[0]
        action = row[1]
        expiry = row[2]
        days_to_expiry = row[3]
        strike_price = row[4]
        mid_price = row[5]
        bid_price = row[6]
        ask_price = row[7]
        implied_volatility_rank = row[8]
        earnings_date = row[9]
        stock_price = row[11]
        raw_return = row[12]
        annualized_return = row[13]
        distance_to_strike = row[14]

        obj, created = ShortPut.objects.get_or_create(
            Symbol=symbol,
            Action=action,
            Expiry=expiry,
            Days_To_Expiry=days_to_expiry,
            Strike_Price=strike_price,
            defaults={
                'Mid_Price': mid_price,
                'Bid_Price': bid_price,
                'Ask_Price': ask_price,
                'Implied_Volatility_Rank': implied_volatility_rank,
                'Earnings_Date': earnings_date,
                'Stock_Price': stock_price,
                'Raw_Return': raw_return,
                'Annualized_Return': annualized_return,
                'Distance_To_Strike': distance_to_strike
            }
        )
        if created:
            created_count += 1
    # return render (request, "main/snippets_templates/output_snippets/option_data.html", context)
    return redirect ('getdata:shortputdata')

def optiondata(request):
    path_list,sub_title,pre_sub_title = path_values(request)
    # Get current datetime with UTC timezone
    date_today = datetime.now(timezone.utc)
   
    if sub_title == 'covered_calls':
        title = 'COVERED CALLS'
        stockdata = covered_calls.objects.all().filter(is_featured=True)
    elif sub_title == 'shortputdata':
        title = 'SHORT PUT'
        stockdata = ShortPut.objects.all().filter(is_featured=True)
    else:
        title = 'CREDIT SPREAD'
        stockdata = credit_spread.objects.all().filter(is_featured=True)

    def get_edit_url(row_id):
        if pre_sub_title == 'shortputdata':
            return reverse('investing:shortputupdate', args=[row_id])
        elif pre_sub_title == 'credit_spread':
                return reverse('investing:creditspreadupdate', args=[row_id])
        else:
            return reverse('investing:coveredupdate', args=[row_id])
            
    filtered_stockdata = []
    days_to_expiration = 0
    for x in stockdata:
        if isinstance(x.expiry, str):
            expiry_str = x.expiry
            expirydate = datetime.strptime(expiry_str, "%m/%d/%Y")
            expiry_date = expirydate.astimezone(timezone.utc)
        elif isinstance(x.expiry, datetime):
            expiry_date = x.expiry.astimezone(timezone.utc)
        else:
            continue
        
        days_to_exp = expiry_date - date_today
        days_to_expiration = days_to_exp.days
        if days_to_expiration > 7:
            filtered_stockdata.append(x)

    context = { 
        "data": filtered_stockdata,
        "days_to_expiration": days_to_expiration,
        "subtitle": sub_title,
        "pre_sub_title": pre_sub_title,
        'title': title,
        "get_edit_url": get_edit_url,
    }
    return render(request, "main/snippets_templates/output_snippets/option_data.html", context)




class OptionList(ListView):
    model=stockmarket
    template_name="getdata/options.html"
    context_object_name = "stocks"


@login_required
@user_passes_test(lambda u: u.is_superuser)
def shortput_update(request, pk):
    path_list,subtitle,pre_sub_title=path_values(request)
    shortput = get_object_or_404(ShortPut, pk=pk)
    success_url = reverse('investing:shortput')

    if request.method == 'POST':
        form = ShortPutForm(request.POST, instance=shortput)
        if form.is_valid():
            form.save()
            return redirect(success_url)
    else:
        form = ShortPutForm(instance=shortput)

    context = {
        'form': form,
        'title': 'Update Short Put',
    }
    return render(request, 'main/snippets_templates/generalform.html', context)

class covered_calls_update(UpdateView):
    model = covered_calls
    success_url = "/investing/covered_calls"
    # fields = "__all__"
    fields = ['symbol','comment','is_featured']
    template_name="main/snippets_templates/generalform.html"
    def form_valid(self, form):
        # form.instance.author=self.request.user
        return super().form_valid(form)
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False
    
class credit_spread_update(UpdateView):
    model = credit_spread
    success_url = "/investing/credit_spread"
    # fields = "__all__"
    fields = ['symbol','comment','is_featured']
    template_name="main/snippets_templates/generalform.html"
    def form_valid(self, form):
        return super().form_valid(form)
    def test_func(self):
        # interview = self.get_object()
        if self.request.user.is_superuser:
            return True
        return False


def oversoldpositions(request):
    path_list,sub_title,pre_sub_title = path_values(request)
    # Get current datetime with UTC timezone
    table_name = "investing_oversold"
    get_over_postions(table_name)
    overboughtsold_records = Oversold.objects.all()
    # expiry_date,days_to_expiration=computes_days_expiration(stockdata)
    for record in overboughtsold_records:
        print("record========>",record)

    context = { 
        "overboughtsold": overboughtsold_records,
        "overboughtsold": overboughtsold_records,
        # "expiry_date": expiry_date,
        # "days_to_expiration": days_to_expiration,
    }
    return render(request, "investing/oversold.html", context)

class oversold_update(UpdateView):
    model = Oversold
    success_url = "/investing/overboughtsold"
    fields ="__all__"
    # fields = ['symbol','comment','is_featured']
    template_name="main/snippets_templates/generalform.html"
    def form_valid(self, form):
        # form.instance.author=self.request.user
        return super().form_valid(form)
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False
