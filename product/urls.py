from django.urls import path

from product.views import CreateStripeCheckoutSessionView, ProductListView, ProductDetailView

app_name = "products"

urlpatterns = [
    path("products/", ProductListView.as_view(), name="product-list"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path(
        "products/<int:pk>/create-checkout-session/",
        CreateStripeCheckoutSessionView.as_view(),
        name="create-checkout-session",
    ),
]
