from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Product, Customer, Cart, Payment, Order, Wishlist
from django.db.models import Q
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.http import JsonResponse





def home(request):
    return render(request, "app/home.html")

def about(request):
    return render(request, "app/about.html")

def contact(request):
    return render(request, "app/contact.html")

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', locals())
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sveikiname, Jūs sėkmingai užsiregistravote!')
        else:
            messages.warning(request, 'Atsiprašome, bet įvyko klaida. Bandykite dar kartą.')
        return render(request, 'app/customerregistration.html', locals())

class ProfileView(View):
    def get(self, request):
        user_profile, created = Customer.objects.get_or_create(user=request.user)
        form = CustomerProfileForm(instance=user_profile)  # Pass the user's profile as an instance
        return render(request, 'app/profile.html', {'form': form})

    def post(self, request):
        user_profile, created = Customer.objects.get_or_create(user=request.user)
        form = CustomerProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Jūsų profilis buvo sėkmingai atnaujintas!')
        else:
            messages.warning(request, 'Atsiprašome, bet įvyko klaida. Bandykite dar kartą.')
        return render(request, 'app/profile.html', {'form': form})


class CategoryView(View):
    def get(self, request, val):
        product = Product.objects.filter(category=val)
        return render(request, "app/category.html",locals())

class CategoryTitle(View):
    def get(self, request, val):
        product = Product.objects.filter(title=val)
        category_titles = product.values_list('category__title', flat=True).distinct()
        return render(request, "app/category.html", {"category_titles": category_titles})


class ProductDetailView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        return render(request, "app/product_detail.html", {"product": product})

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    cart_item, created = Cart.objects.get_or_create(
        product=product,
        user=user,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('/cart')

@login_required
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
        totalamount = amount
    return render(request, "app/addtocart.html", locals())

def plus_cart(request):
    if request.method == 'GET':
            product_id = request.GET['prod_id']
            c = Cart.objects.get(Q(product=product_id) & Q(user=request.user))
            c.quantity += 1
            c.save()
            user = request.user
            cart = Cart.objects.filter(user=user)
            amount = 0
            for p in cart:
                value = p.quantity * p.product.discounted_price
                amount = amount + value
            totalamount = amount
            data={
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': totalamount

            }
            return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
            product_id = request.GET['prod_id']
            c = Cart.objects.get(Q(product=product_id) & Q(user=request.user))
            c.quantity -= 1
            c.save()
            user = request.user
            cart = Cart.objects.filter(user=user)
            amount = 0
            for p in cart:
                value = p.quantity * p.product.discounted_price
                amount = amount + value
            totalamount = amount
            data={
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': totalamount

            }
            return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        product_id = request.GET['prod_id']
        c = Cart.objects.filter(Q(product=product_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount
        data = {
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)

class Checkout(LoginRequiredMixin,View):
    login_url = '/accounts/login/'
    def get(self, request):
        user=request.user
        cart_items=Cart.objects.filter(user=user)
        amount=0
        for p in cart_items:
            value=p.quantity * p.product.discounted_price
            amount=amount+value
        totalamount=amount
        return render(request, "app/checkout.html", locals())

def checkout_view(request):
    if request.method == 'POST':
        user_profile_form = CustomerProfileForm(request.POST, instance=request.user)
        if user_profile_form.is_valid():
            user_profile_form.save()
            return redirect('checkout')
    else:
        user_profile_form = CustomerProfileForm(instance=request.user)
    return render(request, 'app/checkout.html', {'user_profile_form': user_profile_form})

def plus_wishlist(request):
    if request.method == 'GET':
        product_id = request.GET['product_id']
        product = Product.objects.get(id=product_id)
        user = request.user
        wishlist_entry, created = Wishlist.objects.get_or_create(user=user, product=product)
        if created:
            message = f'Produktas "{product.title}" pridėtas į pageidavimų sąrašą'
        else:
            wishlist_entry.delete()
            message = f'Produktas "{product.title}" pašalintas iš pageidavimų sąrašo'
        data = {
            'message': message,
            'type': 'success',
        }
        return JsonResponse(data)


# def minus_wishlist(request):
#     if request.method == 'GET':
#         product_id = request.GET['product_id']
#         product = Product.objects.get(id=product_id)
#         user = request.user
#         Wishlist.objects.filter(Q(user=user) & Q(product=product)).delete()
#         message = 'Produktas pašalintas iš pageidavimų sąrašo'
#         data = {
#             'message': message,
#             'type': 'success',
#             }
#         messages.success(request, message)
#         return JsonResponse(data)


def wishlist_products(request):
    wishlist_products = Wishlist.objects.filter(user=request.user).values_list('product', flat=True)
    products = Product.objects.filter(id__in=wishlist_products)
    return render(request, "app/wishlist_products.html", {'products': products})

def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, "app/address.html", locals())



def payment(request):
    return render(request, 'app/payment.html')

def payment_done(request):
    order_id = request.GET.get('order_id')
    payment_id= request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')
    user= request.user
    customer = Customer.objects.get(id=cust_id)
    payment = Payment.objects.get(stripe_order_id=order_id)
    payment.paid = True
    payment.stripe_payment_id = payment_id
    payment.save()
    cart=Cart.objects.filter(user=user)
    for c in cart:
        Order(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")


def orders(request):
    order_placed=Order.objects.filter(user=request.user)
    print(order_placed)
    print(request.user)
    return render(request, "app/orders.html", {'order_placed': order_placed})

def search_product(request):
    query = request.GET.get("query")
    search_results = Product.objects.filter(
        Q(product_id__icontains=query)
        | Q(product_description__icontains=query)
    )
    return render(
        request,
        template_name="app/search_products.html",
        context={"products": search_results, "query": query},
    )















# funkcija multiple failu ir nuotrauku ikelimui is kito pavyzdzio(html reiks pakeisti i home)

# def index(request):
#     if request.method == 'POST':
#         files = request.FILES.getlist('files')
#         new_file = Files(
#             file = request.FILES['name']
#         )
#         new_file.save()
#         # print('hi'+str(new_file.id))
#         #return redirect(new_file.file.url)
#         return render(request, 'index.html', {'new_url': str(new_file.file.url)})
#     else:
#         return render(request, 'index.html')
