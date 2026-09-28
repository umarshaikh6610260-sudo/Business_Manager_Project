from django.db import models


class Customer(models.Model):

    name = models.CharField(max_length=100)

    phone = models.CharField(max_length=15)

    email = models.EmailField(blank=True, null=True)

    address = models.TextField(blank=True, null=True)

    notes = models.TextField(blank=True, null=True)

    follow_up_date = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name