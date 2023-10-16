import json
from .models import *

def cookieCart(request):

    try:
        cart = json.loads(request.COOKIES['cart'])
          #if the cart is not updated yet, a wholly new page     
    except:
            cart = {}
    print('Cart:' , cart)
    items = []
    order = {'get_cart_items':0 ,'get_cart_total':0 , 'shipping':False }
    cartItems = order['get_cart_items']

    for i in cart:
               try:
                    cartItems += cart[i]["quantity"] # i is productId here
 
                     
                    product = Product.objects.get(id=i)
                    total = (product.price * cart[i]["quantity"])

                    order['get_cart_total'] += total
                    order['get_cart_items'] += cart[i]["quantity"]

                    item = {
                             'product' : {
                                  'id': product.id,
                                  'name': product.name,
                                  'price': product.price,
                                  'imageURL': product.imageURL,
                               },
                          'quantity' :cart[i]["quantity"],
                          'get_total' : total
                          }
                    items.append(item)

                    if product.digital == False :
                       order['shipping'] = True

               except:
                    pass
    return{'cartItems':cartItems, 'order':order, 'items':items}

def cartData(request):
     #Ek cheeze hmko theek karna hai ki,jb hm login krte hai to user create hota hai customer nhi
     if request.user.is_authenticated:
          customer = request.user.customer #acess the authenticated user's customer
          order, created = Order.objects.get_or_create(customer = customer , complete = False) # whi wala info fetch karo jisme ye wala customer ho and complete status false or no ho
         
          items = order.orderitem_set.all() #items wo lene hai jiska parent order wo ho abhi jo fetch hua h
          # items1 = order.wishlistitem_set.all()
          # items1 = products.wishlistitem_set.all()
          cartItems = order.get_cart_items # Total numbers order_item which get connected with the particular objects
     else:
          cookieData = cookieCart(request)
          cartItems = cookieData['cartItems']
          order = cookieData['order']
          items = cookieData['items']

     return {'cartItems':cartItems, 'order':order, 'items':items}

# Ye thoda Yash se poochna
def guestOrder(request, data):
          print('User is not logged in.')
          print('COOKIES:' , request.COOKIES)
          name = data['form']['name']
          email = data['form']['email']

          cookieData = cookieCart(request)
          items = cookieData['items']
          

          # Creating Guest Customer
          customer,created = Customer.objects.get_or_create(email=email,)

          customer.name = name
          customer.save()

          order = Order.objects.create(
               customer=customer,
               complete=False,
          )

          for item in items:
               product = Product.objects.get(id=item['product']['id'])

               orderItem = OrderItem.objects.create(
                    product = product,
                    order = order,
                    quantity = item['quantity']
               )
               
          return customer, order


#Guest User WishlistItem

def wishistCookieCart(request):

    try:
        wishlistcart = json.loads(request.COOKIES['wishlistcart'])
          #if the cart is not updated yet, a wholly new page     
    except:
            wishlistcart = {}
    
    wishlistItems = []

    for i in wishlistcart:
               try:
                
                    product = Product.objects.get(id=i)
                    
                    item = {
                             'product' : {
                                  'id': product.id,
                                  'name': product.name,
                                  'price': product.price,
                                  'imageURL': product.imageURL,
                               },
                          
                          }
                    wishlistItems.append(item)


               except:
                    pass
    return{'wishlistItems':wishlistItems}


def wishlistData(request):
     
          wishlistCookieData = wishistCookieCart(request)
          wishlists = wishlistCookieData['wishlistItems']

          return {'wishlists':wishlists}
