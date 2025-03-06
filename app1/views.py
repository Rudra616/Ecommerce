from django.shortcuts import render,HttpResponse,redirect
from .models import UserRegister,Category,Product,order,cart

from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib import messages

from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from django.conf import settings
import uuid



def add_product(request):
    if 's_email' in request.session:
     
        if request.method == "POST":
            name = request.POST["productName"]
            description = request.POST["description"]
            price = request.POST["price"]
            category_id = request.POST["category"]
            stock = request.POST["stock"]
            image = request.FILES["productImage"]

            category = Category.objects.get(id=category_id)

            product = Product.objects.create(
                name=name, 
                description=description,
                price=price,
                Category=category,
                STOCK=stock, 
                image=image,
                is_approved=False
            )
            messages.success(request, "Your product request has been sent for approval.")
            return redirect("add_product")

        categories = Category.objects.all()
        return render(request, "add_product.html", {"categories": categories})
    else:
        return redirect('login')


# Create your views here.
from django.core.mail import send_mail
from django.conf import settings
def reg(request):
    if request.method == 'POST':
        regdata = UserRegister()
        regdata.name = request.POST['name']
        regdata.password = request.POST['password']
        regdata.email = request.POST['email']
        regdata.mob = request.POST['phone']
        regdata.add = request.POST['add']
        
        useralready = UserRegister.objects.filter(email = request.POST['email'])
        # if useralready:
        if len(useralready) > 0:  
            return render(request, 'reg.html', {'already':'Email already exists!!!'})
        else:
            if request.POST['password']==request.POST['Confirmpassword']:
                regdata.save()
                send_mail(
                    'welcome message from our website',
                    'This is an authication email',
                    'settings.EMAIL_HOST_USER',
                    [regdata.email],
                    fail_silently=False 
                )
            else:
                return render(request, 'reg.html', {'cp':'try again'})

        return render(request, 'reg.html', {'store':'Data has been entered successfully!'})
    else:
        return render(request, 'reg.html')
import random
def login(request):
    if request.method == 'POST':
        try:
            useremail = UserRegister.objects.get(email = request.POST['email'])
            if useremail.password.strip() == request.POST['password'].strip():
                request.session['s_email'] = useremail.email
                otp =random.randint(100000,999999)
                request.session['otp']=otp
                send_mail(
                    'welcome',
                    f'Your OTP for login of ecommerce is {otp}',
                    'rudrampanchal@gmail.com',
                    [useremail.email],
                    fail_silently=False 
                )
                return redirect('otp')
            else:
                return render(request,'login.html', {'password': 'Incorrect password!'})

        except:
            return render(request,'login.html', {'email': 'Email does not exist!'})    
    else:
        return render(request, 'login.html')
    
    
def logout(request):
    del request.session['s_email']
    return redirect('second')

def second(request):
    if 's_email' in request.session:
        catdata = Category.objects.all()
        return render(request, 'index.html', {'cat':catdata, 'session':True})
    else:
        catdata = Category.objects.all()
        return render(request, 'index.html', {'cat':catdata})

def catpro(request,id):
    if 's_email' in request.session:
        prodata=Product.objects.filter(Category=id)
        return render(request,'catpro.html',{'pro1':prodata,'session':True})
    else:
        return redirect('login')
        # try:
        #     prodata=Product.objects.filter(Category=id)
        #     return render(request,'login.html',{'pro1':prodata})
        # except:
        #     return render(request,'login.html', {'email': 'Email does not exist!'})    
