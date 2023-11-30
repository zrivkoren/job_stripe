from django.db import models
import stripe
import os


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stripe_price_id = models.CharField(max_length=50, blank=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.stripe_price_id:
            product = stripe.Product.create(name=self.name)

            price = stripe.Price.create(
                unit_amount=int(self.price * 100),
                currency="usd",
                product=product.id,
            )

            self.stripe_price_id = price.id

        super().save(*args, **kwargs)
