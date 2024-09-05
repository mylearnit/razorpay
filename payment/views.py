from django.urls import reverse
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

RAZOR_PAY_KEY = "rzp_test_RT2rwjEYgOiIA0"
RAZOR_PAY_SECRET = "w0GFSNkMAPGzJUNkoLzoJBht"

razorpay_client = razorpay.Client(auth=(RAZOR_PAY_KEY, RAZOR_PAY_SECRET))
# Create your views here.
# https://razorpay.com/docs/payments/third-party-validation/standard-integration/
@csrf_exempt
def razorpay_form(request):
    amount = int("2500") * 100

    razorpay_order = razorpay_client.order.create(
        {
            "amount": amount,
            "payment_capture": "1",
            # "method": "netbanking",
            "currency": "INR",
            # "bank_account": {
            #     "account_number": "77770121225995",
            #     "name": "suhail",
            #     "ifsc": "FDRL0007777",
            # },
        }
    )
    return JsonResponse(
        {
            "order_id": razorpay_order["id"],
            "amount": amount,
            "razor_pay_key": RAZOR_PAY_KEY,
            "name": "suhail",
            "email": "suhailvs@gmail.com",
            "mobile": "7356775981",
            "callback_url":request.build_absolute_uri(reverse('razorpay_redirect'))
        }
    )


@csrf_exempt
def razorpay_redirect(request):
    if request.method == "POST":
        
        payment_id = request.POST["razorpay_payment_id"]
        data = {
            "razorpay_order_id": request.POST["razorpay_order_id"],
            "razorpay_payment_id": payment_id,
            "razorpay_signature": request.POST["razorpay_signature"],
        }
        is_paid = razorpay_client.utility.verify_payment_signature(data)
        if is_paid:
            return JsonResponse({"msg": "Payment success"})
        return JsonResponse({"msg": "Payment failed"})

def check_payment(request,order):
    # payments = {"msg": {"entity": "collection", "count": 1, "items": [{"id": "pay_OtSARmNMVCDCor", "entity": "payment", "amount": 250000, "currency": "INR", "status": "captured", "order_id": "order_OtS9xuYMQLmdv7", "invoice_id": null, "international": false, "method": "upi", "amount_refunded": 0, "refund_status": null, "captured": true, "description": "FD account opening", "card_id": null, "bank": null, "wallet": null, "vpa": "success@razorpay", "email": "suhailvs@gmail.com", "contact": "+917356775981", "notes": {"razorpay_order_id": "order_OtS9xuYMQLmdv7"}, "fee": 5900, "tax": 900, "error_code": null, "error_description": null, "error_source": null, "error_step": null, "error_reason": null, "acquirer_data": {"rrn": "587808187976", "upi_transaction_id": "9F59AA5AC8C6E04B77285355214E3F6E"}, "created_at": 1725532382, "upi": {"vpa": "success@razorpay"}}]}}
    return JsonResponse({"msg": razorpay_client.order.payments(order)})