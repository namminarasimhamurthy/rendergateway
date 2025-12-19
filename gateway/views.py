import razorpay
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Razorpay client
client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)


def home(request):
    amount = 100  # INR
    amount_paise = amount * 100

    try:
        order = client.order.create({
            "amount": amount_paise,
            "currency": "INR",
            "payment_capture": 1
        })
    except Exception as e:
        return render(request, "error.html", {"error": str(e)})

    context = {
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "order_id": order["id"],
        "amount": amount_paise
    }

    return render(request, "index.html", context)


@csrf_exempt
def success(request):
    if request.method == "POST":
        payment_id = request.POST.get("razorpay_payment_id")
        order_id = request.POST.get("razorpay_order_id")
        signature = request.POST.get("razorpay_signature")

        return render(request, "success.html", {
            "payment_id": payment_id,
            "order_id": order_id,
            "signature": signature
        })

    return render(request, "success.html", {"error": "Invalid access"})
