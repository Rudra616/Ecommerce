from django.db import models

# Create your models here.
class UserRegister(models.Model):
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField()
    mob = models.TextField()
    add = models.TextField()

    
    def __str__(self):
        return self.name
    
class Category(models.Model):
    catname = models.CharField(max_length=80)
    image = models.ImageField(upload_to='catimg')
    def __str__(self):
        return self.catname
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField()
    price = models.CharField(max_length=100)
    STOCK = models.PositiveSmallIntegerField()
    Category = models.ForeignKey(Category,on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)  # Admin approval required

   
    def __str__(self):
        return self.name
    
class order(models.Model):  # ✅ Capitalized "Order" for consistency
    user = models.ForeignKey(UserRegister, on_delete=models.CASCADE)  # ✅ Remove default='Pending'
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)  # ✅ Remove default='Pending'
    
    add = models.TextField(default='Pending')
    status = models.CharField(
        max_length=10, 
        choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], 
        default='Pending'
    )
    city = models.CharField(max_length=50, default='Pending')
    state = models.CharField(max_length=20, default='Pending')
    pincode = models.CharField(max_length=6, default='Pending')
    qty = models.CharField(max_length=6, default='Pending')
    totalprice = models.CharField(max_length=50, default='Pending')
    paytype = models.CharField(max_length=20, default='cash')
    transactionid = models.CharField(max_length=50, default='Pending')
    order_placed = models.DateTimeField(auto_now_add=True)
    order_complited = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f"Order {self.id} - {self.user.name if self.user else 'Unknown'}"    

    
class cart(models.Model):
    userid = models.CharField(max_length=100)
    productid = models.CharField(max_length=100)
    qty=models.PositiveBigIntegerField()
    totalprice=models.PositiveBigIntegerField()
    orderid=models.CharField(max_length=5,default="0")

    def __str__(self):
        return self.userid

