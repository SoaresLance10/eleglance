from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from datetime import date
from itertools import chain
from json import dumps
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .models import User_Profile, Product, Wishlist, ProductImage, WishlistItem

# Create your views here.
def index(request):
    return render(request, "webapp/layout.html", {"title": "Home"})

def login_view(request):
    if request.method=="POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["pw"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            if user.user_profile.access:
                login(request, user)
                return redirect(reverse("products"))
            else:
                return render(request, "webapp/login.html", {'title': 'Login', 'flash_msg': "Account hasn't been Granted Access yet."})
        else:
            message="Incorrect Username or Password, Try again."
            return render(request, "webapp/login.html", {"flash_msg": message, "title": "Login"})
    else:
        return render(request, "webapp/login.html", {"title": "Login"})

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def signup_view(request):
    if request.method=="POST":
        if request.POST['pw1']!=request.POST['pw2']:
            return render (request, "webapp/signup.html", {'title': 'Signup', 'flash_msg': "Passwords don't match"})
        
        try:
            user = User.objects.create_user(username=request.POST['username'], first_name=request.POST['f_name'], last_name=request.POST['l_name'],email=request.POST['email'], password=request.POST['pw1'])
            user.save()
            print(user)
        except IntegrityError:
            return render(request, "webapp/signup.html", {"title": "Signup", 'flash_msg': 'Username Unavailable'})

        u = User.objects.get(username=request.POST['username'])
        u.user_profile.phone = request.POST['phone']
        u.user_profile.company_name = request.POST['company_name']
        u.user_profile.location = request.POST['location']
        u.user_profile.role_in_organisation = request.POST['role']
        u.user_profile.website = request.POST['website']
        u.save()

        return render(request, "webapp/signup.html", {'title': 'Signup', 'flash_msg': "Account Created, Please wait for Amdinistrator to grant Access"})

    else:
        return render(request, "webapp/signup.html", {'title': 'Signup'})


