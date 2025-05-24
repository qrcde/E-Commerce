from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django import forms

from .models import User, Listing, Bid, Comment, Category, Watchlist

#Form to create listings
class CreateListingForm(forms.ModelForm):
    #The 1st existing category is shown as the default option in the dropdown menu
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=None, required=True, initial=Category.objects.first())
    class Meta:
        model = Listing
        fields = ['category', 'title', 'description', 'image']
        
#Form to create bids        
class CreateBidForm(forms.ModelForm):
    bid = forms.IntegerField(min_value=0)
    class Meta:
        model = Bid
        fields = ['bid']

#Form to create comments
class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'placeholder': "Your comment here:",
                'style': 'width: 100%; height: 150px; resize: none;',
                'class': 'form-control',
            }),
        }
        #Remove comment field label:
        labels = {
            'comment': ''
        }

#Display all currently active listings
#For logged-in users, also display the listings won and/or closed by the user
def index(request):
    active_listings = Listing.objects.filter(active=True)
    won_listings = []
    closed_listings = []
    if request.user.is_authenticated:
        won_listings = Listing.objects.filter(active=False, winner=request.user)
        closed_listings = Listing.objects.filter(active=False, owner=request.user)

    return render(request, "auctions/index.html", {
        "listings": active_listings,
        "won_listings": won_listings,
        "closed_listings": closed_listings,
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

#Create a new listing:
@login_required(login_url='login')
def create(request):
    if request.method == "GET":
        listing_form = CreateListingForm()
        bid_form = CreateBidForm()
        return render(request, "auctions/create.html",{
            'listing_form' : listing_form,
            'bid_form' : bid_form
        })
    if request.method == "POST":
        listing_form = CreateListingForm(request.POST)
        bid_form = CreateBidForm(request.POST)
        if listing_form.is_valid() and bid_form.is_valid():
                category = listing_form.cleaned_data['category']
                title = listing_form.cleaned_data['title']
                description = listing_form.cleaned_data['description']
                image = listing_form.cleaned_data['image']
                bid = bid_form.cleaned_data['bid']    
                
                #Create initial bid object with a placeholder listing_id
                #to resolve circular dependency between bid and listing
                initialBid = Bid(
                    bid=bid,
                    bid_owner=request.user,
                    listing_id = Listing.objects.last().id+1 if Listing.objects.last() else 1
                )
                initialBid.save()

                listing = Listing(
                    category=category,
                    title=title,
                    description=description,
                    image=image,
                    owner=request.user,
                    price=initialBid
                )
                listing.save()

                #Update the placeholder listing_id with the actual newly generated listing id:
                initialBid.listing_id=listing.id
                initialBid.save()
                return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create.html", {
                'listing_form': listing_form,
                'bid_form': bid_form
            })    

#Display an individual listing on its own page:
@login_required(login_url='login') 
def listing_view(request, listing_id):
    try:
        listing = Listing.objects.get(id=listing_id)
        #Check if the listing is watchlisted by the current user:
        watchlisted = Watchlist.objects.filter(user=request.user, w_listing=listing).exists()
        #Load comments and comment form:
        comments = Comment.objects.filter(listing=listing)
        comment_form = CreateCommentForm()
        return render(request, "auctions/listing.html", 
                      {"listing" : listing,
                       "watchlisted": watchlisted,
                       "comments": comments,
                       "comment_form": comment_form,
                      })
    except Listing.DoesNotExist:
        return render(request, "auctions/listing.html", {"error_message": "The listing does not exist."})

#Watchlist view, handles adding and removing listings to/from user's watchlist:
@login_required(login_url='login')    
def watchlist(request, action, listing_id):
    try:
        listing = Listing.objects.get(id=listing_id)
        watchlisted = request.user.is_authenticated and request.user.watchlist.filter(w_listing=listing).exists()
        if action == "add":
            if not Watchlist.objects.filter(user=request.user, w_listing=listing).exists():
                Watchlist.objects.create(user=request.user, w_listing=listing)
                watchlisted = True
        elif action == "remove":
                to_remove = Watchlist.objects.filter(user=request.user, w_listing=listing)
                if to_remove:
                    to_remove.delete()
                    watchlisted = False

        comments = Comment.objects.filter(listing=listing)
        comment_form = CreateCommentForm()

        return render(request, "auctions/listing.html", 
                      {"listing" : listing,
                       "watchlisted" : watchlisted,
                       "comments": comments,
                       "comment_form": comment_form,
                       })
        
    except Listing.DoesNotExist:
        return render(request, "auctions/listing.html", {"error_message": "The listing does not exist."})

