from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from main.models import *
import bcrypt
from django.conf import settings

def index(request):
    if "user_id" in request.session:
        return redirect('/dashboard')

    return render(request,'login_reg.html')

def register(request):
    errors = User.objects.validator(request.POST)
    if len(errors)>0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect('/')

    pw = request.POST['password']
    pw_hash = bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()

    new_user = User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        usertype = request.POST['usertype'],
        aboutyou = request.POST['aboutyou'],
        email = request.POST['email'],
        password = pw_hash,
    )

    request.session['user_id'] = new_user.id

    return redirect('/dashboard')

def login(request):

    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
            return redirect('/dashboard')
        
        messages.error(request, "That password does not match that email.")
        return redirect('/')

    messages.error(request, "Please check your email and password.")
    return redirect('/')

def dashboard_page(request):
    if 'cart_id' not in request.session:
        cart = Cart.objects.create(total=0)
        request.session['cart_id']=cart.id
    if "user_id" not in request.session:
        messages.error(request, "You must be logged in to view that page.")
        return redirect('/')
    context={
        "user":User.objects.get(id = request.session['user_id']),
        "artists":User.objects.filter(usertype="Viewer/Seller")
    }
    return render(request,'dashboard.html', context)


def logout(request):
    request.session.pop("user_id")

    return redirect('/')

def handle_uploaded_file(f, file_name):
    with open(file_name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def process_profile_pic(request):
    user = User.objects.get(id=request.session["user_id"])
    filename = f"user_{user.id}.jpg"

    user.image = filename
    user.save()

    handle_uploaded_file(request.FILES["profile_image"], f"{settings.MEDIA_ROOT}/profile_image/{filename}")

    return redirect("/editmyprofile")


def edit_profile_page(request):
    if "user_id" not in request.session:
        messages.error(request, "You must be logged in to view that page.")
        return redirect('/')
    context={
        "user":User.objects.get(id = request.session['user_id'])
    }
    return render(request,'editprofile.html', context)

def process_update_profile(request):
    user = User.objects.get(id = request.session['user_id'])
    user.usertype = request.POST['usertype']
    user.aboutyou = request.POST['aboutyou']
    user.save()

    return redirect("/editmyprofile")

def new_mp_page(request):
    if "user_id" not in request.session:
        messages.error(request, "You must be logged in to view that page.")
        return redirect('/')
    context={
        "user":User.objects.get(id = request.session['user_id'])
    }
    return render(request,'newmp_page.html',context)


def edit_mp_page(request):
    if "user_id" not in request.session:
        messages.error(request, "You must be logged in to view that page.")
        return redirect('/')
    context={
        "user":User.objects.get(id = request.session['user_id']),
        "item":Item.objects.get(id = request.session['item_id'])
    }
    return render(request,'edit_mp_page.html',context)


def process_newmp_info(request):
    errors = Item.objects.validator(request.POST)
    if len(errors)>0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect('/new_masterpiece')

    item = Item.objects.create(
        title = request.POST['title'],
        description = request.POST['description'],
        price = request.POST['price'],
        creator = User.objects.get(id=request.session['user_id'])
    )
    request.session['item_id'] = item.id
    return redirect('/edit_masterpiece')

def update_mp_info(request):
    item = Item.objects.get(id = request.session['item_id'])
    item.title = request.POST['title']
    item.description = request.POST['description']
    item.price = request.POST['price']
    item.save()

    return redirect("/edit_masterpiece")

def process_newmasterpiece_pic(request):
    item = Item.objects.get(id=request.session["item_id"])
    filename = f"item_{item.id}.jpg"

    item.image = filename
    item.save()

    handle_uploaded_file(request.FILES["item_pic"], f"{settings.MEDIA_ROOT}/item_pic/{filename}")

    return redirect("/edit_masterpiece")

def see_artist_page(request, artist_id):
    context={
        "user":User.objects.get(id = request.session['user_id']),
        "artist":User.objects.get(id = artist_id),
        "item":Item.objects.filter(creator = artist_id)
    }
    return render(request,'artist_with_items_page.html', context)

def edit_item_page(request, item_id):
    context={
        "user":User.objects.get(id = request.session['user_id']),
        "item":Item.objects.get(id = item_id)
    }
    return render(request,'edit_item_page.html', context)

def process_update_item(request, item_id):
    item = Item.objects.get(id = request.session['item_id'])
    item.title = request.POST['title']
    item.description = request.POST['description']
    item.price = request.POST['price']
    item.save()
    return redirect(f'/viewmasterpiece/{item_id}')

def process_update_masterpiece_pic(request, item_id):
    item = Item.objects.get(id=request.session["item_id"])
    filename = f"item_{item.id}.jpg"

    item.image = filename
    item.save()

    handle_uploaded_file(request.FILES["item_pic"], f"{settings.MEDIA_ROOT}/item_pic/{filename}")

    return redirect(f'/viewmasterpiece/{item_id}')

def see_viewmasterpiece_page(request,item_id):
    if "user_id" not in request.session:
        messages.error(request, "You must be logged in to view that page.")
        return redirect('/')
    context={
        "user":User.objects.get(id = request.session['user_id']),
        "item":Item.objects.get(id = item_id)
    }
    return render(request,'view_masterpiece_page.html', context)

def process_delete(request, item_id):
    item = Item.objects.get(id= item_id)
    item.delete()
    return redirect ('/dashboard')

def start(request):
    return render(request,'start.html')

def cart(request):
    if 'cart_id' not in request.session:
        cart = Cart.objects.create(total=0)
        request.session['cart_id']=cart.id
    context = {
        'cart': Cart.objects.get(id=request.session['cart_id']),
        "user":User.objects.get(id = request.session['user_id']),
    }
    return render(request, 'cart.html', context)

def refresh_cart_total(cart):
    total = 0
    for item in cart.cart_items.all():
        total+= item.item.price
    cart.total = total
    cart.save()

def remove_from_cart(request, item_id):
    item = Item.objects.get(id=item_id)
    cart = Cart.objects.get(id=request.session['cart_id'])
    cart_item = CartItem.objects.create(item=item, cart=cart)

    refresh_cart_total(cart)

    return redirect('/cart')

def add_to_cart(request, item_id):
    item = Item.objects.get(id=item_id)
    cart = Cart.objects.get(id=request.session['cart_id'])
    cart_item = CartItem.objects.create(item=item, cart=cart)

    refresh_cart_total(cart)

    return redirect('/cart')