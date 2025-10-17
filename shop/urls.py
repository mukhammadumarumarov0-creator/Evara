from django.urls import path,include
from shop.views.user import login_regester,logout_user,create_account
from shop.views.shop import dashboard,details,check_out,shop,selected_items,accounts
from shop.views.cart import cart,cart_page,wish_list,add_to_wishlist,remove_item_form_cart,remove_item_from_wishlist

urlpatterns = [
    path("",dashboard,name="dashboard"),
    path("details/<int:id>/",details,name="details"),
    path("shop/",shop,name="shop"),
    path("accounts/",accounts,name="account"),
    path("cart/",cart,name="cart"),
    path("checkout/",check_out,name="checkout"),

    path("register/",login_regester,name="register"),
    path("create_account/",create_account,name="create_account"),
    path("logout/",logout_user,name="logout_user"),
    
    path("selected_ones/<int:category_id>/",selected_items,name="selected_ones"),
    path("wishlist/",wish_list,name="wishlist"),

    path("wishlist/add/<int:product_id>/",add_to_wishlist),
    path("cart/add/<int:product_id>/",cart_page,name="add_product"),
    path("remove/<int:product_id>/",remove_item_form_cart,name="remove"),
    path("wishlist/remove/<int:product_id>/",remove_item_from_wishlist,name="wishlist_remove"),




    





]