def products(request, id):
    if 's_email' in request.session:
        logindetails = UserRegister.objects.get(email=request.session['s_email'])
        prodata = Product.objects.get(id=id)

        if 'buy' in request.POST:
            requested_qty = int(request.POST['qty'])
            available_stock = int(prodata.STOCK)

            # Check stock availability
            if available_stock <= 0 or requested_qty > available_stock:
                return render(request, 'details.html', {
                    "session": True, 
                    'out': 'Out of stock', 
                    'pro': prodata
                })                              
            else:
                # Store product and quantity in session for checkout
                request.session['proid'] = prodata.pk
                request.session['buyqty'] = requested_qty

                # Deduct stock after purchase
                prodata.STOCK -= requested_qty
                prodata.save()

                return redirect('checkout')

        elif 'cart' in request.POST:
            requested_qty = int(request.POST['qty'])

            # Check if requested quantity is available in stock
            if requested_qty > prodata.STOCK:
                return render(request, 'details.html', {
                    "session": True, 
                    'out': 'Not enough stock available', 
                    'pro': prodata
                })

            # Check if the product is already in the cart
            already_cart = cart.objects.filter(productid=id, userid=logindetails.id)
            if already_cart.exists():
                return render(request, 'index.html', {
                    'pro': prodata, 
                    'session': True, 
                    'already': 'Already in cart'
                })

            # Add to cart
            cartdata = cart()
            cartdata.productid = prodata.pk
            cartdata.userid = logindetails.pk
            cartdata.qty = requested_qty
            cartdata.totalprice = int(prodata.price) * requested_qty
            cartdata.save()

            return render(request, 'index.html', {
                'pro': prodata, 
                'session': True, 
                'store': 'Stored in cart'
            })

        else:
            return render(request, 'details.html', {'pro': prodata, 'session': True})

    else:
        return redirect('login')
 

def profile(request):
    if 's_email' in request.session:
        user=UserRegister.objects.get(email = request.session['s_email'])
        if request.method == 'POST':
            user.name = request.POST['name']
            user.email = request.POST['email']
            user.add = request.POST['Add']
            user.mob = request.POST['mob']
            user.password = request.POST['password']
            user.save()
            return render(request, 'index.html', {'user':user})
        else:
            return render(request, 'profile.html', {'user':user})
    else:
        return redirect('login')

import json
from django.shortcuts import get_object_or_404

from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
import uuid
from .models import UserRegister, order

def payment_success(request):
    
    user_email = request.session.get('s_email')
    total_s=request.session['total_s']
    if not user_email:
        return HttpResponse("Email parameter missing", status=400)

    print(f"Searching for user with email: {user_email}")
    user = UserRegister.objects.get(email=user_email)

    order_id = request.session.get('order_id')
    if order_id:
        order_data = get_object_or_404(order, id=order_id)
        order_date = order_data.order_placed  
        ordernumber = uuid.uuid4().int 

        print(ordernumber)
        print(order_date)

        send_mail(
            'Success',
            f'Dear {user.name},\n\n'
            f'Thank you for placing an order with MYSHOP. We are pleased to confirm '
            f'the receipt of your order {ordernumber}, dated {order_date}. '
            f'Your order is now being processed and we will ensure its prompt dispatch.\n\n'
            'Best regards,\n'
            'MYSHOP Team',
            'rudrampanchal@gmail.com',
            [user_email],
            fail_silently=False
        )

        # send_mail(
        #     'payment success',
        #     f'paypal{total_s}',
        #     'MYSHOP Team',
        #     'rudrampanchal@gmail.com',
        #     [user_email],
        #     fail_silently=False
        # )
        # print(total_s)

        order_data.status = "Completed"  # Mark as completed
        order_data.save()  # Save order status
        del request.session['order_id']  # Remove session key

    return render(request, "payment_success.html", {})

def payment_failed(request):
    return render(request, "payment_failed.html", {})

