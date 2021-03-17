from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newlisting", views.create_listing, name="create_listing"),
    path("listingdetail/<int:pk>", views.listing_details, name="listing_details"),
    path("watchlist/<int:pk>", views.watchlist, name="watchlist"),
    path("add_to_watchlist/<int:pk>", views.add_to_watchlist, name="add_to_watchlist"),
    path("remove_from_watchlist/<int:pk>", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("categories", views.categories, name="categories"),
    path("bid/<int:pk>", views.bid_for_item, name="bid_for_item"),
    path("close_bid/<int:pk>", views.close_bid, name="close_bid"),
    path("add_comment/<int:pk>", views.add_comment, name="add_comment"),
    path("listings_by_categories/<int:pk>/<str:category>", views.listings_by_categories, name="listings_by_categories"),
    path("add_category", views.add_category, name="add_category"),
]
