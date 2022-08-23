from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

INSTITUTION_TYPE = {
    (1, 'fundacja'),
    (2, 'organizacja pozarządowa'),
    (3, 'zbiórka lokalna'),
}


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Institution(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField()
    type = models.IntegerField(choices=INSTITUTION_TYPE, default=1)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=50)
    phone_number = models.BigIntegerField()
    city = models.CharField(max_length=30)
    zip_code = models.IntegerField()
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.CharField(max_length=100, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)

    is_taken = models.BooleanField(default=False)
    taken_time = models.DateTimeField(null=True)


@receiver(pre_delete, sender=User)
def delete_user(sender, instance, **kwargs):
    """This function prevent to deleting any superuser. Result is 403 Forbidden"""
    if instance.is_superuser:
        raise PermissionDenied
