# 🛒 E-Commerce Auction Platform
An eBay-style auction website built with Django. 
Allows users to create auction listings, place and manage bids, comment on listings, maintain personalized watchlists, and browse items by category. 
Developed as part of the CS50 Web Programming course, the project showcases comprehensive backend and frontend integration using Django.

## 🌟 Features
- **User Authentication:**
  register, login, and logout using Django’s authentication system
- **Auction Listings:**
  users can create listings with a title, description, starting bid, optional image, and category
- **Bidding System:**
  enforces bid rules (bids must exceed the current highest bid or starting bid)
- **Listing Detail Page:**
  view all listing details and interact with them depending on user role
- **Watchlist:**
  add or remove listings from a personal watchlist
- **Comments:**
  post and view comments on individual listings
- **Auction Closure:**
  listing creators can close auctions and designate the highest bidder as winner
- **Categories:**
  browse active listings by category
- **Django Admin Interface:**
  admins can manage all listings, bids, and comments via the admin dashboard

## 🛠️ Technologies
- Python3
- Django Framework
- SQLite
- HTML5 / CSS

## 🚀 Getting Started
1. **Clone the repository:** <br>
   `git clone https://github.com/your-username/auction-site.git` <br>
   `cd auction-site`
2. **Create a virtual environment:** <br>
   `python3 -m venv venv` <br>
   `venv\Scripts\activate`
4. **Apply database migrations:** <br>
   `python manage.py makemigrations auctions` <br>
   `python manage.py migrate`
5. **Run the development server** <br>
   `python manage.py runserver`
6. **Visit the application** <br>
   Open `http://127.0.0.1:8000/`in your browser


##

_Developed by [qrcde](https://github.com/qrcde) as part of Harvard's CS50's Web Programming with Python and JavaScript course._

