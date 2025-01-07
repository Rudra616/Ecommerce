from django.shortcuts import render,HttpResponse,redirect
from .models import UserRegister,Category,Product,order,cart

import razorpay
def first(request):
    return HttpResponse("This is my first web page!")   

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
            if useremail.password == request.POST['password']:
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
                # return redirect('second')
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
    
def products(request,id):
    if 's_email' in request.session:
        logindetails=UserRegister.objects.get(email= request.session['s_email'])
        prodata=Product.objects.get(id=id)
        if 'buy' in request.POST:
            if prodata.STOCK <= 0:
                return render(request,'details.html',{"session":True})
            else:
                if int(request.POST['qty']) > int(prodata.STOCK):
                    return render(request,'details.html',{"session":True})
                else:
                    request.session['proid']=prodata.pk
                    request.session['buyqty']=request.POST['qty']
                    return redirect('checkout')
        elif 'cart' in request.POST:
       
            cartdata=cart()
            cartdata.productid=prodata.pk
            cartdata.userid=logindetails.pk
            cartdata.qty=request.POST['qty']
            cartdata.totalprice=int(prodata.price) * int(request.POST['qty'])
            already_cart = cart.objects.filter(productid=id,userid=logindetails.id)
            if already_cart:
                return render(request,'index.html',{'pro':prodata,'session':True ,'already':'already in cart'})
            else:
                cartdata.save()
                return render(request,'index.html',{'pro':prodata,'session':True ,'store':'store in cart'})

        else:
            return render(request,'details.html',{'pro':prodata,'session':True})
    else:
        return redirect('login')
        # prodata=Product.objects.get(id=id)
        # return render(request,'details.html',{'pro':prodata})
 

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
            return render(request, 'profile.html', {'user':user})
        else:
            return render(request, 'profile.html', {'user':user})
    else:
        return redirect('login')
    
def checkout(request):
    if 's_email' in request.session:
        userRegister=UserRegister.objects.get(email = request.session['s_email'])
        pro=Product.objects.get(id=request.session['proid'])
        Qty=request.session['buyqty']
        total= int(pro.price) * int(Qty)
        if request.method=='POST':
            ordata=order()
            ordata.productid=pro.id
            ordata.userid=userRegister.pk
            
            ordata.add=request.POST['addres']
            ordata.city=request.POST['country']
            ordata.state=request.POST['state']
            ordata.pincode=request.POST['pincode']
            ordata.totalprice=total
            ordata.qty=Qty
            ordata.paytype=request.POST['option']
            ordata.transactionid="1"
            # clint=razorpay.Client(auth=())
            ordata.save()
            return render(request,"confrom.html",{'conform':'confrom your order'})
        else:
            return render(request,"checkout.html",{'session':True,'user':userRegister,'pro':pro,'Qty':Qty,'total':total})  
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
            prodict ={'proimg':pro.image
                      ,'proname':pro.name
                      ,'proprice':pro.price
                      ,'totalprice':i.totalprice
                      ,'qty':i.qty}
            prolist.append(prodict)
        return render(request,'cart.html',{'userR':True,'prolist':prolist})
    return render(request,"login.html")
