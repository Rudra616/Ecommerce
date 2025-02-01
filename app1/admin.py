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


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'qty', 'totalprice', 'status', 'datetime','state')
    list_filter = ('status', 'datetime')
    search_fields = ('user__name', 'product__name')
    actions = ['mark_as_completed', 'mark_as_cancelled']

    def mark_as_completed(self, request, queryset):
        queryset.update(status='Completed')
    mark_as_completed.short_description = "Mark selected orders as Completed"

    def mark_as_cancelled(self, request, queryset):
        queryset.update(status='Cancelled')
    mark_as_cancelled.short_description = "Mark selected orders as Cancelled"
admin.site.register(order,OrderAdmin)


class cart_(admin.ModelAdmin):
    list_display=['userid','productid','qty','totalprice','orderid']
admin.site.register(cart,cart_)

class product_(admin.ModelAdmin):
    list_display=['name','description','image','price','STOCK','Category']
admin.site.register(Product,product_)