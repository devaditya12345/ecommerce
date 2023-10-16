from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q


class ProductQuerySet(models.QuerySet):
    def search(self, query=None):
        if query is None or query == "":
            return self.none()
        lookups = (
            Q(name__icontains=query) | 
            Q(description__icontains=query) 
        )
        return self.filter(lookups) 

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True) # django default user model
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200,null=True)

    def __str__(self):
        # return str(self.email)
        return self.email

# Question --> null=True,blank=True kya hai and  def __str__(self): , on_delete=models.SET_NULL kya hai
class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    digital = models.BooleanField(default=False,null=True,blank=True)
    image = models.ImageField(null=True, blank=True)
    description=models.TextField(null=True)

    objects = ProductManager()

    def __str__(self):
        return self.name
    
    # Is function ko yh maante hue likha gya hai ki product me koi image nhi hogi tb kya hoga , aise me error ki sambhavnaaye hai
    @property
    def imageURL(self):
        # pehle jb url call hoga tab try krke dekhenge koi image url (image) hai ki nahi
        try: 
            url = self.image.url
        # nhi hone pe empty string pass ho jaegi
        except:
            url = ""
        return url

#one to many relationship i.e. one customer have several orders    
class Order(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered=models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=True)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)
    
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False :  #if any one of the product is physical then set shipping to true
                shipping = True
        return shipping
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all() #order ordemitem me foreign key hai isiliye use kr sakte hain
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all() #order ordemitem me foreign key hai isiliye use kr sakte hain
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.SET_NULL, blank=True, null=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL, blank=True, null=True)
    quantity=models.IntegerField(default=0,null=True,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
class WishlistItem(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL, blank=True, null=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE, blank=True, null=True)
    date_added=models.DateTimeField(auto_now_add=True)
    # order=models.ForeignKey(Order,on_delete=models.SET_NULL, blank=True, null=True)
    # whishlist_quantity=models.IntegerField(default=0,null=True,blank=True)

    def __str__(self):
        return str(self.id)

# Many to one relationship
class ShippingAddress(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL, blank=True, null=True) # agar order delete ho gya to kam se kam customer se shipping info grab kr lenge
    order=models.ForeignKey(Order,on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


