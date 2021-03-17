from django.contrib.auth.models import AbstractUser
from djmoney.models.fields import MoneyField
from django.db import models
from django.conf import settings


class User(AbstractUser):
    pass

    def __str__(self):
        return f"{self.username}"


class Auction_category(models.Model):
    category_title = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.category_title}"


class Auction_listing(models.Model):
    is_active = models.BooleanField(default=True)
    listing_poster = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    listing_title = models.CharField(max_length=50)
    listing_category = models.ForeignKey(Auction_category, on_delete=models.CASCADE, default=1, related_name="Categories")
    listing_image = models.ImageField(null=True, blank=True, upload_to="images/")
    listing_image_url = models.CharField(null=True, blank=True, max_length=100) #I added this field in case the user's image is hosted on another website (for whatever reason)
    listing_description = models.TextField(max_length=500)
    listing_price = models.DecimalField(max_digits=6, decimal_places=2)
    listing_date_time_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    listing_winner = models.CharField(null=True, blank=True, max_length=50)
    listing_bid = models.DecimalField(null=True, blank=True, max_digits=6, decimal_places=2)

    def __str__(self):
        return f"Listing: {self.listing_title}"


class Auction_bid(models.Model):
    bid_maker = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.CharField(max_length=50)
    bid_amount = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.listing}, {self.bid_amount}, {self.bid_maker}"


class Auction_comment(models.Model):
    comment_listing = models.CharField(max_length=50)
    comment_posterid = models.CharField(max_length=50)
    comment_posterusername = models.CharField(max_length=50)
    comment_content = models.TextField(max_length=200)

    def __str__(self):
        return f"{self.comment_content}, posted by: {self.comment_posterusername}"


class Auction_watchlist(models.Model):
    watchlist_item_adder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    watchlist_auction_listing = models.ForeignKey(Auction_listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.watchlist_auction_listing}, added to watchlist by: {self.watchlist_item_adder}"