def checkout(request):
    if 's_email' in request.session:
        user = UserRegister.objects.get(email=request.session['s_email'])
        product = Product.objects.get(id=request.session['proid'])
        qty = int(request.session['buyqty'])
        total = int(product.price) * qty
        request.session['total_s']=total

        notify_url = request.build_absolute_uri(reverse('paypal-ipn'))
        return_url = request.build_absolute_uri(reverse('payment_success'))
        cancel_url = request.build_absolute_uri(reverse('payment_failed'))

        paypal_dict = {
            'business': 'busness@ggmail.com',
            'amount': str(total),
            'item_name': product.name,
            'invoice': str(uuid.uuid4()),
            "notify_url": notify_url,
            "return_url": return_url,
            "cancel_url": cancel_url,   'cmd': '_xclick',
            'currency_code': 'USD',  # Force USD to avoid issues
            'no_shipping': '1',
            'no_note': '1',
            'bn': 'PP-BuyNowBF',
            'custom': user.id,
}
        print("AA")
        print("PayPal Data JSON:", json.dumps(paypal_dict, indent=4))

        if request.method == 'POST':
            order_data = order()
            order_data.user = user
            order_data.product = product
            order_data.add = request.POST['addres']
            order_data.city = request.POST['country']
            order_data.state = request.POST.get('state', '')
            order_data.pincode = request.POST['pincode']
            order_data.qty = qty
            order_data.totalprice = total
            order_data.paytype = request.POST['option']

            if request.POST['option'] == 'online':
                order_data.transactionid = str(uuid.uuid4())
                order_data.status = "Pending Payment"
                order_data.save() 
    
                request.session['order_id'] = order_data.id 
 
                return render(request, "paypal_redirect.html", {'paypal_dict': paypal_dict})
            else:
                order_data.transactionid = str(uuid.uuid4())
                order_data.status = "Pending"
            
                user_email = request.session.get('s_email')

                if not user_email:
                    return HttpResponse("Email parameter missing", status=400)

                print(f"Searching for user with email: {user_email}")
                user = UserRegister.objects.get(email=user_email)

                send_mail(
                    'Success',
                    f'Dear {user.name},\n\n'
                    f'Thank you for placing an order with MYSHOP. We are pleased to confirm '
                    f'the receipt of your order'
                    f'Your order is now being processed and we will ensure its prompt dispatch.\n\n'
                    'Best regards,\n'
                    'MYSHOP Team',
                    'rudrampanchal@gmail.com',
                    [user_email],
                    fail_silently=False
                )
                order_data.save()
                return render(request, "confrom.html")
            

        return render(request, "checkout.html", {'session': True, 'user': user, 'product': product, 'qty': qty, 'total': total})
    else:
        return redirect('login')




def otp(request):
    if request.method == 'POST':
        if int(request.session['otp'])==int(request.POST['otp']):
            return redirect('second')
        else:
            return render(request,'otp.html',{'invalid':"the otp you enter does not match"})
    else:
        return render(request,'otp.html')
        
def cartdata(request):
    if 's_email' in request.session:
        prolist=[]
        userR=UserRegister.objects.get(email = request.session['s_email'])
        catpro=cart.objects.filter(userid=userR.id)
        for i in catpro:
            pro = Product.objects.get(id=i.productid)
            prodict = {'proimg':pro.image
                      ,'proname':pro.name
                      ,'proprice':pro.price
                      ,'totalprice':i.totalprice
                      ,'qty':i.qty,
                        'id': pro.id,  
                    }
            prolist.append(prodict)
        return render(request,'cart.html',{'userR':True,'prolist':prolist})
    return render(request,"login.html")
    


def remove_item(request,id):
    try:
        the_id = request.session['cart_id']
        Cart = cart.objects.get(id= the_id)
    except:
        return render(request,'cart.html')
    cartitem = cart.objects.get(id=id)
    cartitem.delete()

def order_history(request):
    if 's_email' in request.session:
        user = UserRegister.objects.get(email=request.session['s_email'])
        orders = order.objects.filter(user=user).order_by('-order_placed')
        return render(request, 'order_histroy.html', {'orders': orders})
    else:
        return redirect('login')

def product_search(request):
    if request.method == "POST":
        searched = request.POST.get('searched')
        # searched = request.POST.get('searched', '') 
        return render(request,'search_results.html',{'searched':searched})  
    else:
        return render(request,'search_results.html')  

    # query = request.GET.get('q')  # Get search query from URL
    # if query:
    #     products = Product.objects.filter(name__icontains=query)  # Filter products by name
    # else:
    #     products = Product.objects.all()  # Show all products if no search

    # return render(request, 'search_results.html', {'products': products, 'query': query})


def product_list(request):
    products = Product.objects.filter(is_approved=True)  # Show only approved products
    return render(request, "product_list.html", {"products": products})

from django.http import JsonResponse

def debug_request(request):
    return JsonResponse(dict(request.META))
from django.contrib.auth import get_user_model
from django.http import HttpResponse

def create_superuser(request):
    User = get_user_model()
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@example.com", "admin123")
        return HttpResponse("Superuser created successfully. Now remove this URL!")
    else:
        return HttpResponse("Superuser already exists.")
from django.core.management import call_command

def run_migrations(request):
    try:
        call_command("migrate")
        return JsonResponse({"status": "success", "message": "Migrations applied!"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})

from django.http import HttpResponse

def check_session(request):
    if "test_key" not in request.session:
        request.session["test_key"] = "Hello, Session!"
    return HttpResponse(f"Session Key: {request.session.session_key}, Data: {request.session.get('test_key')}")