@login_required(login_url='login')
def products(request):
    products_with_images = {}
    wishlist = []
    filters = []
    keyword = ""
    all_products = Product.objects.all()
    products = all_products

    #Category Filtering
    if request.GET.get('category1') and request.GET.get('category1')=="Earrings":
        filters.append('category1')
        
        if request.GET.get('category2') and request.GET.get('category2')=="Pendants":
            filters.append('category2')
            
            if request.GET.get('category3') and request.GET.get('category3')=="Rings":
                products = all_products.filter(Q(category="Earring") | Q(category="Pendant") | Q(category="Ring"))
                filters.append('category3')
                
            else:
                products = all_products.filter(Q(category="Earring") | Q(category="Pendant"))

        else:
            if request.GET.get('category3') and request.GET.get('category3')=="Rings":
                products = all_products.filter(Q(category="Earring") | Q(category="Ring"))
                filters.append('category3')
                
            else:
                products = all_products.filter(category="Earring")

    else:
        if request.GET.get('category2') and request.GET.get('category2')=="Pendants":
            filters.append('category2')
            
            if request.GET.get('category3') and request.GET.get('category3')=="Rings":
                products = all_products.filter(Q(category="Pendant") | Q(category="Ring"))
                filters.append('category3')
                
            else:
                products = all_products.filter(category="Pendant")

        else:
            if request.GET.get('category3') and request.GET.get('category3')=="Rings":
                products = all_products.filter(category="Ring")
                filters.append('category3')
                
            else:
                pass

    category_filtered = products

    #Diamond Weight Filtering
    if request.GET.get('dwt1') and request.GET.get('dwt1')=="true":
        filters.append('dwt1')
        
        if request.GET.get('dwt2') and request.GET.get('dwt2')=="true":
            filters.append('dwt2')

            if request.GET.get('dwt3') and request.GET.get('dwt3')=="true":
                filters.append('dwt3')

                if request.GET.get('dwt4') and request.GET.get('dwt4')=="true":
                    products = category_filtered.filter(Q(diamond_weight__gte=0.01, diamond_weight__lte=0.50) | Q(diamond_weight__gte=0.51, diamond_weight__lte=0.75) | Q(diamond_weight__gte=0.76, diamond_weight__lte=1.0) | Q(diamond_weight__gte=1.01))
                    filters.append('dwt4')
                else:
                    products = category_filtered.filter(Q(diamond_weight__gte=0.01, diamond_weight__lte=0.50) | Q(diamond_weight__gte=0.51, diamond_weight__lte=0.75) | Q(diamond_weight__gte=0.76, diamond_weight__lte=1.0))
                    
            else:
                if request.GET.get('dwt4') and request.GET.get('dwt4')=="true":
                    products = category_filtered.filter(Q(diamond_weight__gte=0.01, diamond_weight__lte=0.50) | Q(diamond_weight__gte=0.51, diamond_weight__lte=0.75) | Q(diamond_weight__gte=1.01))
                    filters.append('dwt4')
                else:
                    products = category_filtered.filter(Q(diamond_weight__gte=0.01, diamond_weight__lte=0.50) | Q(diamond_weight__gte=0.51, diamond_weight__lte=0.75))

        else:
            if request.GET.get('dwt3') and request.GET.get('dwt3')=="true":
                filters.append('dwt3')

                if request.GET.get('dwt4') and request.GET.get('dwt4')=="true":
                    products = category_filtered.filter(Q(diamond_weight__gte=0.01, diamond_weight__lte=0.50) | Q(diamond_weight__gte=0.76, diamond_weight__lte=1.0) | Q(diamond_weight__gte=1.01))
                    filters.append('dwt4')
                else:
                    products = category_filtered.filter(Q(diamond_weight__gte=0.01, diamond_weight__lte=0.50) | Q(diamond_weight__gte=0.76, diamond_weight__lte=1.0))

            else:
                if request.GET.get('dwt4') and request.GET.get('dwt4')=="true":
                    products = category_filtered.filter(Q(diamond_weight__gte=0.01, diamond_weight__lte=0.50) | Q(diamond_weight__gte=1.01))
                    filters.append('dwt4')
                else:
                    products = category_filtered.filter(diamond_weight__gte=0.01, diamond_weight__lte=0.50)

    else:
        if request.GET.get('dwt2') and request.GET.get('dwt2')=="true":
            filters.append('dwt2')

            if request.GET.get('dwt3') and request.GET.get('dwt3')=="true":
                filters.append('dwt3')

                if request.GET.get('dwt4') and request.GET.get('dwt4')=="true":
                    products = category_filtered.filter(Q(diamond_weight__gte=0.51, diamond_weight__lte=0.75) | Q(diamond_weight__gte=0.76, diamond_weight__lte=1.0) | Q(diamond_weight__gte=1.01))
                    filters.append('dwt4')
                else:
                    products = category_filtered.filter(Q(diamond_weight__gte=0.51, diamond_weight__lte=0.75) | Q(diamond_weight__gte=0.76, diamond_weight__lte=1.0))

            else:
                if request.GET.get('dwt4') and request.GET.get('dwt4')=="true":
                    products = category_filtered.filter(Q(diamond_weight__gte=0.51, diamond_weight__lte=0.75) | Q(diamond_weight__gte=1.01))
                    filters.append('dwt4')
                else:
                    products = category_filtered.filter(diamond_weight__gte=0.51, diamond_weight__lte=0.75)

        else:
            if request.GET.get('dwt3') and request.GET.get('dwt3')=="true":
                filters.append('dwt3')

                if request.GET.get('dwt4') and request.GET.get('dwt4')=="true":
                    products = category_filtered.filter(Q(diamond_weight__gte=0.76, diamond_weight__lte=1.0) | Q(diamond_weight__gte=1.01))
                    filters.append('dwt4')
                else:
                    products = category_filtered.filter(diamond_weight__gte=0.76, diamond_weight__lte=1.0)

            else:
                if request.GET.get('dwt4') and request.GET.get('dwt4')=="true":
                    products = category_filtered.filter(diamond_weight__gte=1.01)
                    filters.append('dwt4')
                else:
                    pass

    diamond_wt_filtered = products

    #Gold Weight Filtering
    if request.GET.get('gwt1') and request.GET.get('gwt1')=="true":
        filters.append('gwt1')
        
        if request.GET.get('gwt2') and request.GET.get('gwt2')=="true":
            filters.append('gwt2')

            if request.GET.get('gwt3') and request.GET.get('gwt3')=="true":
                filters.append('gwt3')

                if request.GET.get('gwt4') and request.GET.get('gwt4')=="true":
                    products = diamond_wt_filtered.filter(Q(gold_weight__gte=0.10, gold_weight__lte=2.50) | Q(gold_weight__gte=2.51, gold_weight__lte=3.50) | Q(gold_weight__gte=3.51, gold_weight__lte=5.0) | Q(gold_weight__gte=5.01))
                    filters.append('gwt4')
                else:
                    products = diamond_wt_filtered.filter(Q(gold_weight__gte=0.10, gold_weight__lte=2.50) | Q(gold_weight__gte=2.51, gold_weight__lte=3.50) | Q(gold_weight__gte=3.51, gold_weight__lte=5.0))

            else:
                if request.GET.get('gwt4') and request.GET.get('gwt4')=="true":
                    products = diamond_wt_filtered.filter(Q(gold_weight__gte=0.10, gold_weight__lte=2.50) | Q(gold_weight__gte=2.51, gold_weight__lte=3.50) | Q(gold_weight__gte=5.01))
                    filters.append('gwt4')
                else:
                    products = diamond_wt_filtered.filter(Q(gold_weight__gte=0.10, gold_weight__lte=2.50) | Q(gold_weight__gte=2.51, gold_weight__lte=3.50))

        else:
            if request.GET.get('gwt3') and request.GET.get('gwt3')=="true":
                filters.append('gwt3')

                if request.GET.get('gwt4') and request.GET.get('gwt4')=="true":
                    products = diamond_wt_filtered.filter(Q(gold_weight__gte=0.10, gold_weight__lte=2.50) | Q(gold_weight__gte=3.51, gold_weight__lte=5.0) | Q(gold_weight__gte=5.01))
                    filters.append('gwt4')
                else:
                    products = diamond_wt_filtered.filter(Q(gold_weight__gte=0.10, gold_weight__lte=2.50) | Q(gold_weight__gte=3.51, gold_weight__lte=5.0))

            else:
                if request.GET.get('gwt4') and request.GET.get('gwt4')=="true":
                    products = diamond_wt_filtered.filter(Q(gold_weight__gte=0.10, gold_weight__lte=2.50) | Q(gold_weight__gte=5.01))
                    filters.append('gwt4')
                else:
                    products = diamond_wt_filtered.filter(gold_weight__gte=0.10, gold_weight__lte=2.50)

    else:
        if request.GET.get('gwt2') and request.GET.get('gwt2')=="true":
            filters.append('gwt2')

            if request.GET.get('gwt3') and request.GET.get('gwt3')=="true":
                filters.append('gwt3')

                if request.GET.get('gwt4') and request.GET.get('gwt4')=="true":
                    products = diamond_wt_filtered.filter(Q(gold_weight__gte=2.51, gold_weight__lte=3.50) | Q(gold_weight__gte=3.51, gold_weight__lte=5.0) | Q(gold_weight__gte=5.01))
                    filters.append('gwt4')
                else:
                    products = diamond_wt_filtered.filter(Q(gold_weight__gte=2.51, gold_weight__lte=3.50) | Q(gold_weight__gte=3.51, gold_weight__lte=5.0))


            else:
                if request.GET.get('gwt4') and request.GET.get('gwt4')=="true":
                    products = diamond_wt_filtered.filter(Q(gold_weight__gte=2.51, gold_weight__lte=3.50) | Q(gold_weight__gte=5.01))
                    filters.append('gwt4')
                else:
                    products = diamond_wt_filtered.filter(gold_weight__gte=2.51, gold_weight__lte=3.50)

        else:
            if request.GET.get('gwt3') and request.GET.get('gwt3')=="true":
                filters.append('gwt3')

                if request.GET.get('gwt4') and request.GET.get('gwt4')=="true":
                    products = diamond_wt_filtered.filter(Q(gold_weight__gte=3.51, gold_weight__lte=5.0) | Q(gold_weight__gte=5.01))
                    filters.append('gwt4')
                else:
                    products = diamond_wt_filtered.filter(gold_weight__gte=3.51, gold_weight__lte=5.0)

            else:
                if request.GET.get('gwt4') and request.GET.get('gwt4')=="true":
                    products = diamond_wt_filtered.filter(gold_weight__gte=5.01)
                    filters.append('gwt4')
                else:
                    pass

    if request.GET.get('search') and (request.GET.get('search')!="" or request.GET.get('search')!=""):
        products = products.filter(name__icontains=request.GET.get('search'))
        keyword = request.GET.get('search')


    for product in products:
        products_with_images[product] = ProductImage.objects.filter(product=product)[:2]
    
    for item in WishlistItem.objects.filter(owner=request.user.wishlist):
        wishlist.append(item.item)

    json_filters = dumps(filters)

    return render(request, "webapp/products.html", {"title": "Products", "products": products_with_images, "wishlist": wishlist, 'filters': json_filters, 'filterNo': len(filters), 'keyword': keyword})

