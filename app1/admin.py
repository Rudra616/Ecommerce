from django.contrib import admin
from .models import UserRegister,Category,Product,order,cart
# Register your models here.

class userreg_(admin.ModelAdmin):
    list_display = ['id', 'name', 'email','password','mob', 'add']
    # def Confirm_password(self, obj):
    #     # Replace with actual logic to display password confirmation status
    #     return 'Confirmed' if obj.password == obj.password_confirmation else 'Not Confirmed'
    
admin.site.register(UserRegister, userreg_)


class category_(admin.ModelAdmin):
    list_display = ['catname', 'image']

admin.site.register(Category, category_)


class allproduct_(admin.ModelAdmin):
    list_display = ['name','description','image','STOCK','price','Category']
admin.site.register(Product,allproduct_)

class order_(admin.ModelAdmin):
    list_display = ['userid','productid','add','city','state','pincode','qty','totalprice','transactionid','paytype','datetime']
admin.site.register(order,order_)

class cart_(admin.ModelAdmin):
    list_display=['userid','productid','qty','totalprice','orderid']
admin.site.register(cart,cart_)