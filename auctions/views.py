from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import get_object_or_404
from .models import User, Auction_category, Auction_listing, Auction_bid, Auction_watchlist, Auction_comment
from .forms import listing_creation_form, comment_creation_form, watchlist_creation_form, bid_creation_form, category_creation_form
from django.contrib.auth.decorators import login_required


def index(request):
    active_listings = Auction_listing.objects.filter(is_active=True)
    inactive_listings = Auction_listing.objects.filter(is_active=False)
    return render(request, "auctions/index.html", {
    "active_listings": active_listings,
    "inactive_listings": inactive_listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


#Attempt to create a new listing
@login_required(login_url="login")
def create_listing(request):
    if request.method == "POST":
        form = listing_creation_form(request.POST, request.FILES)
        formC = category_creation_form(request.POST or None)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.listing_poster = request.user
            listing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/createlisting.html", {"form": form, "formC": category_creation_form})
    else:
        form = listing_creation_form()
        return render(request, "auctions/createlisting.html", {"form": listing_creation_form, "formC": category_creation_form})


#Get and display details of a listing post
@login_required(login_url="login")
def listing_details(request, pk):
    user = request.user
    #user_id = user.id
    listings = Auction_listing.objects.all()
    listing = Auction_listing.objects.get(pk=pk)
    winner = listing.listing_winner
    comment_form = comment_creation_form(request.POST or None)
    bid_form = bid_creation_form(request.POST or None)
    comments = Auction_comment.objects.filter(comment_listing=pk)
    item = get_object_or_404(Auction_listing, pk=pk)
    if request.method == "POST":
        return render(request, "auctions/listingpage.html", {
            "listing": listing,
            "listings": listings,
            "comment_form": comment_form,
            "bid_form": bid_form,
            "comments": comments,
            })
    else:
        try:
            #Get latest bid information if there is a bid
            latest_bid_amount = Auction_bid.objects.filter(listing=pk).latest("bid_amount").bid_amount
            latest_bid_maker = Auction_bid.objects.filter(listing=pk).latest("bid_amount").bid_maker
            #If listing is inactive, display winner message to user of winning bid.
            if listing.is_active == False:
                if f"{user}" == f"{winner}":
                    messages.info(request, "Congratulations, you are the winner!")
                    return render(request, "auctions/closedlisting.html", {
                    "listing": listing,
                    "listings": listings,
                    "winner": winner,
                    "latest_bid_amount": latest_bid_amount,
                    "latest_bid_maker": latest_bid_maker,
                    "user": user,
                    })
                else:
                    #If listing is inactive, display 'Already sold..' message to user who is not the winner.
                    messages.info(request, "Inactive listing. Already sold to another user.")
                    return render(request, "auctions/closedlisting.html", {
                    "listing": listing,
                    "listings": listings,
                    "winner": winner,
                    "latest_bid_amount": latest_bid_amount,
                    "latest_bid_maker": latest_bid_maker,
                    "user": user,
                    })
            else:
                #This piece of code is called if listing is active and is added to current user's watchlist
                if Auction_watchlist.objects.filter(watchlist_item_adder=user, watchlist_auction_listing=item).exists():
                    return render(request, "auctions/listingpage.html", {
                    "listing": listing,
                    "listings": listings,
                    "comment_form": comment_creation_form(),
                    "bid_form": bid_creation_form(),
                    "comments": comments,
                    "added": True,
                    "latest_bid_amount": latest_bid_amount,
                    "latest_bid_maker": latest_bid_maker,
                    })
                else:
                    #This piece of code is called if listing is active and is NOT added to current user's watchlist
                    return render(request, "auctions/listingpage.html", {
                    "listing": listing,
                    "listings": listings,
                    "comment_form": comment_creation_form(),
                    "bid_form": bid_creation_form(),
                    "comments": comments,
                    "added": False,
                    "latest_bid_amount": latest_bid_amount,
                    "latest_bid_maker": latest_bid_maker,
                    })
        except Auction_bid.DoesNotExist:
            #This piece of code is called if there is no bid on the listing item.
            if listing.is_active == False:
                    #If the listing is inactive and there is no bid on the item, display 'No winner' message.
                    messages.info(request, "There is no winner for this item")
                    return render(request, "auctions/closedlisting.html", {
                    "listing": listing,
                    "listings": listings,
                    "message": "There is no winner for this item",
                    })
            else:
                #If there is no bid and listing is active AND added to a watchlist.
                if Auction_watchlist.objects.filter(watchlist_item_adder=user, watchlist_auction_listing=item).exists():
                    return render(request, "auctions/listingpage.html", {
                    "listing": listing,
                    "listings": listings,
                    "comment_form": comment_creation_form(),
                    "bid_form": bid_creation_form(),
                    "comments": comments,
                    "added": True,
                    })
                else:
                    #If there is no bid and listing is active AND is NOT added to a watchlist.
                    return render(request, "auctions/listingpage.html", {
                    "listing": listing,
                    "listings": listings,
                    "comment_form": comment_creation_form(),
                    "bid_form": bid_creation_form(),
                    "comments": comments,
                    "added": False,
                    })


#Add listing to current user's watchlist.
@login_required(login_url="login")
def add_to_watchlist(request, pk):
    item_adder = request.user
    item = Auction_listing.objects.get(pk=pk)
    #If by any means the user adds an item to their watchlist more than once, display 'Already on watchlist' message.
    if Auction_watchlist.objects.filter(watchlist_item_adder=item_adder, watchlist_auction_listing=item).exists():
        messages.info(request, "You already have this in your watchlist.")
        return HttpResponseRedirect(reverse("listing_details", args=(pk, )))
    else:
        #Display 'Success' message when user adds items to their watchlist.
        Auction_watchlist(watchlist_item_adder=item_adder, watchlist_auction_listing=item).save()
        messages.add_message(request, messages.SUCCESS, "Successfully added to your watchlist.")
        return HttpResponseRedirect(reverse("listing_details", args=(pk, )))


#Remove listing from current user's watchlist.
@login_required(login_url="login")
def remove_from_watchlist(request, pk):
    item_adder = request.user
    item = get_object_or_404(Auction_listing, pk=pk)
    Auction_watchlist.objects.filter(watchlist_item_adder=item_adder, watchlist_auction_listing=item).delete()
    messages.add_message(request, messages.SUCCESS, "Successfully removed from your watchlist.")
    return HttpResponseRedirect(reverse("listing_details", args=(pk, )))


#Get current user's watchlist items and display them on webpage.
@login_required(login_url="login")
def watchlist(request, pk):
    watchlist_items = Auction_watchlist.objects.filter(watchlist_item_adder=pk)
    return render(request, "auctions/watchlist.html", {"watchlist_items": watchlist_items})


#Get categories and display them on webpage.
@login_required(login_url="login")
def categories(request):
    items = Auction_category.objects.all()
    return render(request, "auctions/categories.html", {"items": items})


#Create category
@login_required(login_url="login")
def add_category(request):
    if request.method == "POST":
        form = category_creation_form(request.POST or None)
        if form.is_valid():
            category = form.save(commit=False)
            title = form.cleaned_data['category_title']
            capitalized_title = title.capitalize()
            try:
                Auction_category.objects.get(category_title=capitalized_title)
                messages.info(request, "This category already exists..")
                return HttpResponseRedirect(reverse("create_listing"))
            except Auction_category.DoesNotExist:
                category.category_title = capitalized_title
                form.save()
                messages.info(request, "Category successfully created..")
                return HttpResponseRedirect(reverse("create_listing"))
        else:
            messages.info(request, "Form is not valid..")
            return HttpResponseRedirect(reverse("create_listing"))
    else:
        pass


#Place a bid for item
@login_required(login_url="login")
def bid_for_item(request, pk):
    if request.method == "POST":
        list_of_bids = []
        item = get_object_or_404(Auction_listing, pk=pk)
        form = bid_creation_form(request.POST or None)
        if form.is_valid():
                bidform = form.save(commit=False)
                bid = bidform.bid_amount
                ilisting_price = item.listing_price
                #This piece of code is called if the current user's bid is greater than the listing's initial price.
                if bid > ilisting_price:
                    try:
                        latest_bid = Auction_bid.objects.filter(listing=pk).latest("bid_amount").bid_amount
                        #If there is already a bid for the listing item, the current user's bid must be greater than..
                        #..the already existing bid.
                        if bid > latest_bid:
                            bidform.bid_maker = request.user
                            bidform.listing = pk
                            bidform.save()
                            item.listing_bid = bid
                            item.save()
                            messages.info(request, "Bid successfully made.")
                            return HttpResponseRedirect(reverse("listing_details", args=(pk, )))
                        else:
                            #Display error message if current user's bid is less than already exisiting bid.
                            messages.info(request, "Bid amount must be larger than the highest bid.")
                            return HttpResponseRedirect(reverse("listing_details", args=(pk, )))

                    #If there is no existing bid and current user's bid is greater than the listing's initial price.
                    except Auction_bid.DoesNotExist:
                        bidform.bid_maker = request.user
                        bidform.listing = pk
                        bidform.save()
                        item.listing_bid = bid
                        item.save()
                        messages.info(request, "Bid successfully made.")
                        return HttpResponseRedirect(reverse("listing_details", args=(pk, )))
                else:
                    #Display error message if current user's bid is less than the listing's initial price.
                    messages.info(request, "Bid amount must be larger than the listing price.")
                    return HttpResponseRedirect(reverse("listing_details", args=(pk, )))
        else:
            #Display error message if form is not valid.
            messages.info(request, "Form is not valid.")
            return HttpResponseRedirect(reverse("listing_details", args=(pk, )))
    else:
        #If request is GET, do nothing.
        pass


#Close bid
@login_required(login_url="login")
def close_bid (request, pk):
    winner = Auction_bid.objects.filter(listing=pk).latest("bid_amount").bid_maker.username
    listing = Auction_listing.objects.get(pk=pk)
    listing.is_active = False
    listing.listing_winner = winner
    listing.save()
    return HttpResponseRedirect(reverse("index"))


#Add comment on listing page
@login_required(login_url="login")
def add_comment(request, pk):
    if request.method == "POST":
        comment_form = comment_creation_form(request.POST or None)
        if comment_form.is_valid():
            content = comment_form.cleaned_data["comment_content"]
            comment = Auction_comment(comment_listing=pk, comment_posterid=request.user.id, comment_posterusername=request.user.username, comment_content=content)
            comment.save()
            return HttpResponseRedirect(reverse("listing_details", args=(pk, )))
        else:
            pass
    else:
        pass


#Display listings by categories
@login_required(login_url="login")
def listings_by_categories(request, pk, category):
    listings = Auction_listing.objects.filter(listing_category=pk, is_active=True)
    return render(request, "auctions/listingsbycategory.html", {"listings": listings, "category": category})
