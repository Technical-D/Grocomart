from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse, JsonResponse
from app.forms import SignupForm, AccountAuthenticationForm, NewsletterForm, QueriesForm
from app.models import Customer, Product, OrderItem, Order, ShippingAddress
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib import messages
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from app.utils import generate_token
import json
import stripe
import datetime
# Create your views here.


stripe.api_key = settings.STRIPE_SECRET_KEY



def cart(r):
    if r.user.is_authenticated:
        customer = r.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        return order


def index(request):
    products = Product.objects.all()[:9]
    order = cart(request)
    return render(request, 'app/index.html', {'products':products, 'order':order})

def login_view(request):
    user = request.user
    if user.is_authenticated: 
        return redirect("index")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect("index")
    else:
        form = AccountAuthenticationForm()

    return render(request, 'registration/login.html', {'login_form':form})

def logout_view(request):
	logout(request)
	return redirect("index")


def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    email_body = render_to_string('registration/activate.txt', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })

    admin_email = settings.EMAIL_HOST_USER
    try:
        send_mail(email_subject, email_body, admin_email , [user.email], fail_silently=False)
    except BadHeaderError:
        return HttpResponse('Invalid header found.')


def signup_view(request):
    user = request.user

    if user.is_authenticated:
        return redirect('index')
    
    context = {}
    if request.POST:
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            u = Customer.objects.get(email=email)
            send_activation_email(u, request)
            return render(request, 'registration/activation_email_sent.html', {})
        else:
            context['signup_form'] = form

    else:
        form = SignupForm()
    
    return render(request, 'registration/signup.html', {'signup_form':form})

def profile(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        customer = Customer.objects.get(pk=user_id)
        address = ShippingAddress.objects.filter(customer=customer).values()
        order_detail = Order.objects.filter(customer=customer, complete=True)
        print(order_detail)
    else:
        return redirect('login')
    order = cart(request)
    return render(request, 'app/profile.html', {'customer':customer, 'order':order, 'address':address, 'order_detail':order_detail})

def product_view(request, id):
    product_id = id
    product = Product.objects.get(pk=product_id)
    order = cart(request)
    return render(request, 'app/product.html', {'product':product, 'order':order})

def products(request):
    products = Product.objects.all()
    order = cart(request)
    return render(request, 'app/products.html', {'products':products, 'order':order})

def category(request):
    vegetables = Product.objects.filter(category='vegetables').all()
    fruits = Product.objects.filter(category='fruits').all()
    dairy = Product.objects.filter(category='dairy').all()
    oils = Product.objects.filter(category='edible oils').all()
    snacks = Product.objects.filter(category='snacks').all()
    grains = Product.objects.filter(category='grains').all()
    pulses = Product.objects.filter(category='pulses').all()
    biscuits = Product.objects.filter(category='biscuits').all()

    order = cart(request)
    context = {'vegetables':vegetables, 'fruits':fruits, 'dairy': dairy, 'oils':oils,'snacks':snacks,'grains':grains,'pulses':pulses,'biscuits':biscuits, 'order':order}

    return render(request, 'app/category.html', context)


def categories_view(request, name):
    category  = name
    p = Product.objects.filter(category=category).all()
    order = cart(request)

    return render(request, 'app/categories.html', {'products':p, 'category':category, 'order':order})

def cart_view(request):

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_item
    else:
        return redirect('login')
    context ={'items':items, 'order':order, 'cartItem':cartItem}
    return render(request, 'app/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_item
        address = ShippingAddress.objects.filter(customer=customer).values()
        amount = int(order.get_cart_total * 100)
        key = settings.STRIPE_PUBLISH_KEY

    else:
        return redirect('login')

    context ={'items':items, 'order':order, 'cartItem':cartItem, 'address':address, 'amount':amount, 'key':key}

    return render(request, 'app/checkout.html', context)

def process_payment(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            customer = request.user
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
            amount = int(order.get_cart_total * 100)
            address = ShippingAddress.objects.filter(customer=customer).values()
            
            stripe.PaymentIntent.create(
                amount=amount,
                currency="inr",
                payment_method_types=["card"],
            )

            order.transaction_id = datetime.datetime.now().timestamp()
            order.complete = True
            order.date_completed = datetime.date.today()
            order.save()

    return render(request, 'payment/payment_status.html', {'order':order, 'customer':customer,'address':address, 'items':items })

def invoice(request, id):
    order_id = id
    if request.user.is_authenticated:
        customer = request.user
        order= Order.objects.get(pk=order_id)
        items = order.orderitem_set.all()
        address = ShippingAddress.objects.filter(customer=customer).values()


    return render(request, 'payment/invoice.html', {'order':order, 'address':address, 'customer':customer, 'items':items})


def shipping_address(request):
    customer = request.user
    if request.POST:
            add = request.POST['address']
            land = request.POST['landmark']
            state = request.POST['state']
            city = request.POST['city']
            zcode = request.POST['zipcode']
            c = ShippingAddress.objects.create(customer=customer, address=add, landmark=land, state=state, city=city, zipcode=zcode)
            c.save()
            return redirect('checkout')

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity -1)
    
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item added!', safe=False)




def contact(request):
    context ={}
    if request.POST:
        if request.user.is_authenticated:

            form = QueriesForm(request.POST)
            if form.is_valid():
                form.save()
                return render(request, 'app/sent.html')
            else:
                context['contact_form'] =form
        else:
            return HttpResponse('Please Login to send query!!')
    else:
        form = QueriesForm()

    order = cart(request)
    
    return render(request,'app/contact.html', {'contact_form':form, 'order':order})

def about(request):
    order = cart(request)
    return render(request, 'app/about.html', {'order':order})

def newsletter(request):
    if request.POST:
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'app/newsletter.html')






def password_reset_request(request):
    if request.method == 'POST':
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = Customer.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = 'Password Reset Requested'
                    email_template_name = 'password/password_reset_email.txt'
                    c = {
                        "email":user.email,
                        'domain':'127.0.0.1:8000',
                        'site_name': 'Grocomart',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    admin_email = settings.EMAIL_HOST_USER
                    try:
                        send_mail(subject, email, admin_email , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect ("password_reset_done")
            
            messages.error(request, 'Email is not registered!')
            return redirect('password_reset')

    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})



def activate_user(request, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))

        user = Customer.objects.get(pk=uid)

    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_active = True
        user.save()

        return render(request, 'registration/verified.html', {})

    return render(request, 'registration/activate_failed.html', {"user": user})
