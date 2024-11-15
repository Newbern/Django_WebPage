from django.shortcuts import render, redirect
from .models import Account, ImageSlide, Part
from decimal import Decimal
import ast


# Getting Profile Image
def image(request):
    # Checking to see if they are logged in
    if request.user.is_authenticated:
        image = Account.objects.filter(user=request.user)[0].image.url

    # If Not then Going to image
    elif request.user.is_anonymous:
        image = "/media/AccountImages/Guest"
    else:
        image = None
    return image


# Home Page
def home(request):
    # Getting all the Images
    images_index = ImageSlide.objects.filter(name="MainPage")[0].get_images()

    return render(request, 'main/MainPage.html', {'Profile_Image': image(request), "Image_Slides": images_index})


# Account Page
def account(request):
    print(request.method)
    info = Account.objects.filter(user=request.user)[0]
    name = img = None
    if request.method == "POST":
        # Updating Name
        info.name = request.POST.get("name")

        # Updating Image
        if request.POST.get("img") != "":
            info.image.delete()
            info.image = request.FILES.get("img")

        # Saving
        info.save()
        return redirect('account')

    elif request.method == "GET":
        name = info.name
        img = info.image.url

    print(name)
    print(img)



    return render(request, "main/Account.html", {"Profile_Image": image(request), "name": name, "img": img})


# Cart
def cart(request):
    # Getting Account Cart
    info = Account.objects.filter(user=request.user)[0]
    cart = info.cart

    # If Item in Cart is 0 it will be erased
    for item in list(cart):
        if cart[item] == "0":
            cart.pop(item)

    # Saving Cart list
    info.save()

    # Getting Parts Data
    part_items = Part.objects.all()

    # Getting Selected Parts from cart
    parts_lst = []
    for item in list(cart):
        for part in part_items:
            if item == part.name:
                parts_lst.append(part)

    return render(request, 'main/Cart.html', {'Profile_Image': image(request), "cart": cart, "parts": parts_lst})


# Parts
def parts(request):
    items = Part.objects.all()
    # Showing all Parts
    print(f"User: {request.user}")

    # Getting The Requested Part
    if request.method == "GET":
        # Getting the Value of part
        part_item = request.GET.get('part')
        cart_num = request.GET.get('cart_num')
        print(f"Part: {part_item}")

        # Checking to see if a part was selected
        if part_item is not None and cart_num is None:

            print(f"None in Cart: {cart_num}")
            # Getting the part_items values
            parts = Part.objects.filter(name=part_item)[0]

            # Getting Count in Inventory
            count = Part.objects.filter(name=part_item)[0].stock

            # Going to The Specific Part Page
            return render(request, "main/Part_Item.html", {"Profile_Image": image(request), "part": parts, "Inventory": count})

        # Checking to see how much was added in Cart
        if cart_num is not None:
            if request.user.is_authenticated:
                # Getting Account
                info = Account.objects.filter(user=request.user)[0]

                # Updating Cart data
                new_cart = {f"{part_item}": f"{cart_num}"}
                info.cart.update(new_cart)

                # Saving Request
                info.save()

        else:
            print(f"None in Cart: {cart_num}")

    return render(request, 'main/Parts.html', {"Profile_Image": image(request), "items": items})


# Map
def map(request):
    return render(request, "main/Map.html", {"Profile_Image": image(request)})


# Total Price
def price(request):

    # Cart
    info = Account.objects.filter(user=request.user)[0]
    cart = info.cart
    # Updating Data
    if request.method == "POST":
        data = ast.literal_eval(request.POST.get("list"))
        info.cart.update(data)
        info.save()

    # Items in Cart
    quantity = [i for i in cart.values()]

    price = 0
    # Getting Price Total
    for item, amount in zip(cart, quantity):
        part = Part.objects.filter(name=item)[0]
        if part.name:
            # Turning the price string into a Decimal for precise amount
            moneys = Decimal(part.price.split("$")[1])
            price += moneys * Decimal(amount)

    # Collected Total
    price = "$" + str(price)

    return render(request, 'main/Price.html', {"Profile_Image": image(request), "total": price})


# Contacts
def contacts(request):
    return render(request, "main/Contacts.html", {"Profile_Image": image(request)})