#Display the watchlist of the logged in user on a dedicated page
@login_required(login_url='login')    
def user_watchlist(request):
    watchlisted_listings = Listing.objects.filter(id__in=Watchlist.objects.filter(user=request.user).values('w_listing'))
    return render(request, "auctions/watchlist.html", {"watchlisted_listings" : watchlisted_listings})

#Place a new bid
@login_required(login_url="login")
def make_bid(request, listing_id):
    try:
        listing = Listing.objects.get(id=listing_id)
        new_bid = None
        message = None
        watchlisted = request.user.is_authenticated and request.user.watchlist.filter(w_listing=listing).exists()
        if request.method == "POST":
            #Validate the bid form and process data:
            new_bid_form = CreateBidForm(request.POST, initial={'listing_id': listing_id})
            if new_bid_form.is_valid():
                new_bid = new_bid_form.save(commit=False)
                new_bid.listing_id = listing_id
                #Get the value of the initial bid:
                first_bid = Bid.objects.filter(listing_id=listing_id).order_by('id').first().bid
                #Get the number of existing bids:
                num_bids = Bid.objects.filter(listing_id=listing_id).count()
                if new_bid.bid < first_bid and num_bids == 1:
                    message = f"Your bid must be equal to or greater than ${first_bid}."
                #Assume the 'price' value holds the highest bid:
                elif new_bid.bid <= listing.price.bid and num_bids > 1:
                    message = f"Your bid must be greater than the current highest bid: ${listing.price.bid}."
                else:
                    new_bid.bid_owner = request.user
                    new_bid.save()
                    listing.price = new_bid
                    listing.save()
                    return redirect('listingview', listing_id=listing_id)
        else:
            new_bid_form = CreateBidForm(initial={'listing_id': listing_id})  

        #Display the listing page with the bid form:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "new_bid_form": new_bid_form,
            "bid" : new_bid,
            "message" : message,
            "watchlisted": watchlisted,
        })
    except Listing.DoesNotExist:
        return redirect("index")

#Handle comments:
@login_required(login_url="login")
def comment(request, listing_id):
    try:
        listing = Listing.objects.get(id=listing_id)
        watchlisted = request.user.is_authenticated and request.user.watchlist.filter(w_listing=listing).exists()
        if request.method == "POST":
            form = CreateCommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                comment.listing = listing
                comment.save()
                return redirect('listingview', listing_id=listing_id)
            else:
                comments = Comment.objects.filter(listing=listing).order_by('-id')
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "comments": comments,
                    "comment_form": form,
                    "watchlisted": watchlisted,
                })
        else:
            return redirect('listingview', listing_id=listing_id)
    except Listing.DoesNotExist:
        return render(request, "auctions/listing.html", {"error_message": "The listing does not exist."})

#Display the list of categories     
def categories(request, category_id=None):
    categories = Category.objects.all()
    listings = None
    selected_category = None
    #Display listings from the selected category:
    if category_id:
        selected_category = Category.objects.filter(id=category_id).first()
        if selected_category:
            listings = Listing.objects.filter(category=selected_category, active=True)
    return render(request, "auctions/categories.html", {
        "categories": categories,
        "listings": listings,
        "selected_category": selected_category,
    })

#Close listing
@login_required(login_url="login")
def close(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    if request.user == listing.owner and listing.active:
        listing.active = False
        listing.save()
        highest_bid = listing.price
        #Determine the auction winner if there are bids:
        if highest_bid and highest_bid.bid_owner and highest_bid.bid_owner != request.user:
            listing.winner = highest_bid.bid_owner
            listing.save()
        else:
            #If there are no bids, winner is None:
            listing.winner = None
            listing.save()
        listing.save()
    return redirect('listingview', listing_id=listing_id)

