from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name="login"),
    path('logout', views.logout_view, name="logout"),
    path('signup', views.signup_view, name="signup"),
    path('products', views.products, name="products"),
    path('products/<sku>', views.product, name="product"),
    path('wishlist', views.wishlist, name="wishlist"),
    path('wishlist/add/<sku>', views.addWishlist, name="addWishlist"),
    path('wishlist/remove/<sku>', views.removeWishlist, name="removeWishlist"),
    path('wishlist/send', views.sendWishlist, name="sendWishlist"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)