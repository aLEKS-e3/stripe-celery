from product.models import Product

from celery import shared_task


@shared_task
def count():
    return Product.objects.count()


@shared_task
def summ(a, b):
    return a + b
