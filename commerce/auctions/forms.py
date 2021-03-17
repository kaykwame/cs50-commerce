from django import forms
from django.views.generic.edit import FormView
from .models import User, Auction_category, Auction_listing, Auction_bid, Auction_comment, Auction_watchlist


class listing_creation_form(forms.ModelForm):
    class Meta:
        model = Auction_listing
        fields = [
            "listing_title",
            "listing_category",
            "listing_description",
            "listing_image",
            "listing_image_url", #I added this field in case the user's image is hosted on another website (for whatever reason)
            "listing_price"
        ]

        labels = {
            "listing_title": "",
            "listing_category": "",
            "listing_description": "",
            "listing_image": "Upload image (optional)..",
            "listing_image_url": "",
            "listing_price": "",
        }

        widgets ={
        "listing_title": forms.TextInput(attrs={'placeholder': 'Enter listing title here..'}),
        "listing_description": forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter listing description here..'}),
        "listing_image_url": forms.TextInput(attrs={'placeholder': 'Or paste listing image url here (optional)..', 'size': '37'}),
        "listing_price": forms.TextInput(attrs={'placeholder': 'Enter listing price here..'})
        }


class comment_creation_form(forms.ModelForm):
    class Meta:
        model = Auction_comment
        fields = [
            "comment_content",
        ]

        labels = {
            "comment_content": "",
        }

        widgets ={
        "comment_content": forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your comment here..'}),
        }


class watchlist_creation_form(forms.ModelForm):
    class Meta:
        model = Auction_watchlist
        fields = [

        ]

class bid_creation_form(forms.ModelForm):
    class Meta:
        model = Auction_bid
        fields = [
        "bid_amount"
        ]

        labels = {
            "bid_amount": "",
        }

        widgets ={
        "bid_amount": forms.TextInput(attrs={'placeholder': 'Enter bid amount here..'}),
        }


class category_creation_form(forms.ModelForm):
    class Meta:
        model = Auction_category
        fields = [
            "category_title"
        ]

        labels = {
            "category_title": "",
        }

        widgets ={
        "category_title": forms.TextInput(attrs={'placeholder': 'Enter category title here in small letters..', 'size': '35'}),
        }
