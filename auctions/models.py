from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=64, unique=True, null=False, blank=False)
    def __str__(self):
        return self.category
    
class Bid(models.Model):
    bid = models.IntegerField(default=0)
    bid_owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_bids")
    listing_id = models.IntegerField()
    
    def __str__(self):
        return f"${self.bid}"
    
class Listing(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_listings", null=False, blank=False)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=300)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_listings")
    image = models.URLField(max_length=800, blank=True, null=True)
    price = models.ForeignKey(Bid, on_delete=models.SET_NULL, null=True, related_name="bid_listings")
    active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="won_listings")
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    w_listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.w_listing} watchlisted by {self.user}."

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_comments")
    comment = models.CharField(max_length=300)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.author} on {self.listing}: {self.comment}"