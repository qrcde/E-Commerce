from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:listing_id>", views.listing_view, name="listingview"),
    path("watchlist/", views.user_watchlist, name="user_watchlist"),
    path("watchlist/<str:action>/<int:listing_id>", views.watchlist, name="watchlist"),
    path("make_bid/<int:listing_id>", views.make_bid, name="make_bid"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
    path("categories", views.categories, name="categories"),
    path('categories/<int:category_id>/', views.categories, name='categories'),
    path('close/<int:listing_id>/', views.close, name='close'),
]
