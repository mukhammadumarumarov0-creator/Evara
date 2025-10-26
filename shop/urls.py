from django.urls import path,include
from shop.views.user import LoginUserView,LogOutView,CreatAccountView
from shop.views.shop import DashboardView,DetailsView,ShopView,SelectedItemsView,AccountView,Password,ReviewView
from shop.views.cart import CartPageView,WishlistView,RemoveCartView,RemoveWishView,DetailAddProductView,DetailAddToWishlistView
from shop.views.order import GetCheckOutView


urlpatterns = [
    path("",DashboardView.as_view(),name="dashboard"),
    path("details/<int:id>/",DetailsView.as_view(),name="details"),
    path("shop/",ShopView.as_view(),name="shop"),
    path("accounts/",AccountView.as_view(),name="account"),
    path("cart/",CartPageView.as_view(),name="cart"),
    path("checkout/",GetCheckOutView.as_view(),name="checkout"),

    path("register/",LoginUserView.as_view(),name="register"),
    path("create_account/",CreatAccountView.as_view(),name="create_account"),
    path("logout/",LogOutView.as_view(),name="logout_user"),
    
    path("selected_ones/<int:category_id>/",SelectedItemsView.as_view(),name="selected_ones"),
    path("wishlist/",WishlistView.as_view(),name="wishlist"),

    path("wishlist/add/<int:product_id>/",WishlistView.as_view(),name="wishlist_add"),
    path("cart/add/<int:product_id>/",CartPageView.as_view(),name="add_product"),
    path("remove/<int:product_id>/",RemoveCartView.as_view(),name="remove"),
    path("wishlist/remove/<int:product_id>/",RemoveWishView.as_view(),name="wishlist_remove"),
    path("details/add/<int:id>/",DetailAddProductView.as_view(),name="add_product_from_details"),
    path("details/wishlist/add/<int:id>/",DetailAddToWishlistView.as_view(),name="add_product_from_details_to_wishlist"),
    path("password/",Password.as_view(),name="password"),
    path("review/<int:id>",ReviewView.as_view(),name="review"),








    





]