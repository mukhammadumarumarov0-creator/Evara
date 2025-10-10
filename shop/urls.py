from django.urls import path,include
from .views import dashboard,details,shop,accounts,cart,check_out,login_regester,wish_list,logout_user,create_account,selected_items

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




]