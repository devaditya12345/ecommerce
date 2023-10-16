from django.urls import path

from . import views

urlpatterns = [
        #Leave as empty string for base url
	path('store/', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),

    #search
    path('search/', views.search_view, name='search'),

    #wishlist
    path('wishlist/', views.wishlist, name="wishlist"), # GET request (getting data from database)
    path('create_wishlist_item/', views.createWishListItem, name="create_wishlist_item"), # POST request
    path('delete_wishlist_item/<int:id>', views.deleteWishListItem, name="delete_wishlist_item"), # DELETE request
    
	path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    
	# Accounts URL
	path('',views.login_view,name="login"),
    path('logout/',views.logout_view,name="logout"),
    path('register/',views.register_view,name="register"),


]