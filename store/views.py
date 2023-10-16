from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart,cartData,guestOrder,wishlistData
from .models import *

# Accounts setting
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

# Create your views here.

def store(request):

     data = cartData(request)
     cartItems = data['cartItems']

     products = Product.objects.all()
     context = {'products': products,'cartItems': cartItems}
     return render(request, 'store/store.html', context)

def cart(request):

     data = cartData(request)
     cartItems = data['cartItems']
     order = data['order']
     items = data ['items']
          
     context = {'items': items , 'order': order,'cartItems': cartItems}
     return render(request, 'store/cart.html', context)


def checkout(request):
     
     data = cartData(request)
     cartItems = data['cartItems']
     order = data['order']
     items = data ['items']
          
     context = {'items': items , 'order': order , 'cartItems': cartItems , 'shipping':False}
     return render(request, 'store/checkout.html', context)

#for cart
def updateItem(request):
     data = json.loads(request.body) #parsed (convert) the data in json format as we stringy it while sending.
     productId = data['productId']
     action = data['action']

     print("Action:" ,action)
     print("ProductId:" ,productId)

     customer = request.user.customer # currently log in customer
     product = Product.objects.get(id=productId)
     order,created = Order.objects.get_or_create(customer=customer, complete = False)

     orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)


     if action == 'add_new':
          orderItem.quantity = 1
     elif action == 'add':
          orderItem.quantity = (orderItem.quantity+1)
     elif action == 'remove':
          orderItem.quantity = (orderItem.quantity-1)

     orderItem.save()

     if orderItem.quantity <= 0:
          orderItem.delete()

     return JsonResponse('Item was added', safe = False)

def wishlist(request):

     data = cartData(request)
     cartItems = data['cartItems']

     if request.method != 'GET':
          return "Bad request method"
     
     if request.user.is_authenticated:

          wishlists = WishlistItem.objects.filter(customer=request.user.customer)

     else :
          data2 = wishlistData(request)
          wishlists = data2['wishlists']
          
     # context = {'items': items , 'order': order,'cartItems': cartItems}
     # context = {'items': items , 'cartItems': cartItems}
     return render(request, 'store/wishlist.html', {"wishlists": wishlists,'cartItems': cartItems})


def createWishListItem(request):
     if request.method == 'POST':
          customer = request.user.customer
          data = json.loads(request.body)
          product_id = data['product_id']
          try:
               product = Product.objects.get(id=product_id)
          except Product.DoesNotExist:
               return JsonResponse('Error: Product not found', safe = False)
          
          wishlist_item_exists = WishlistItem.objects.filter(product=product, customer=customer).exists()

          if not wishlist_item_exists:
               WishlistItem.objects.create(product=product, customer=customer)
          else :
               pass

          return JsonResponse('Wishlist item was added', safe = False)

def deleteWishListItem(request, id):
     if request.method =='DELETE':
          try: 
               product = Product.objects.get(id=id)
               wishlist = WishlistItem.objects.filter(product=product) # filter that wishlist from all wishlist whose productID is this.
          except WishlistItem.DoesNotExist:
               return JsonResponse('Error: Wishlist not found', safe = False)
          
          # wishlist = WishlistItem.objects.filter(id=id)
          # if len(wishlist)>0:
          wishlist.delete()

          return JsonResponse('Wishlist deleted', safe = False)

# #for wishlist,Sahi ye bhi hai
# def updateWishListItem(request):
#      data = json.loads(request.body) #parsed (convert) the data in json format as we stringy it while sending.
#      productId = data['productId']
#      action = data['action']

#      print("Action:" ,action)
#      print("ProductId:" ,productId)

#      customer = request.user.customer # currently log in customer
#      product = Product.objects.get(id=productId)
#      # order,created = Order.objects.get_or_create(customer=customer, complete = False)

#      # wishlistItem, created = WishlistItem.objects.get_or_create(order=order, product=product)
#      wishlistItem, created = WishlistItem.objects.get_or_create(product=product)

#      if action == 'one':
#           wishlistItem.whishlist_quantity = 1
#      elif action == 'zero':
#           wishlistItem.whishlist_quantity = 0

#      wishlistItem.save()

#      if wishlistItem.whishlist_quantity <= 0:
#           wishlistItem.delete()

#      return JsonResponse('Item was added', safe = False)

#csrf exempt ka matlab hai csrf token ko consider nhi krna h, yha pe isliye isko use kiye hai kyonki logout ke samay order process mein dikkat aa rhi thi
#but this is a temporary solution, so isko comment kr diye hai , permanent solution checkout.html me form ke saath use kr liye hai

# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
def processOrder(request):
     transaction_id = datetime.datetime.now().timestamp()
     data = json.loads(request.body)
     # print('Data:', request.body)

     if request.user.is_authenticated:
          customer = request.user.customer
          order, created = Order.objects.get_or_create(customer=customer, complete = False) # is customer ke liye to get hi hoga
          

     else:
         customer, order = guestOrder(request,data)

     total = float(data['form']['total'])
     order.transaction_id = transaction_id
 
     #check considering the threat that well learned javascript developers could manipulate that data from frontend
     if total == float(order.get_cart_total):
          order.complete = True
     order.save()

     if order.shipping == True:
               ShippingAddress.objects.create(
			customer=customer,
			order=order,
			address=data['shipping']['address'],
			city=data['shipping']['city'],
			state=data['shipping']['state'],
			zipcode=data['shipping']['zipcode'],
			)
     return JsonResponse('Payment Complete', safe = False)


#search view

def search_view(request):
    
    data = cartData(request)
    cartItems = data['cartItems']

    query = request.GET.get('q')
    
    qs = Product.objects.search(query=query)
    context = {
     #    "queryset": qs,
        "products": qs,
        'cartItems': cartItems
    }
    template = "store/store.html"
#     if request.htmx:
    
#         context['queryset'] = qs
#         template = "search/results-view.html"
    return render(request, template, context)

# Accounts setting

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
             user=form.get_user()
             login(request,user)
        #yha pe ek alert message dalna hai
             return redirect('/store')
    else:
        form=AuthenticationForm(request)
    context={
        'form':form
    }
    if request.user.is_authenticated:
         return redirect('/store')
    return render(request,"store/login.html",context)

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/store')
    return render(request,"store/logout.html",{})

def register_view(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        email= request.POST.get('email')
        user_obj = form.save()

     #    Customer.objects.get_or_create(user= user_obj,name=username)
        Customer.objects.get_or_create(user= user_obj,name=user_obj.username,email=email)
        return redirect('/')
    context = {'form':form}
    return render(request,"store/register.html",context)