@login_required(login_url='login')
def product(request, sku):
    product = Product.objects.get(sku=sku)
    images = ProductImage.objects.filter(product=product)
    wishlist = False
    if WishlistItem.objects.filter(owner=request.user.wishlist, item=sku):
        wishlist = True
    return render(request, "webapp/product.html", {"product": product, "images": images, "wishlist": wishlist})

@login_required(login_url='login')
def wishlist(request):
    wishlist = {}
    for item in WishlistItem.objects.filter(owner=request.user.wishlist):
        image_date = {}
        image_date[ProductImage.objects.filter(product=Product.objects.get(sku=item.item), default=True)[0]] = item.date_added
        wishlist[Product.objects.get(sku=item.item)] = image_date
    return render(request, "webapp/wishlist.html", {'title': "Wishlist", 'wishlist': wishlist})

@login_required(login_url='login')
def addWishlist(request, sku):
    if not WishlistItem.objects.filter(owner=request.user.wishlist, item=sku):
        item = WishlistItem()
        item.owner = request.user.wishlist
        item.item = sku
        item.date_added = date.today()
        item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/products'))

@login_required(login_url='login')
def removeWishlist(request, sku):
    if not WishlistItem.objects.filter(owner=request.user.wishlist, item=sku):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/products'))
    else:
        WishlistItem.objects.filter(owner=request.user.wishlist, item=sku).delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/products'))

