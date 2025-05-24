# 🛒 E-Commerce Auction Platform
A eBay-style auction website built with Django. 
This web application allows users to create auction listings, place and manage bids, comment on listings, maintain personalized watchlists, and browse items by category. 
Designed as part of a CS50 Web Programming course project, this application demonstrates comprehensive backend and frontend integration using Django.

## 🌟 Features
- **User Authentication**
  - Register, login, and logout using Django’s authentication system
- **Auction Listings**
  - Users can create listings with a title, description, starting bid, optional image, and category
- **Bidding System**
  - Enforces bid rules: bids must exceed the current highest bid or starting bid
- **Listing Detail Page**
  - View all listing details and interact with them depending on user role
- **Watchlist**
  - Add or remove listings from a personal watchlist
- **Comments**
  - Post and view comments on individual listings
- **Auction Closure**
  - Listing creators can close auctions and designate the highest bidder as winner
- **Categories**
  - Browse active listings by category
- **Django Admin Interface**
  - Admins can manage all listings, bids, and comments via the admin dashboard

## 🛠️ Technologies
- Python3
- Django Framework
- SQLite
- HTML5 / CSS

## 🚀 Getting Started
1. **Clone the repository**
   git clone https://github.com/your-username/auction-site.git
   cd auction-site
2. **Create a virtual environment**
   python3 -m venv venv
   venv\Scripts\activate
4. **Apply database migrations**
   python manage.py makemigrations auctions
   python manage.py migrate
5. **Run the development server**
   python manage.py runserver
6. **Visit the application**
   Open your browser and go to `http://127.0.0.1:8000/`
