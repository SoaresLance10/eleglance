from django.contrib import admin
from .models import User_Profile, Product, Wishlist, ProductImage, WishlistItem

# Register your models here.

admin.site.register(User_Profile)


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]

    class Meta:
       model = Product

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass

class WishlistItemAdmin(admin.StackedInline):
    model = WishlistItem

@admin.register(Wishlist)
class WishlisttAdmin(admin.ModelAdmin):
    inlines = [WishlistItemAdmin]

    class Meta:
       model = Wishlist

@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    pass