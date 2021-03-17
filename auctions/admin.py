from django.contrib import admin
from .models import User, Auction_category, Auction_listing, Auction_bid, Auction_comment, Auction_watchlist

class ShowDateAdmin(admin.ModelAdmin):
    readonly_fields = ('listing_date_time_created',)

# Register your models here.
admin.site.register(User)
admin.site.register(Auction_category)
admin.site.register(Auction_listing, ShowDateAdmin)
admin.site.register(Auction_bid)
admin.site.register(Auction_comment)
admin.site.register(Auction_watchlist)
#admin.site.register(Auction_watchlist_item)
