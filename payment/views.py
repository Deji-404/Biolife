import json, requests
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.urls import reverse
from django.contrib import messages
from .forms import PaymentInitForm
from .models import Payment
from market.models import Order
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def payment_init(request):

    order = Order.objects.filter(user=request.user, ordered=False)[0]
    order_items = order.items.all()
    

    if request.method == "POST":
        amount = order.get_total_price()
        form = PaymentInitForm(request.POST)

        if form.is_valid():
            payment = form.save(commit=False)
            payment.amount = amount
            payment.order = order
            payment.save()

            request.session['payment_id'] = payment.id
            messages.success(request, "Payment Initialized successfully")

            return redirect(reverse('payment:process'))
        
    else:

        try:
            pay = get_object_or_404(Payment, order=order)
            print(pay)
            pay.amount = order.get_total_price()
            pay.save()
            request.session['payment_id'] = pay.id
            messages.success(request, "Payment Initialized successfully")

            return redirect(reverse('payment:process'))
        
        except:
            print("None")

        form = PaymentInitForm()

    return render(request, 'payment/create.html', {'form': form,
                                                   'order': order,
                                                   'items': order_items
                                                   })

api_key = settings.PAYSTACK_TEST_SECRET_KEY
url = settings.PAYSTACK_INITIALIZE_PAYMENT_URL

@login_required
def payment_process(request):

    payment_id = request.session.get('payment_id', None)
    payment = get_object_or_404(Payment, id=payment_id)
    amount = payment.get_amount() * 100

    if request.method == "POST":

        success_url = request.build_absolute_uri(reverse('payment:success'))
        cancel_url = request.build_absolute_uri(reverse('payment:canceled'))

        metadata = json.dumps({
            "payment_id": payment_id,
            "cancel_action": cancel_url
        })

        #paystack checkout session data
        session_data = {
            'email': payment.email,
            'amount': int(amount),
            'callback_url': success_url,
            'metadata': metadata
        }

        headers = {"authorization": f"Bearer {api_key}"}
        #api request to paystack server
        r = requests.post(url, headers=headers, data=session_data)
        response = r.json()

        if response["status"] == True:
            #redirect to paystack payment form
            try:
                redirect_url = response["data"]["authorization_url"]
                return redirect(redirect_url, code=303)

            except:
                pass

        else:

            return render(request, 'payment/process.html', {'payment': payment})
    else:

        return render(request, 'payment/process.html', {'payment': payment})
    
@login_required
def payment_success(request):

    order = Order.objects.filter(user=request.user, ordered=False)[0]
    payment_id = request.session.get('payment_id', None)
    payment = get_object_or_404(Payment, id=payment_id)

    # retrive the query parameter from the request object
    ref = request.GET.get('reference', '')
    # verify transaction endpoint
    url = 'https://api.paystack.co/transaction/verify/{}'.format(ref)

    #set headers
    headers = {"authorization": f"Bearer {api_key}"}
    r = requests.get(url, headers=headers)
    res = r.json()
    print(res)
    res = res["data"]

    #verify before setting payment
    if res["status"] == "success":
        #update payment
        payment.paystack_ref = ref
        payment.save()
        order.ordered = True
        order.save()

    return render(request, 'payment/success.html')

@login_required
def payment_canceled(request):
    return render(request, 'payment/canceled.html')
