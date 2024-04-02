import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.views import View
from django.views.generic import DetailView, ListView

from product.models import Product

stripe.api_key = settings.STRIPE_SECRET_KEY


class ProductListView(ListView):
    model = Product
    context_object_name = "products"
    template_name = "product/product_list.html"


class ProductDetailView(DetailView):
    model = Product
    context_object_name = "product"
    template_name = "product/product_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data()
        context["prices"] = self.get_object().price
        return context


class CreateStripeCheckoutSessionView(View):
    """
    Create a checkout session and redirect the user to Stripe's checkout page
    """

    def post(self, request, *args, **kwargs):
        product = Product.objects.get(id=self.kwargs["pk"])

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": product.price * 100,
                        "product_data": {
                            "name": product.name,
                        },
                    },
                    "quantity": 1,
                }
            ],
            metadata={"product_id": product.id},
            mode="payment",
            success_url=settings.PAYMENT_SUCCESS_URL,
            cancel_url=settings.PAYMENT_CANCEL_URL,
        )
        # print(checkout_session)
        return redirect(checkout_session.url)
