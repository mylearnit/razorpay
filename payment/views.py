from django.shortcuts import render
import razorpay

RAZOR_PAY_KEY="rzp_test_RT2rwjEYgOiIA0"
RAZOR_PAY_SECRET="w0GFSNkMAPGzJUNkoLzoJBht"
# Create your views here.
def razorpay_form(request):
    
    razorpay_client = razorpay.Client(
        auth=(RAZOR_PAY_KEY, RAZOR_PAY_SECRET)
    )
    currency = "INR"
    amount = int('2500') * 100
    razorpay_order = razorpay_client.order.create(
        dict(
            amount=amount,
            currency=currency,
            payment_capture="1",
        )
    )
    return render(
        request,
        "razorpay.html",
        {
            "order": razorpay_order["id"],
            "amount": amount,
            "razor_pay_key": RAZOR_PAY_KEY,
        },
    )