@login_required(login_url='login')
def sendWishlist(request):
    if request.method=="POST":
        user = User.objects.get(username=request.user.username)
        diamond_quality = request.POST['diamond_quality']
        gold_purity = request.POST['gold_purity']
        gold_color = request.POST['gold_color']

        wishlist = Wishlist.objects.get(user=request.user)
        wishlist.diamond_quality = diamond_quality
        wishlist.gold_purity = gold_purity
        wishlist.gold_color = gold_color
        wishlist.date_submitted = date.today()
        wishlist.save()

        subject = f'Quotation Request from: {user.first_name} {user.last_name}'
        message = f' Wishlist Submitted for Quotation by {user.first_name} {user.last_name} on {wishlist.date_submitted}\n\n \
Username: {user.username}\n \
Phone: {user.user_profile.phone}\n \
Email ID: {user.email}\n \
Organisation: {user.user_profile.company_name}     {user.user_profile.role_in_organisation}     {user.user_profile.location}\n \
Company Website: {user.user_profile.website}\n\n \
Diamond Quality Requested: {wishlist.diamond_quality}\n \
Gold Purity Requested: {wishlist.gold_purity}\n \
Gold Color Requested: {wishlist.gold_color}\n\n \
-----------------WISHLISTED ITEMS----------------- \n\n'

        for item in WishlistItem.objects.filter(owner=request.user.wishlist):
            message = message + f'{item.item}\n'

        message = message + '\n\n---------------------------------------------------'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['soareslance10@gmail.com',]
        print(message)
        #send_mail( subject, message, email_from, recipient_list )

        return render(request, 'webapp/confirmation.html', {'title': 'Wishlist Recieved'})
    else:
        return redirect(reverse("wishlist"))