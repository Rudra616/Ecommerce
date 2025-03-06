from django.contrib import admin
from .models import UserRegister,Category,Product,order,cart
# Register your models here.

from django.utils import timezone

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
    # Display columns in the list view
    list_display = ('user', 'product', 'order_placed', 'order_complited', 'status', 'totalprice','paytype')

    # Filter options for the list view
    list_filter = ('status',)

    # Search options
    search_fields = ('user__email', 'product')

    # Make order_complited field editable in the form
    fields = ('user', 'product', 'order_placed', 'order_complited', 'status', 'totalprice')

    # Custom action to mark orders as completed
    def mark_as_completed(self, request, queryset):
        queryset.update(status='Completed', order_complited=timezone.now())  # Fixed typo in `order_complited`
    mark_as_completed.short_description = "Mark selected orders as Completed"

    # Custom action to mark orders as cancelled
    def mark_as_cancelled(self, request, queryset):
        queryset.update(status='Cancelled', order_complited=None)  # Set completed date to None
    mark_as_cancelled.short_description = "Mark selected orders as Cancelled"

    # Add custom actions to admin
    actions = [mark_as_completed, mark_as_cancelled]

# Register the model with the custom admin interface
admin.site.register(order, OrderAdmin)




class cart_(admin.ModelAdmin):
    list_display=['userid','productid','qty','totalprice','orderid']
    

admin.site.register(cart,cart_)

class product_(admin.ModelAdmin):
    list_display=['name','description','image','price','STOCK','Category']
    list_editable = ('STOCK',)  # Allows direct stock editing in the list view
    search_fields = ('name',)
    list_filter = ("is_approved","Category")
    actions = ["approve_products"]
    
    def approve_products(self,request,queryset):
        queryset.update(is_approved=True)
        self.message_user(request,"selected product have been approved")

admin.site.register(Product,product_)
