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
   
    def __str__(self):
        return self.name
    
class order(models.Model):
    userid = models.CharField(max_length=100)
    productid = models.CharField(max_length=100)
    add = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=20)
    pincode = models.CharField(max_length=6)
    qty = models.CharField(max_length=6)
    totalprice = models.CharField(max_length=50)
    paytype = models.CharField(max_length=20 ,default='cash')
    transactionid = models.CharField(max_length=50)
    datetime = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.userid
    
class cart(models.Model):
    userid = models.CharField(max_length=100)
    productid = models.CharField(max_length=100)
    qty=models.PositiveBigIntegerField()
    totalprice=models.PositiveBigIntegerField()
    orderid=models.CharField(max_length=5,default="0")

    def __str__(self):
        return self.userid

