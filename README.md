## Run test

```
$ pip install -r requirements.txt
$ ./manage.py runserver 8100
```
open `index.html` and click pay

**Test UPI ID Details:**

[docs](https://razorpay.com/docs/payments/payments/test-upi-details/)

+ Test payment success flow using `success@razorpay`.
+ Test payment failure flow using `failure@razorpay`.


## Step 1: create order at backend and pass orderid to react

```
razorpay_client = razorpay.Client(auth=(RAZOR_PAY_KEY, RAZOR_PAY_SECRET))
razorpay_order = razorpay_client.order.create(
    {
        "amount": int("2500") * 100,
        "payment_capture": "1",
        "currency": "INR",
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
```

## Step 2: Frontend code
```
<button id="rzp-button1">Pay</button><br>

<script src="https://checkout.razorpay.com/v1/checkout.js"></script>
<script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
<script>
    $("#rzp-button1").click(function (e) {
        e.preventDefault();
        $.post("http://localhost:8100", function (data) {
            console.log(data)
            var options = {
                "key": data.razor_pay_key,
                "name": "SIB FD", //your business name
                "description": "FD account opening",
                "image": "https://videokyc.southindianbank.com/static/images/logo_white.png",
                "order_id": data.order_id, 
                "handler": function (response) {
                    $.ajax({
                        type: "POST",
                        url: "http://localhost:8100/razorpay_redirect/",
                        data: { 
                            'razorpay_payment_id': response.razorpay_payment_id, 
                            'razorpay_order_id': response.razorpay_order_id, 
                            'razorpay_signature': response.razorpay_signature 
                        },
                        success: function (data) {
                            alert(JSON.stringify(data))
                        },
                        error: function (request, status, error) {
                        }
                    });
                },
                // "callback_url": data.callback_url,
                "prefill": { 
                    "name": data.email, //your customer's name
                    "email": data.email,
                    "contact": data.mobile
                },
                "notes": {
                    "razorpay_order_id": data.order_id
                },
                "theme": {
                    "color": "#c90b0c"
                }
            };
            let rzp1 = new Razorpay(options);
            rzp1.open();
        });
    })

</script>
```

## Step 3: Mark as payment successfull in backend

```
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
```