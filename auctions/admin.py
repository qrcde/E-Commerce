from django.contrib import admin
from .models import Listing, Comment, Bid, Category, Watchlist

# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    #Listing fields displayed to admin:
    list_display = ('title', 'category', 'price', 'active', 'owner', 'created')
    #Fields admin can edit:
    fields = ('title', 'description', 'category', 'price', 'active', 'image')

class BidAdmin(admin.ModelAdmin):
    #Bid fields displayed to admin:
    list_display = ('bid_owner', 'bid', 'get_listing')
    list_display_links = ('bid_owner', 'bid', 'get_listing')

    #Method to retrieve listing title by listing_id from Bid
    #since the Bid model doesn't store Listing as ForeignKey
    def get_listing(self, obj):
        try:
            listing = Listing.objects.get(id=obj.listing_id)
            return listing.title
        except Listing.DoesNotExist:
            return "Unknown"
    
    get_listing.admin_order_field = 'listing_id'
    #Assign a user-friendly column name:
    get_listing.short_description = "Listing" 
    

class CommentAdmin(admin.ModelAdmin):
    #Comment fields displayed to admin:
    list_display = ('listing', 'comment_author', 'comment')

    #Assign a user-friendly column name:
    def comment_author(self, obj):
        return obj.author
    comment_author.short_description = "Comment Author"

class WatchlistAdmin(admin.ModelAdmin):
    #Watchlist fields displayed to admin:
    list_display = ('listing_title', 'listing_owner', 'watchlisted_by')

    #Assign user-friendly column names:
    def listing_title(self, obj):
        return obj.w_listing.title
    listing_title.short_description = "Listing Title"

    def listing_owner(self, obj):
        return obj.w_listing.owner
    listing_owner.short_description = "Listing Owner"

    def watchlisted_by(self, obj):
        return obj.user
    watchlisted_by.short_description = "Watchlisted By"


admin.site.register(Listing, ListingAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Category)
admin.site.register(Watchlist, WatchlistAdmin)
