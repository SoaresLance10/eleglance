from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class User_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=64)
    phone = models.CharField(max_length=64)
    company_name = models.CharField(max_length=64)
    location = models.CharField(max_length=64)
    role_in_organisation = models.CharField(max_length=64)
    website = models.CharField(max_length=64)
    access = models.BooleanField(default = False)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        User_Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.user_profile.save()

class Product(models.Model):
    name = models.CharField(max_length=64)
    sku = models.CharField(max_length=64)
    gold_weight = models.FloatField()
    diamond_weight = models.FloatField()
    category = models.CharField(max_length=64)

    def __str__(self):
        return self.name    

class ProductImage(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.product.sku

class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_submitted = models.DateField(null=True, blank=True)
    diamond_quality = models.CharField(max_length=64, null=True, blank=True)
    gold_purity = models.CharField(max_length=64, null=True, blank=True)
    gold_color = models.CharField(max_length=64, null=True, blank=True)
    def __str__(self):
        return f"{self.user.username}'s Wishlist"

@receiver(post_save, sender=User)
def create_wishlist(sender, instance, created, **kwargs):
    if created:
        Wishlist.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_wishlist(sender, instance, **kwargs):
    pass

class WishlistItem(models.Model):
    owner = models.ForeignKey(Wishlist, default=None, on_delete=models.CASCADE)
    item = models.CharField(max_length=64)
    date_added = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"UserID:{self.owner.user_id} 's Item"